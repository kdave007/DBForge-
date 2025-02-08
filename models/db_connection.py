# models/database_connection.py
import psycopg2
from typing import Dict

class DBConnection:
    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize with database connection parameters
        """
        self.db_config = db_config
        self.connection = None

    def connect(self) -> bool:
        """
        Establish connection to PostgreSQL
        Returns:
            bool: True if connection succeeded, False otherwise
        """
        try:
            self.connection = psycopg2.connect(**self.db_config)
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a SQL query
        Args:
            query: SQL query string
            params: Optional tuple of parameters
        Returns:
            cursor: The database cursor if successful, None otherwise
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor
        except Exception as e:
            print(f"Query execution error: {e}")
            self.connection.rollback()
            return None

    def close(self):
        """
        Close the database connection
        """
        if self.connection:
            self.connection.close()