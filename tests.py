import unittest
from musicuploader import *
import os
import pathlib
import shutil
from mutagen.easyid3 import EasyID3

TESTING_DIR = "./test/testing"
TESTS_DIR = "./tests"
TEST_JSON_PATH = "tests/release_example.json"

#ASSUMPTIONS
# Files in tests forlder: Cover.png and *.wav 
# Test does not cover albums yet

#Move to class itself
class TestInit(unittest.TestCase):
    #Make sure we can load a valid configuration
    def test_read_json(self):
        '''Make sure we can load the music data json file'''
        music_release = MusicRelease(TEST_JSON_PATH)
        self.assertIsInstance(music_release, MusicRelease)
        self.assertEqual(music_release.metadata[0]["title"], "Test")

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
        '''Should create an .mp3 file with appropriate tags'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH)
        #Create the file
        dest_path = pathlib.Path(TESTING_DIR, "Test.mp3")
        music_release.create_mp3(dest_path=dest_path)
        self.assertIsFile(dest_path)

        #Test tag data
        audio = EasyID3(dest_path)
        self.assertEqual(audio["title"], music_release.metadata[0]["title"])
        tags = ["artist", "website", "genre", "album"]
        for tag in tags:
            self.assertEqual(audio[tag], [music_release.metadata[0]["mp3"][tag]])

    #@unittest.skip("Too verbose")
    def test_make_mp4(self):
        '''Should create an .mp4'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH)
        #Create the file
        dest_path = pathlib.Path(TESTING_DIR, "Test.mp4")
        music_release.create_mp4(dest_path)
        self.assertIsFile(dest_path)

    def test_make_webp(self):
        '''Should create a webp from a provided image'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH)
        #Create the file
        dest_path = pathlib.Path(TESTING_DIR, music_release[0]["cover"])
        cover = pathlib.Path(TESTS_DIR, "Cover.png")
        music_release.create_webp(cover)
        self.assertIsFile(dest_path)

    def test_zip_stems(self):
        '''Should produce a .zip of the Stems folder'''
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH)
        #Make .zip
        src = pathlib.Path(TESTS_DIR, "Source/Stems/")
        target = pathlib.Path(TESTING_DIR, "Stems.zip")
        music_release.create_zip(src, str(target)[:-4]) #shutil.make_archive() doesn't need .zip
        self.assertIsFile(target)

class TestServices(unittest.TestCase):
    def test_youtube(self):
        #Initialize the class
        music_release = MusicRelease(TEST_JSON_PATH)
        #Don't upload if there's already an ID, if this fails check config for embed
        self.assertFalse(services.youtube.upload(None, music_release.metadata[0]))

if __name__ == "__main__":
    unittest.main()