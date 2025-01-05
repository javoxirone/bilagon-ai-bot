from typing import NoReturn

import pytest
from unittest.mock import patch, Mock
from psycopg2 import DataError, IntegrityError
from database.repositories.user import User
from exceptions.database import NoRecordsFound, UserDoesNotExist, DataTypeError, UserAlreadyExistsError
from tests.database.repositories.base import TestRepositoryBase


class TestUser(TestRepositoryBase):
    def setup_method(self):
        self.db: any = None
        self.user_id: int = 1
        self.telegram_id = 957481488
        self.raw_user_data: tuple[any, ...] = (1,
                                               957481488,
                                               'javoxirone',
                                               'Javohir',
                                               'Nurmatjonov',
                                               '2024-12-04 19:07:22.795534',
                                               'en',)
        self.serialized_user_data: dict[str, any] = {
            'user_id': 1,
            'telegram_id': 957481488,
            'username': 'javoxirone',
            'first_name': 'Javohir',
            'last_name': 'Nurmatjonov',
            'created_at': '2024-12-04 19:07:22.795534',
            'language': 'en'
        }
        self.raw_user_list: list[tuple[any, ...]] = [self.raw_user_data, ]
        self.serialized_user_list: list[dict[str, any]] = [self.serialized_user_data, ]
        with patch('psycopg2.connect') as mock_connect:
            mock_connection: Mock = Mock()
            mock_connection.commit = Mock()
            mock_connect.return_value = mock_connection
            self.db: User = User()
            self.db.conn = mock_connection

    def test_serialize_successful(self) -> NoReturn:
        method_result = self.db._serialize(self.raw_user_data)
        assert method_result == self.serialized_user_data

    def test_serialize_raises_value_error_for_invalid_data(self) -> NoReturn:
        with pytest.raises(ValueError):
            self.db._serialize((None,))

    def test_get_raw_user_list_successful(self) -> NoReturn:
        mocked_fetchall = self._setup_mock_cursor(return_value=self.raw_user_list, method_name="fetchall")
        method_result = self.db.get_raw_user_list()
        assert method_result == self.raw_user_list
        mocked_fetchall.assert_called_once()
        self.db.conn.cursor().fetchall.assert_called_once()
        self.db.conn.close.assert_called_once()

    def test_get_raw_user_list_raises_no_records_found(self) -> NoReturn:
        mocked_fetchall = self._setup_mock_cursor(return_value=[], method_name="fetchall")
        with pytest.raises(NoRecordsFound):
            self.db.get_raw_user_list()
        mocked_fetchall.assert_called_once()
        self.db.conn.cursor().fetchall.assert_called_once()
        self.db.conn.close.assert_called_once()

    def test_get_serialized_user_list_successful(self) -> NoReturn:
        self.db.get_raw_user_list = Mock()
        self.db.get_raw_user_list.return_value = self.raw_user_list
        self.db._serialize = Mock()
        self.db._serialize.return_value = self.serialized_user_data
        method_result = self.db.get_serialized_user_list()
        assert method_result == self.serialized_user_list

    def test_get_serialized_user_list_no_records(self) -> NoReturn:
        with patch('database.repositories.user.User.get_raw_user_list') as mock_get_raw_user_list:
            mock_get_raw_user_list.side_effect = NoRecordsFound("There is no any users on the database")
            method_result = self.db.get_serialized_user_list()
            self.db._serialize = Mock()
            assert method_result == []
            assert self.db._serialize.call_count == 0

    def test_get_raw_user_successful(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(return_value=self.raw_user_data, method_name="fetchone")
        method_result = self.db.get_raw_user(self.telegram_id)
        assert method_result == self.raw_user_data
        mocked_fetchone.assert_called_once()
        self.db.conn.cursor().fetchone.assert_called_once()
        self.db.conn.close.assert_called_once()

    def test_get_raw_user_raises_no_records_found(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(return_value=None, method_name="fetchone")
        with pytest.raises(UserDoesNotExist):
            self.db.get_raw_user(self.telegram_id)
        mocked_fetchone.assert_called_once()
        self.db.conn.cursor().fetchone.assert_called_once()
        self.db.conn.close.assert_called_once()

    def test_get_serialized_user_successful(self) -> NoReturn:
        self.db.get_raw_user = Mock()
        self.db.get_raw_user.return_value = self.raw_user_data
        self.db._serialize = Mock()
        self.db._serialize.return_value = self.serialized_user_data
        method_result = self.db.get_serialized_user(self.telegram_id)
        assert method_result == self.serialized_user_data

    def test_get_serialized_user_not_found(self) -> NoReturn:
        with patch('database.repositories.user.User.get_raw_user') as mock_get_raw_user:
            mock_get_raw_user.side_effect = UserDoesNotExist(f"Provided telegram_id is {self.telegram_id}")
            with pytest.raises(UserDoesNotExist):
                self.db.get_serialized_user(self.telegram_id)

    def test_get_user_id_successful(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(return_value=(self.user_id,), method_name="fetchone")
        method_result = self.db.get_user_id(self.telegram_id)
        assert method_result == self.user_id
        mocked_fetchone.assert_called_once()
        self.db.conn.cursor().fetchone.assert_called_once()

    def test_add_user_successful(self) -> NoReturn:
        mocked_cursor = self._setup_mock_cursor(method_name="execute")
        self.db.add_user(self.telegram_id, "javoxirone", "Javohir", "Nurmatjonov", "en")
        self.db.conn.close.assert_called_once()

    def test_add_user_integrity_error(self) -> NoReturn:
        mocked_cursor = self._setup_mock_cursor(method_name="execute")
        mocked_cursor.side_effect = IntegrityError()
        with pytest.raises(UserAlreadyExistsError):
            self.db.add_user(self.telegram_id, "javoxirone", "Javohir", "Nurmatjonov", "en")

    def test_add_user_data_error(self) -> NoReturn:
        mocked_cursor = self._setup_mock_cursor(method_name="execute")
        mocked_cursor.side_effect = DataError()
        with pytest.raises(DataTypeError):
            self.db.add_user(self.telegram_id, "javoxirone", "Javohir", "Nurmatjonov", "en")

    def test_user_exists_successful(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(return_value=(1,), method_name="fetchone")
        result = self.db.user_exists(self.telegram_id)
        assert result is True
        self.db.conn.close.assert_called_once()

    def test_user_exists_not_found(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(return_value=(0,), method_name="fetchone")
        result = self.db.user_exists(self.telegram_id)
        assert result is False
        self.db.conn.close.assert_called_once()

    def test_user_exists_data_error(self) -> NoReturn:
        mocked_fetchone = self._setup_mock_cursor(method_name="fetchone")
        mocked_fetchone.side_effect = DataError()
        with pytest.raises(DataTypeError):
            self.db.user_exists(self.telegram_id)

    def test_update_user_language_successful(self) -> NoReturn:
        self.db.user_exists = Mock(return_value=True)
        mocked_cursor = self._setup_mock_cursor(method_name="execute")
        self.db.update_user_language(self.telegram_id, "uz")
        self.db.user_exists.assert_called_once_with(self.telegram_id)
        self.db.conn.close.assert_called_once()

    def test_update_user_language_user_does_not_exist(self) -> NoReturn:
        self.db.user_exists = Mock(return_value=False)
        with pytest.raises(UserDoesNotExist):
            self.db.update_user_language(self.telegram_id, "uz")
        self.db.user_exists.assert_called_once_with(self.telegram_id)

    def test_update_user_language_data_error(self) -> NoReturn:
        self.db.user_exists = Mock(return_value=True)
        mocked_cursor = self._setup_mock_cursor(method_name="execute")
        mocked_cursor.side_effect = DataError()
        with pytest.raises(DataTypeError):
            self.db.update_user_language(self.telegram_id, "uz")

        self.db.user_exists.assert_called_once_with(self.telegram_id)
