import pytest
from unittest.mock import Mock


class TestRepositoryBase:
    def setup_method(self):
        self.db = None
        self.user_id = 1
        self.telegram_id = 957481488

    def teardown_method(self, method):
        self.__dict__.clear()

    def _setup_mock_cursor(self, return_value=None, method_name="fetchall"):
        mock_cursor = Mock()
        setattr(mock_cursor, method_name, Mock(return_value=return_value))
        self.db.conn.cursor.return_value = mock_cursor
        return getattr(mock_cursor, method_name)
