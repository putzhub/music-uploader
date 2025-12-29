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

#TODO Add more config files to test
# - Track that hasn't been uploaded yet
# - Fully uploaded track
# - Multiple tracks

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

    music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR, TESTING_DIR)

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
        MusicRelease(TEST_JSON_PATH, CONTENT_DIR, TESTING_DIR).preprocessing()

        files = ["Test.mp3", "Test.mp4", "Stems.zip", "test.webp"]
        for f in files:
            assertIsFile(Path(TESTING_DIR, f))
    
    def test_upload_music(self):
        '''Make sure the full flow of uploading music works'''
        music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR, TESTING_DIR)
        music_release.preprocessing()
        music_release.upload_music()
    
    @unittest.skip("Annoying to test frequently")
    def test_ludoloon_studio(self):
        music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR, TESTING_DIR)
        music_release.preprocessing()
        services.lls.post(music_release)
        os.remove("/home/pootz/Documentos/Websites/LudoLoonStudio/ludoloon.studio/content/images/covers/test.webp")


class TestServices(unittest.TestCase):
    def test_combine_tags(self):
        '''Make sure combine_tags gives the expected output'''
        tags = ["test", "if", "tags", "work", "Combined Word"]
        additional_tags = ["more", "of", "them"]
        tags_with_hashtags = "#test #if #tags #work #CombinedWord #more #of #them"
        tags_with_spaces = "test if tags work CombinedWord more of them"
        tags_with_commas = "test,if,tags,work,CombinedWord,more,of,them"

        c = services.combine_tags

        self.assertEqual(c(tags, additional_tags), tags_with_spaces)
        self.assertEqual(c(tags, additional_tags, separator=","), tags_with_commas)
        self.assertEqual(c(tags, additional_tags, prepend="#"), tags_with_hashtags)

    def test_prep_post(self):
        music_release = MusicRelease(TEST_JSON_PATH, SOURCE_DIR)
        #Still relevant for constructing the message to refer to one track
        track = music_release.tracks[0]
        #Prep the test message
        #MASTODON
        masto_msg = '''
{0}

{1}

{2}
'''.format(track["summary"], 
           track["streaming"]["youtube"], 
           services.combine_tags(services.mastoposter.DEFAULT_TAGS, track["tags"], prepend="#"))
        #Test results
        self.assertEqual(masto_msg, services.prep_post(music_release, services.Service.MASTODON))
        #INSTAGRAM
        insta_msg = '''
{0}

See link in bio for more.

{1}
'''.format(track["summary"], services.combine_tags(services.instagram.DEFAULT_TAGS, track["tags"], prepend="#"))
        #Test if we got the expected results
        self.assertEqual(insta_msg, services.prep_post(music_release, services.Service.INSTAGRAM))

    def test_youtube(self):
        '''Youtube related tests'''
        #Ensure that we return False for code that depends on that.
        self.assertEqual([('','')], 
                         services.youtube.upload(MusicRelease(TEST_JSON_PATH, SOURCE_DIR)))
    
    @unittest.skip("Annoying to test often")
    def test_itch(self):
        '''Prepare for posting to itch.io'''
        #Should return something other than empty
        itch_url = services.itch.upload(MusicRelease(TEST_JSON_PATH, SOURCE_DIR))
        self.assertIsNotNone(itch_url)
        self.assertIsNot(itch_url, "")

    @unittest.skip("Annoying to test often")
    def test_newgrounds(self):
        '''Prepare for posting to Newgrounds'''
        #Should return something other than empty
        ng_url = services.newgrounds.upload(MusicRelease(TEST_JSON_PATH, SOURCE_DIR))
        self.assertIsNotNone(ng_url)
        self.assertIsNot(ng_url, "")

class TestSocialMedia(unittest.TestCase):
    def test_mastodon(self):
        '''Mastodon - Make sure we can do everything besides post'''
        self.assertTrue(services.mastoposter.post(MusicRelease(TEST_JSON_PATH, SOURCE_DIR), 
                                                  testing=True))
    
    @unittest.skip("Annoying to test often")
    def test_bluesky(self):
        '''Bluesky - Make sure we can do everything besides post'''
        self.assertTrue(services.bsky.post(MusicRelease(TEST_JSON_PATH, SOURCE_DIR), 
                                           testing=True))

    @unittest.skip("Annoying to test often")
    def test_instagram(self):
        '''Instagram - Make sure we can do everything besides post'''
        self.assertTrue(services.instagram.post(MusicRelease(TEST_JSON_PATH, SOURCE_DIR), 
                                                testing=True))

    @unittest.skip("Annoying to test often")
    def test_patreon(self):
        services.patreon.post(MusicRelease(TEST_JSON_PATH, SOURCE_DIR))

if __name__ == "__main__":
    unittest.main()