import unittest
from musicuploader import *
import os
import pathlib
import shutil
from mutagen.easyid3 import EasyID3

TESTING_DIR = "./test/testing"
TESTS_DIR = "./tests/"
CONTENT_DIR = "./tests/Source"
TEST_JSON_PATH = "tests/release_example.json"

#ASSUMPTIONS
# Files in tests forlder: Cover.png and *.wav 
# Test does not cover albums yet

#Move to class itself
class TestInit(unittest.TestCase):
    #Make sure we can load a valid configuration
    def test_read_json(self):
        '''Make sure we can load the music data json file'''
        music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR)
        self.assertIsInstance(music_release, MusicRelease)
        self.assertEqual(music_release.metadata[0]["title"], "Test")

class TestWithFiles(unittest.TestCase):
    music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR)

    #Helper functions
    def assertIsFile(self, path):
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    #Prep & cleanup
    @classmethod
    def setUpClass(self):
        os.makedirs(TESTING_DIR)
    
    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test")

    #Tests
    def test_make_mp3(self):
        #Create the file
        fname = "Test.wav"
        src_path = pathlib.Path(CONTENT_DIR, fname)
        dest_path = pathlib.Path(TESTING_DIR, fname[:-3] + "mp3")
        create_mp3(src_path, self.music_release.metadata[0], dest_path=dest_path)
        self.assertIsFile(dest_path)

        #Test tag data
        audio = EasyID3(dest_path)
        self.assertEqual(audio["title"], ["Test"])
        tags = ["artist", "website", "genre", "album"]
        for tag in tags:
            self.assertEqual(audio[tag], [self.music_release.metadata[0]["mp3"][tag]])

    #@unittest.skip("Too verbose")
    def test_make_mp4(self):
        #Create the file
        fname = "Test.wav"
        src_path = pathlib.Path(CONTENT_DIR, fname)
        dest_path = pathlib.Path(TESTING_DIR, fname[:-3] + "mp4")
        cover = pathlib.Path(CONTENT_DIR, "Cover.png")
        create_mp4(src_path, dest_path, cover)
        self.assertIsFile(dest_path)

    def test_make_webp(self):
        #Create the file
        fname = "Cover.png"
        dest_path = pathlib.Path(TESTING_DIR, self.music_release.metadata[0]["cover"])
        cover = pathlib.Path(CONTENT_DIR, "Cover.png")
        create_webp(cover, dest_path)
        self.assertIsFile(dest_path)

    def test_zip_stems(self):
        src = pathlib.Path(CONTENT_DIR, "Stems/")
        target = pathlib.Path(TESTING_DIR, "Stems.zip")
        create_zip(src, str(target)[:-4]) #shutil.make_archive() doesn't need .zip
        self.assertIsFile(target)

class TestServices(unittest.TestCase):
    def test_youtube(self):
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH, CONTENT_DIR)
        #Don't upload if there's already an ID, if this fails check config for embed
        self.assertFalse(services.youtube.upload(None, music_release.metadata[0]))

if __name__ == "__main__":
    unittest.main()