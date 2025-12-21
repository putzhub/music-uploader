import unittest
from musicuploader import *
import os
import pathlib
import shutil

testing_dir = "./test/testing"
tests_dir = "./tests"

class TestInit(unittest.TestCase):
    def test_read_json(self):
        '''Make sure we're working with valid data'''
        results = read_json("release_example.json")
        self.assertEqual(results["title"], "Roguelike Adventure Music Pack")
        self.assertEqual(results["date"], datetime.datetime(2025, 12, 20))

class TestPreProcessing(unittest.TestCase):
    #Helper functions
    def assertIsFile(self, path):
        if not pathlib.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))
    
    #Prep & cleanup
    @classmethod
    def setUpClass(self):
        os.makedirs(testing_dir)
    
    @classmethod
    def tearDownClass(self):
        shutil.rmtree("test")

    #Tests
    def test_make_mp3(self):
        fname = "Chill Shop (Loop).wav"
        src_path = pathlib.Path(tests_dir, fname)
        dest_path = pathlib.Path(testing_dir, fname[:-3] + "mp3")
        create_mp3(src_path, dest_path)
        self.assertIsFile(dest_path)

if __name__ == "__main__":
    unittest.main()