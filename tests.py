import unittest
from musicuploader import *
import os
import pathlib
import shutil
from mutagen.easyid3 import EasyID3

TESTING_DIR = "./test/testing"
TESTS_DIR = "./tests"
JSON = read_json("release_example.json")

#ASSUMPTIONS
# Files in tests forlder: Cover.png and *.wav 
class TestInit(unittest.TestCase):
    #Make sure we can load a valid configuration
    def test_read_json(self):
        '''Make sure we're working with valid data'''
        results = read_json("release_example.json")
        self.assertEqual(results["title"], "Test")

class TestWithFiles(unittest.TestCase):
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
        fname = "Chill Shop (Loop).wav"
        src_path = pathlib.Path(TESTS_DIR, fname)
        dest_path = pathlib.Path(TESTING_DIR, fname[:-3] + "mp3")
        create_mp3(src_path, JSON, dest_path=dest_path)
        self.assertIsFile(dest_path)

        #Test tag data
        audio = EasyID3(dest_path)
        self.assertEqual(audio["title"], ["Test"])
        tags = ["artist", "website", "genre", "album"]
        for tag in tags:
            self.assertEqual(audio[tag], [JSON["mp3"][tag]])

    #@unittest.skip("Too verbose")
    def test_make_mp4(self):
        #Create the file
        fname = "Chill Shop (Loop).wav"
        src_path = pathlib.Path(TESTS_DIR, fname)
        dest_path = pathlib.Path(TESTING_DIR, fname[:-3] + "mp4")
        cover = pathlib.Path(TESTS_DIR, "Cover.png")
        create_mp4(src_path, dest_path, cover)
        self.assertIsFile(dest_path)

    def test_make_webp(self):
        #Create the file
        fname = "Cover.png"
        dest_path = pathlib.Path(TESTING_DIR, JSON["cover"])
        cover = pathlib.Path(TESTS_DIR, "Cover.png")
        create_webp(cover, dest_path)
        self.assertIsFile(dest_path)

    def test_zip_stems(self):
        src = pathlib.Path(TESTS_DIR, "Stems/")
        target = pathlib.Path(TESTING_DIR, "Stems.zip")
        create_zip(src, str(target)[:-4]) #shutil.make_archive() doesn't need .zip
        self.assertIsFile(target)

class TestServices(unittest.TestCase):
    def test_youtube(self):
        #Don't upload if there's already an ID, if this fails check config for embed
        self.assertFalse(services.youtube.upload(None, JSON))

if __name__ == "__main__":
    unittest.main()