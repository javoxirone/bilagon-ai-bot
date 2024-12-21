import pytest
from unittest.mock import patch, Mock
from services.database.user import get_user_id_by_telegram_id


@patch('psycopg2.connect')
def test_get_user_id_by_telegram_id_successful(mock_connect):
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = (1,)

    mock_connection = Mock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    result = get_user_id_by_telegram_id(123456789)
    assert result == 1
