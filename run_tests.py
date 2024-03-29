import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/tests")

from tests.test_utils import (
    TestFormatDateTime,
    TestGetSingleUser,
)


if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestFormatDateTime))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestGetSingleUser))

    unittest.TextTestRunner(verbosity=2).run(test_suite)
