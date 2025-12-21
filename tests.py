import unittest
from musicuploader import *
import os
import pathlib

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
        os.makedirs("test/testing")
    
    @classmethod
    def tearDownClass(self):
        os.removedirs("test/testing")

    #Tests
    def test_make_mp3(self):
        fname = "Chill Shop (Loop).mp3"
        self.assertIsFile(pathlib.Path("test/testing/" + fname))

if __name__ == "__main__":
    unittest.main()