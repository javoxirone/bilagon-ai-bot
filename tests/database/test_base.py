import os
import unittest
from unittest.mock import patch, MagicMock

from database.base import Database
from exceptions.database import RollbackError, CommitError


class TestDatabase(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_database_initialization(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        db = Database()

        self.assertIsNotNone(db.conn)
        mock_connect.assert_called_once_with(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

    @patch('psycopg2.connect')
    def test_context_manager_commit_successful(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        db = Database()

        with db:
            pass

        mock_connection.commit.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_context_manager_rollback_on_exception(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        db = Database()

        with self.assertRaises(Exception) as context:
            with db:
                raise Exception("Test exception")

        self.assertEqual(str(context.exception), "Test exception")
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch('psycopg2.connect')
    def test_context_manager_rollback_error_handling(self, mock_connect):
        mock_connection = MagicMock()
        mock_connection.rollback.side_effect = Exception("Rollback failed")
        mock_connect.return_value = mock_connection
        db = Database()

        with self.assertRaises(RollbackError):
            with db:
                raise Exception("simulate exception")

        mock_connection.close.assert_called()

    @patch('psycopg2.connect')
    def test_context_manager_commit_error_handling(self, mock_connect):
        mock_connection = MagicMock()
        mock_connection.commit.side_effect = Exception("Commit failed")
        mock_connect.return_value = mock_connection
        db = Database()

        with self.assertRaises(CommitError):
            with db:
                pass

        mock_connection.rollback.assert_called()
        mock_connection.close.assert_called()


if __name__ == '__main__':
    unittest.main()
