import pytest
from unittest.mock import patch, Mock
from database.repositories.conversation import Conversation
from exceptions.database import UserDoesNotExist, RelatedRecordDoesNotExist
from tests.database.repositories.base import TestRepositoryBase


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
        self.raw_conversation_list = [self.raw_conversation, ]
        self.serialized_conversation_list = [self.serialized_conversation, ]
        with patch('psycopg2.connect') as mock_connect:
            mock_connection = Mock()
            mock_connection.commit = Mock()
            mock_connect.return_value = mock_connection
            self.db = Conversation()
            self.db.conn = mock_connection

    def test_private_serialize_successful(self):
        method_result = self.db._serialize(self.raw_conversation)
        assert method_result == self.serialized_conversation

    def test_private_serialize_raises_value_error(self):
        with pytest.raises(ValueError):
            self.db._serialize((None,))

    def test_private_get_user_id_successful(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = (self.user_id,)
            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection
            with patch('services.database.user.get_user_id_by_telegram_id') as mock_get_user_id:
                mock_get_user_id = Mock()
                mock_get_user_id.return_value = self.user_id
            method_result = self.db._get_user_id(self.telegram_id)
            assert method_result == self.user_id

    def test_private_get_user_id_raises_related_record_does_not_exist(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = None
            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection
            with patch('services.database.user.get_user_id_by_telegram_id') as mock_get_user_id:
                mock_get_user_id.side_effect = UserDoesNotExist("User does not exist")

                with pytest.raises(RelatedRecordDoesNotExist):
                    self.db._get_user_id(self.telegram_id)

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

    def test_delete_all_conversations_successful(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = (self.user_id,)

            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection

            self.db.delete_all_conversations(self.telegram_id)
            self.db.conn.close.assert_called_once()
            assert self.db.conn.commit.call_count == 2

    def test_get_raw_conversation_list_successful(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_cursor.fetchone.return_value = (self.user_id,)

            mock_connection = Mock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_connection
            self._setup_mock_cursor(return_value=self.raw_conversation_list, method_name="fetchall")
            method_result = self.db.get_raw_conversation_list(self.telegram_id)
            assert method_result == self.raw_conversation_list
            self.db.conn.cursor().fetchall.assert_called_once()
            self.db.conn.close.assert_called_once()

    def test_get_get_serialized_conversation_list_successful(self):
        self.db.get_raw_conversation_list = Mock()
        self.db.get_raw_conversation_list.call_args = (self.telegram_id,)
        self.db.get_raw_conversation_list.return_value = self.raw_conversation_list
        method_result = self.db.get_serialized_conversation_list(self.telegram_id)
        assert method_result == self.serialized_conversation_list
