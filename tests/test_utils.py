import unittest
from services.utils import format_datetime

class TestFormatDateTime(unittest.TestCase):

    def test_valid_datetime_format(self):
        input = "2022-12-31 23:59:59.123456"
        expected_output = "23:59:59 31.12.2022"
        self.assertEqual(format_datetime(input), expected_output)

    def test_invalid_datetime_format(self):
        input = "2022/12/31 23:59:59"
        with self.assertRaises(ValueError):
            format_datetime(input)

    def test_empty_input(self):
        input = ""
        self.assertIsNone(format_datetime(input))


if __name__ == '__main__':
    unittest.main()