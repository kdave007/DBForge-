# models/database_connection.py
import psycopg2
from psycopg2 import pool
from typing import Dict, Optional
from contextlib import contextmanager

class DBConnection:
    _instance = None
    _pool = None

    def __new__(cls, db_config: Dict[str, str], min_conn: int = 1, max_conn: int = 10):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.db_config = db_config
            cls._instance.min_conn = min_conn
            cls._instance.max_conn = max_conn
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        """
        Initialize the connection pool
        """
        try:
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.min_conn,
                maxconn=self.max_conn,
                **self.db_config
            )
            print("Database pool initialized successfully")
        except Exception as e:
            print(f"Error initializing connection pool: {e}")
            self._pool = None

    @contextmanager
    def get_connection(self):
        """
        Get a connection from the pool using context manager
        Usage:
            with db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
        """
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        finally:
            if conn:
                self._pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a SQL query
        Args:
            query: SQL query string
            params: Optional tuple of parameters
        Returns:
            Query results if SELECT, otherwise number of affected rows
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query, params)
                    if query.strip().upper().startswith('SELECT'):
                        return cur.fetchall()
                    else:
                        conn.commit()
                        return cur.rowcount
                except Exception as e:
                    conn.rollback()
                    raise e

    def close_pool(self):
        """
        Close all connections in the pool
        """
        if self._pool:
            self._pool.closeall()
            print("All database connections closed")