import unittest
import os
import numpy as np

class TestImageDifferences(unittest.TestCase):
    def test_all_same(self):
        arr1 = np.zeros((64, 64, 3))
        arr2 = np.zeros((64, 64, 3))
        
        diff = arr1 - arr2

        self.assertTrue(np.all(diff == 0))
        
    def test_all_diff(self):
        arr1 = np.zeros((64, 64, 3))
        arr2 = np.ones((64, 64, 3))

        diff = arr1 - arr2

        self.assertFalse(np.all(diff == 0))

    def test_half_diff(self):
        arr1 = np.ones((64, 64, 3))

        arr2 = np.ones((64, 64, 3))
        arr2[0:32, 0:64, 0:3] = np.zeros((32, 64, 3))

        # Allowed difference
        epsilon = 0.4

        different = ((arr1 - arr2) >= epsilon).astype(int)
        diff_percentage = np.count_nonzero(different) / np.size(different)

        self.assertTrue(round(diff_percentage, 1) == 0.5, \
                        "Difference " + \
                        str(diff_percentage*100) + \
                        "% and should be 50%")


if __name__ == "__main__":
    unittest.main()

