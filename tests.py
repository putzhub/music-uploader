import unittest
from musicuploader import *

class TestInit(unittest.TestCase):
    def test_read_json(self):
        '''Make sure we're working with valid data'''
        results = read_json("release_example.json")
        self.assertEqual(results["title"], "Roguelike Adventure Music Pack")
        self.assertEqual(results["date"], datetime.datetime(2025, 12, 20))

if __name__ == "__main__":
    unittest.main()