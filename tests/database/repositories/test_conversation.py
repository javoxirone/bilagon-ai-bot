import pytest
from unittest.mock import patch, Mock
from database.repositories.conversation import Conversation
from psycopg2 import DataError, IntegrityError

from database.repositories.user import User
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist
from services.database.user import get_user_id_by_telegram_id
from tests.database.repositories.base import TestRepositoryBase


def test_get_user_id_by_telegram_id_successful():
    with patch('psycopg2.connect') as mock_connect:
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)

        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        result = get_user_id_by_telegram_id(123456789)
        print(result)
        assert result == 1


class TestConversation(TestRepositoryBase):
    def setup_method(self):
        self.db = None
        self.user_id = 1
        self.telegram_id = 957481488
        self.raw_conversation = (
            'user',
            'Hello, how are you?'
        )
        self.serialized_conversation = {
            'role': 'user',
            'content': 'Hello, how are you?'
        }
        with patch('psycopg2.connect') as mock_connect:
            mock_connection = Mock()
            mock_connection.commit = Mock()
            mock_connect.return_value = mock_connection
            self.db = Conversation()
            self.db.conn = mock_connection

    def test_serialize_successful(self):
        method_result = self.db._serialize(self.raw_conversation)
        assert method_result == self.serialized_conversation

    def test_serialize_raises_value_error(self):
        with pytest.raises(ValueError):
            self.db._serialize((None,))

    def test_add_conversation_successful(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = (self.user_id,)

            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection

            self.db.add_conversation(self.telegram_id, 'user', "Hello, how are you?")
            self.db.conn.close.assert_called_once()
            assert self.db.conn.commit.call_count == 2

    def test_add_conversation_raises_related_record_does_not_exist(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = None

            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection
            with patch('services.database.user.get_user_id_by_telegram_id') as mock_get_user_id:
                mock_get_user_id.side_effect = UserDoesNotExist("User does not exist")

                with pytest.raises(RelatedRecordDoesNotExist):
                    self.db.add_conversation(self.telegram_id, 'user', "Hello, how are you?")
