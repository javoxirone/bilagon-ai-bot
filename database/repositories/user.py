from typing import NoReturn
from data_types.db import UserDataType
from database.base import Database
from psycopg2.extensions import cursor as CursorType
from psycopg2 import (
    IntegrityError,
    OperationalError,
    DataError,
)
from exceptions.database import (
    UserAlreadyExistsError,
    DBError,
    DataTypeError, UserDoesNotExist,
)


class User(Database):
    """
    Represents a user management system interfacing with a database to perform
    standard operations such as adding, updating, and retrieving user information.
    This class extends the Database class to leverage database connection and
    transaction functionalities for managing user data records.

    :ivar db_name: Name of the database being connected to.
    :type db_name: str
    :ivar conn: Parameters required to establish a database connection.
    :type conn: dict
    """

    def __init__(self):
        super().__init__()

    def _serialize(self, user_data_raw: tuple[any, ...]) -> UserDataType:
        """
        Converts a tuple of raw user data into a dictionary format suitable
        for further processing. This method extracts specific user details
        from the incoming tuple and constructs a dictionary with predefined
        keys corresponding to each piece of user data.

        This conversion operation helps organize user data systematically,
        making it efficient to access and manipulate individual user attributes
        based on their keys. In case of invalid input types or insufficient data,
        meaningful exceptions are raised to indicate input errors.

        :param user_data_raw: A tuple containing user data fields in a specific order
        :type user_data_raw: tuple[any, ...]

        :return: A dictionary representation of the user data with defined keys
        :rtype: UserDataType
        """
        try:
            user_id: int = user_data_raw[0]
            telegram_id: int = user_data_raw[1]
            username: str = user_data_raw[2]
            first_name: str = user_data_raw[3]
            last_name: str = user_data_raw[4]
            created_at: str = user_data_raw[5]
            language: str = user_data_raw[6]

            return {
                "user_id": user_id,
                "telegram_id": telegram_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": created_at,
                "language": language
            }
        except IndexError as e:
            raise ValueError("User data raw tuple does not contain the required number of elements") from e
        except TypeError as e:
            raise ValueError("Invalid data type encountered while processing user data") from e

    def get_user_list(self) -> list[UserDataType]:
        """
        Retrieves a list of users from the database. The users are fetched from the
        'users' table and the raw data is transformed into a list of dictionaries,
        each representing a user with specific fields.

        The function attempts to establish a database session and execute an SQL
        query to fetch all records from the 'users' table. Each record is then
        serialized into a dictionary format suitable for further processing or
        usage. If the users list is empty, an empty list is returned. In the event
        of database operation errors, specific exceptions are raised to indicate
        the type of failure encountered.

        :return: A list of dictionaries, each containing user data from the database.
        :rtype: list[UserDataType]

        :raises DBError: If there is an error establishing a database connection
                         or executing the database operation.
        :raises DataTypeError: If there is an error related to data types
                                     during data retrieval or processing.
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users')
                user_list_raw: list[tuple[any, ...]] = cursor.fetchall()
                user_list_serialized: list[UserDataType] = []

                if not user_list_raw:
                    return []

                for user_data_raw in user_list_raw:
                    user_data_serialized: UserDataType = self._serialize(user_data_raw)
                    user_list_serialized.append(user_data_serialized)

                return user_list_serialized
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()

    def get_user(self, telegram_id: int) -> UserDataType:
        """
        Retrieve user information from the database using the given telegram ID.

        This method queries the database for a user with the specified telegram ID.
        If the user is found, their data is returned in a dictionary format.
        If the user does not exist or any database errors occur during the process,
        appropriate exceptions are raised.

        :param telegram_id: Unique identifier for the user in the telegram system
        :type telegram_id: int
        :return: A dictionary containing user information if found
        :rtype: UserDataType
        :raises UserDoesNotExist: If no user is found with the provided telegram ID
        :raises DBError: If an operational error occurs within the database
        :raises DataTypeError: If a data error occurs while inserting the data type

        Examples:
            >>> db = User()
            >>> db.get_user(123456789)
            {
                "user_id": 1,
                "telegram_id": 123456789,
                "username": "john_smith",
                "first_name": "John",
                "last_name": "Smith",
                "created_at": "2023-03-15T12:34:56",
                "language": "en"
            }
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('SELECT * FROM users WHERE telegram_id = %s', (telegram_id,))
                user_data_raw = cursor.fetchone()
                if not user_data_raw:
                    raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
                user_data_serialized: UserDataType = self._serialize(user_data_raw)
                return user_data_serialized
        except OperationalError:
            raise DBError(f"Database operational error occurred while getting a user, telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Data type error occurred because of wrong data type used while fetching a user, telegram_id is {telegram_id}")

    def get_user_id(self, telegram_id: int) -> int:
        """
        Retrieves the user ID associated with the given Telegram ID. Uses a database
        session to execute the query. Handles specific database errors that may
        occur during the operation, including operational and data type errors.
        If the user ID does not exist for the provided Telegram ID, a custom error
        is raised.

        :param telegram_id: The Telegram ID of the user whose user ID is to be retrieved.
        :return: The user ID associated with the given Telegram ID.
        :raises UserDoesNotExist: If no user ID exists for the provided Telegram ID.
        :raises DBError: If a database operational error occurs.
        :raises DataTypeError: If a data type error occurs during the query.
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE telegram_id = %s", (telegram_id,))
                user_id = cursor.fetchone()
                if not user_id:
                    raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
                return user_id[0]
        except OperationalError:
            raise DBError(f"Database operational error occurred while getting a user id, telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError(
                f"Data type error occurred because of wrong data type used while fetching a user id, telegram_id is {telegram_id}")

    def add_user(self, telegram_id: int, username: str, first_name: str, last_name: str, language: str) -> NoReturn:
        """
        Adds a new user to the database with the provided details. The operation
        will attempt to insert a new record into the 'users' table. If the
        insertion leads to a data integrity violation, e.g., duplicate telegram_id,
        a UserAlreadyExistsError is raised. This method performs database rollback
        in case of any errors to maintain database consistency.

        :param telegram_id: The unique identifier for the user in Telegram.
        :type telegram_id: int
        :param username: The username of the user.
        :type username: str
        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param language: The preferred language of the user.
        :type language: str
        :raises UserAlreadyExistsError: If a user with the given telegram_id already exists.
        :raises DataTypeError: If there is an issue with the data type during insertion.
        :raises DBError: For any general operational errors encountered during the insertion.

        Examples:
            >>> db = User()
            >>> db.add_user(123456789, "john_smith", "John", "Smith", "en")
            None
        """

        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                            INSERT INTO users (
                                telegram_id,
                                username,
                                first_name,
                                last_name,
                                language
                            )
                            VALUES (%s, %s, %s, %s, %s);
                        ''', (telegram_id,
                              username,
                              first_name,
                              last_name,
                              language,))
                db_session.conn.commit()
        except IntegrityError:
            raise UserAlreadyExistsError(f"Provided telegram_id is {telegram_id}")
        except DataError:
            raise DataTypeError()
        except OperationalError:
            raise DBError()

    def user_exists(self, telegram_id: int) -> bool:
        """
        Determines whether a user with a given Telegram ID exists within
        the database. This method executes a query to check the presence
        of the user and returns a boolean result based on the count.

        :param telegram_id: The unique identifier for a Telegram user.
        :type telegram_id: int
        :return: True if the user exists, otherwise False.
        :rtype: bool
        :raises DBError: If there is an operational error during database
                         communication.
        :raises DataTypeError: If there is an issue with the data
                                     type during the insert operation.

        Examples:
            >>> db = User()
            >>> db.user_exists(123456789)
            True

            >>> db = User()
            >>> db.user_exists(987654321)
            False
        """
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM users
                    WHERE telegram_id = %s
                ''', (telegram_id,))
                count: int = cursor.fetchone()[0]
                return count > 0
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()

    def update_user_language(self, telegram_id: int, new_language: str) -> NoReturn:
        """
        Updates the language preference for a user in the database identified by
        their Telegram ID. The method ensures that the specified user exists and
        then attempts to update their language setting. If the user does not exist,
        a custom exception is raised. This operation might also raise exceptions
        related to database connectivity or data integrity issues.

        :param telegram_id: Unique identifier for the user in Telegram.
        :type telegram_id: int
        :param new_language: New language code to be set for the user.
        :type new_language: str
        :raises UserDoesNotExist: If no user is found with the provided telegram_id.
        :raises DBError: If there is an operational error while accessing the database.
        :raises DataTypeError: If there is an issue with the data type being inserted.
        :return: None
        """
        if not self.user_exists(telegram_id):
            raise UserDoesNotExist(f"Provided telegram_id is {telegram_id}")
        try:
            with self as db_session:
                cursor: CursorType = db_session.conn.cursor()
                cursor.execute('UPDATE users SET language = %s WHERE telegram_id = %s',
                               (new_language, telegram_id))
                db_session.conn.commit()
        except OperationalError:
            raise DBError()
        except DataError:
            raise DataTypeError()
