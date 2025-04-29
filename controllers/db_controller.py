from typing import Optional, List, Tuple, Any, Dict
from models.db_connection import DBConnection

class DatabaseController:
    def __init__(self, db_config: Dict[str, str], min_conn: int = 1, max_conn: int = 10):
        """
        Initialize the database controller with connection configuration
        Args:
            db_config: Dictionary containing database connection parameters
            min_conn: Minimum number of connections in the pool
            max_conn: Maximum number of connections in the pool
        """
        self.db = DBConnection(db_config, min_conn, max_conn)

    def create_table(self, table_name: str, columns: List[str]) -> bool:
        """
        Create a new table in the database
        Args:
            table_name: Name of the table to create
            columns: List of column definitions
        Returns:
            bool: True if successful, False otherwise
        """
        query = f"CREATE TABLE {table_name} ({', '.join(columns)})"
        result = self.db.execute_query(query)
        return result is not None

    def insert_data(self, table_name: str, columns: List[str], values: Tuple) -> bool:
        """
        Insert data into a table
        Args:
            table_name: Target table name
            columns: List of column names
            values: Tuple of values to insert
        Returns:
            bool: True if successful, False otherwise
        """
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        result = self.db.execute_query(query, values)
        return result is not None

    def select_data(self, table_name: str, columns: List[str] = None, 
                   where_clause: str = None, params: Tuple = None) -> Optional[List[Tuple[Any, ...]]]:
        """
        Select data from a table
        Args:
            table_name: Target table name
            columns: List of columns to select (None for all columns)
            where_clause: Optional WHERE clause
            params: Parameters for WHERE clause
        Returns:
            List of tuples containing the query results
        """
        cols = '*' if columns is None else ', '.join(columns)
        query = f"SELECT {cols} FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return self.db.execute_query(query, params)

    def update_data(self, table_name: str, set_values: Dict[str, Any], 
                   where_clause: str, params: Tuple) -> bool:
        """
        Update data in a table
        Args:
            table_name: Target table name
            set_values: Dictionary of column-value pairs to update
            where_clause: WHERE clause for the update
            params: Parameters for WHERE clause
        Returns:
            bool: True if successful, False otherwise
        """
        set_clause = ', '.join([f"{k} = %s" for k in set_values.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        values = tuple(set_values.values()) + params
        result = self.db.execute_query(query, values)
        return result is not None

    def delete_data(self, table_name: str, where_clause: str, params: Tuple) -> bool:
        """
        Delete data from a table
        Args:
            table_name: Target table name
            where_clause: WHERE clause for deletion
            params: Parameters for WHERE clause
        Returns:
            bool: True if successful, False otherwise
        """
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        result = self.db.execute_query(query, params)
        return result is not None

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database
        Args:
            table_name: Name of the table to check
        Returns:
            bool: True if table exists, False otherwise
        """
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            )
        """
        result = self.db.execute_query(query, (table_name,))
        return result[0][0] if result else False

    def close_connections(self):
        """
        Close all database connections in the pool
        """
        self.db.close_pool()