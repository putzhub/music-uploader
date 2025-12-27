import unittest
from musicuploader import *
import os
from pathlib import Path
import shutil
from mutagen.easyid3 import EasyID3

TESTING_DIR = "./test/testing"
CONTENT_DIR = "./tests/"
SOURCE_DIR = "./tests/Source"
TEST_JSON_PATH = "tests/release_example.json"

#ASSUMPTIONS
# Files in tests forlder: Cover.png and *.wav 
# Test does not cover albums yet

#Helpers
def assertIsFile(path):
    if not Path(path).resolve().is_file():
        raise AssertionError("File does not exist: %s" % str(path))

#Move to class itself
class TestInit(unittest.TestCase):
    #Make sure we can load a valid configuration
    def test_read_json(self):
        '''Make sure we can load the music data json file'''
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        self.assertIsInstance(music_release, MusicRelease)
        self.assertEqual(music_release.tracks[0]["title"], "Test")

class TestWithFiles(unittest.TestCase):
    #Prep & cleanup
    @classmethod
    def setUpClass(self):
        os.makedirs(TESTING_DIR)
    
    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test")

    music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)

    #Tests
    def test_make_mp3(self):
        #Create the file
        fname = "Test.wav"
        src_path = Path(SOURCE_DIR, fname)
        dest_path = Path(TESTING_DIR, fname[:-3] + "mp3")
        create_mp3(src_path, self.music_release.tracks[0], dest_path=dest_path)
        assertIsFile(dest_path)

        #Test tag data
        audio = EasyID3(dest_path)
        self.assertEqual(audio["title"], ["Test"])
        tags = ["artist", "website", "genre", "album"]
        for tag in tags:
            self.assertEqual(audio[tag], [self.music_release.tracks[0]["mp3"][tag]])

    #@unittest.skip("Too verbose")
    def test_make_mp4(self):
        #Create the file
        fname = "Test.wav"
        src_path = Path(SOURCE_DIR, fname)
        dest_path = Path(TESTING_DIR, fname[:-3] + "mp4")
        cover = Path(SOURCE_DIR, "Cover.png")
        create_mp4(src_path, dest_path, cover)
        assertIsFile(dest_path)

    def test_make_webp(self):
        #Create the file
        fname = "Cover.png"
        dest_path = Path(TESTING_DIR, self.music_release.tracks[0]["cover"])
        cover = Path(SOURCE_DIR, "Cover.png")
        create_webp(cover, dest_path)
        assertIsFile(dest_path)

    def test_zip_stems(self):
        src = Path(SOURCE_DIR, "Stems/")
        target = Path(TESTING_DIR, "Stems.zip")
        create_zip(src, str(target)[:-4]) #shutil.make_archive() doesn't need .zip extension
        assertIsFile(target)

#@unittest.skip("testing")
class TestPreprocessing(unittest.TestCase):
    #Prep & cleanup
    @classmethod
    def setUpClass(self):
        os.makedirs(TESTING_DIR)
    
    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test")

    #Tests
    def test_preprocessing(self):
        #Init the release
        music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR, TESTING_DIR)
        music_release.preprocessing()

        files = ["Test.mp3", "Test.mp4", "Stems.zip", "test.webp"]
        for f in files:
            assertIsFile(Path(TESTING_DIR, f))

class TestServices(unittest.TestCase):
    def test_youtube(self):
        '''Youtube related tests'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        #Ensure that we return False for code that depends on that.
        self.assertFalse(services.youtube.upload(None, music_release.tracks[0]))
    
    @unittest.skip("Annoying to test often")
    def test_itch(self):
        '''Prepare for posting to itch.io'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        #Should return something other than empty
        itch_url = services.itch.upload(music_release.tracks)
        self.assertIsNotNone(itch_url)
        self.assertIsNot(itch_url, "")

    @unittest.skip("Annoying to test often")
    def test_newgrounds(self):
        '''Prepare for posting to Newgrounds'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        #Should return something other than empty
        ng_url = services.newgrounds.upload(music_release.tracks)
        self.assertIsNotNone(ng_url)
        self.assertIsNot(ng_url, "")

    def test_upload_music(self):
        '''Make sure the full flow of uploading music works'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        music_release.upload_music()

class TestSocialMedia(unittest.TestCase):
    def test_mastodon(self):
        '''Mastodon - Make sure we can do everything besides post'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        track = music_release.tracks[0]
        self.assertTrue(services.mastoposter.post(
            track["summary"], 
            track["embed"].replace("embed", "video"),
            track["tags"],
            testing=True))
    
    @unittest.skip("Annoying to test often")
    def test_bluesky(self):
        '''Bluesky - Make sure we can do everything besides post'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        track = music_release.tracks[0]
        self.assertTrue(services.bsky.post(
            track["summary"],
            track["embed"].replace("embed", "video"),
            track["tags"],
            testing=True))

    @unittest.skip("Instagram is dogshit ._.")
    def test_instagram(self):
        '''Instagram - Make sure we can do everything besides post'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        track = music_release.tracks[0]
        self.assertTrue(services.instagram.post(
            track["summary"], 
            track["tags"],
            testing=True))

if __name__ == "__main__":
    unittest.main()