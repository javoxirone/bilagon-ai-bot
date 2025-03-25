from typing import Union

from data_types.database import UserDataType
from database.base import Database
from psycopg2 import (
    IntegrityError,
    OperationalError,
    DataError,
)
from exceptions.database import (
    UserAlreadyExistsError,
    DBError,
    UserDoesNotExist, NoRecordsFound,
)


class User(Database):
    def __init__(self):
        """
        Initialize User repository.
        """
        super().__init__()

    def fetch_user_fields(
            self,
            telegram_ids: int | list[int] | None = None,
            fields: str | list[str] = None,
            filter_conditions: dict = None
    ) -> Union[list[dict], dict, any]:
        """
        Fetch specific field(s) for one or multiple users with advanced filtering.

        Args:
            telegram_ids (int | list[int] | None, optional):
                - Single Telegram ID
                - List of Telegram IDs
                - None to fetch for all users
            fields (str | list[str], optional):
                - Single field name
                - List of field names to retrieve
                - None to return all fields
            filter_conditions (dict, optional): Additional SQL WHERE conditions

        Returns:
            - Single value if one user, one field requested
            - Dictionary if one user, multiple fields requested
            - List of dictionaries for multiple users/all users

        Raises:
            ValueError: For invalid field names or filter conditions
            DBError: For database-related errors
        """
        # Define all possible fields
        all_fields = [
            'user_id', 'telegram_id', 'username', 'first_name',
            'last_name', 'created_at', 'language', 'saved_conversation_mode', 'model_name'
        ]

        # Normalize fields input
        if fields is None:
            fields = all_fields
        elif isinstance(fields, str):
            fields = [fields]

        # Validate requested fields
        invalid_fields = set(fields) - set(all_fields)
        if invalid_fields:
            raise ValueError(f"Invalid field(s) requested: {invalid_fields}")

        # Normalize telegram_ids input
        if telegram_ids is not None:
            if isinstance(telegram_ids, int):
                telegram_ids = [telegram_ids]

        try:
            # Construct base query
            field_list = ', '.join(fields)

            # Prepare WHERE conditions
            where_clauses = []
            query_params = []

            # Add telegram_id condition if specified
            if telegram_ids is not None:
                id_placeholders = ', '.join(['%s'] * len(telegram_ids))
                where_clauses.append(f"telegram_id IN ({id_placeholders})")
                query_params.extend(telegram_ids)

            # Add additional filter conditions
            if filter_conditions:
                for key, value in filter_conditions.items():
                    if key not in all_fields:
                        raise ValueError(f"Invalid filter field: {key}")

                    # Handle different types of conditions
                    if isinstance(value, (list, tuple)):
                        # IN clause for list of values
                        placeholders = ', '.join(['%s'] * len(value))
                        where_clauses.append(f"{key} IN ({placeholders})")
                        query_params.extend(value)
                    else:
                        # Simple equality
                        where_clauses.append(f"{key} = %s")
                        query_params.append(value)

            # Construct full query
            query = f"SELECT {field_list} FROM users"
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            # Execute query
            cursor = self.execute_query(query, tuple(query_params))
            results = cursor.fetchall()
            cursor.close()
            self.commit()

            # Process results
            processed_results = []
            for result in results:
                processed_results.append(dict(zip(fields, result)))

            # Return based on input
            if telegram_ids is not None and len(telegram_ids) == 1:
                # Single user case
                if len(fields) == 1:
                    # Single field for single user
                    return processed_results[0][fields[0]] if processed_results else None
                return processed_results[0] if processed_results else None

            return processed_results

        except Exception as e:
            self.rollback()
            raise DBError(f"Error fetching user fields: {str(e)}")

    def update_user_fields(
            self,
            telegram_id: int,
            update_fields: dict,
            validate_fields: bool = True
    ) -> None:
        """
        Update multiple fields for a specific user.

        Args:
            telegram_id (int): Telegram ID of the user to update
            update_fields (dict): Dictionary of fields to update
            validate_fields (bool, optional): Whether to validate field names. Defaults to True.

        Raises:
            UserDoesNotExist: If the user is not found
            ValueError: If invalid fields are provided
            DBError: For database-related errors
        """
        # Validate user existence
        if not self.user_exists(telegram_id):
            raise UserDoesNotExist(f"User with telegram_id {telegram_id} does not exist")

        # Define updatable fields (excluding user_id and created_at)
        updatable_fields = [
            'username', 'first_name', 'last_name',
            'language', 'saved_conversation_mode', 'model_name'
        ]

        # Validate fields if requested
        if validate_fields:
            invalid_fields = set(update_fields.keys()) - set(updatable_fields)
            if invalid_fields:
                raise ValueError(f"Invalid field(s) for update: {invalid_fields}")

        # Prepare update query
        try:
            # Construct update set clause
            update_clauses = []
            query_params = []

            for field, value in update_fields.items():
                update_clauses.append(f"{field} = %s")
                query_params.append(value)

            # Add telegram_id to parameters
            query_params.append(telegram_id)

            # Construct full query
            query = f"""
            UPDATE users 
            SET {', '.join(update_clauses)}
            WHERE telegram_id = %s
            """

            # Execute update
            cursor = self.execute_query(query, tuple(query_params))
            cursor.close()
            self.commit()

        except Exception as e:
            self.rollback()
            raise DBError(f"Error updating user fields: {str(e)}")

    def add_user(
            self,
            telegram_id: int,
            user_data: dict = None,
            ignore_existing: bool = False
    ) -> int:
        """
        Advanced method for adding a new user with flexible data input.

        :param telegram_id:  Telegram ID of the user.
        :type telegram_id: int

        :param user_data: Additional user information.
        :type user_data: dict

        :param ignore_existing: If True, update existing user instead of raising an error.
        :type ignore_existing: bool

        :returns: The user_id of the newly added or existing user.
        :rtype: int

        :raise UserAlreadyExistsError: If user exists and ignore_existing is False.
        :raise DBError: For database-related errors
        """
        # Prepare user data with defaults
        if user_data is None:
            user_data = {}

        # Extract known fields, use empty string or None as default
        username = user_data.get('username', '')
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        language = user_data.get('language', 'en')  # Default to English
        saved_conversation_mode = user_data.get('saved_conversation_mode', True)
        model_name = user_data.get('model_name', "gpt-4o-mini")

        # Check if user already exists
        try:
            if self.user_exists(telegram_id):
                if ignore_existing:
                    # Update existing user
                    update_fields = {k: v for k, v in user_data.items()
                                     if k in ['username', 'first_name', 'last_name', 'language',
                                              'saved_conversation_mode', 'model_name']}
                    self.update_user_fields(telegram_id, update_fields)

                    # Return existing user_id
                    return self.get_user_id(telegram_id)
                else:
                    raise UserAlreadyExistsError(f"User with telegram_id {telegram_id} already exists")

            # Prepare insert query with optional fields
            insert_fields = ['telegram_id', 'username', 'first_name', 'last_name', 'language',
                             'saved_conversation_mode', 'model_name']
            values = [telegram_id, username, first_name, last_name, language, saved_conversation_mode, model_name]

            # Construct query dynamically
            field_names = ', '.join(insert_fields)
            placeholders = ', '.join(['%s'] * len(values))

            query = f"""
            INSERT INTO users ({field_names})
            VALUES ({placeholders})
            RETURNING user_id
            """

            # Execute insert
            cursor = self.execute_query(query, tuple(values))
            new_user_id = cursor.fetchone()[0]
            cursor.close()
            self.commit()

            return new_user_id

        except Exception as e:
            self.rollback()
            raise DBError(f"Error adding user: {str(e)}")

    def user_exists(self, telegram_id: int) -> bool:
        """
        Check if a user exists by telegram ID.
        """
        try:
            cursor = self.execute_query(
                '''
                SELECT COUNT(*)
                FROM users
                WHERE telegram_id = %s
                ''',
                (telegram_id,)
            )
            count = cursor.fetchone()[0]
            cursor.close()
            self.commit()
            return count > 0
        except Exception as e:
            self.rollback()
            raise DBError(f"Error checking if user exists: {str(e)}")
