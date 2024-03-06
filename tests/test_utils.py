import unittest
import datetime
from services.utils import (
    format_datetime,
    get_single_user,
    get_language_of_single_user,
)


class TestFormatDateTime(unittest.TestCase):

    def test_valid_datetime_format(self):
        input = "2022-12-31 23:59:59.123456"
        expected_return = "23:59:59 31.12.2022"
        self.assertEqual(format_datetime(input), expected_return)

    def test_invalid_datetime_format(self):
        input = "2022/12/31 23:59:59"
        with self.assertRaises(ValueError):
            format_datetime(input)

    def test_empty_input(self):
        input = ""
        self.assertIsNone(format_datetime(input))


class TestGetSingleUser(unittest.TestCase):

    def test_user_data_extraction(self):
        telegram_id = 957481488
        expected_return = {
            "user_id": 2,
            "telegram_id": 957481488,
            "username": "javoxirone",
            "first_name": "Javohir",
            "last_name": "Nurmatjonov",
            "created_at": datetime.datetime(2024, 3, 2, 15, 29, 14, 574722),
            "language": "en",
        }
        self.assertDictEqual(get_single_user(telegram_id), expected_return)


class TestGetLanguageOfSingleUser(unittest.TestCase):
    def test_extraction_of_language_of_single_user(self):
        telegram_id = 957481488
        expected_return_types = (
            "en",
            "ru",
            "uz",
        )
        self.assertIn(get_language_of_single_user(telegram_id), expected_return_types)


if __name__ == "__main__":
    unittest.main()
