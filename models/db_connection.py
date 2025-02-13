import psycopg2
from psycopg2 import pool, errors
from contextlib import contextmanager
from typing import Dict, Optional, Tuple, List, Any

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
        except psycopg2.OperationalError as e:
            print(f"Connection refused: Check your database credentials. Error: {e}")
            self._pool = None
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
        if self._pool is None:
            raise ConnectionError("Database connection pool is not initialized. Check your credentials or database configuration.")

        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Failed to get a connection from the pool: {e}")
        finally:
            if conn:
                self._pool.putconn(conn)

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> Optional[List[Tuple[Any, ...]]]:
        """
        Execute a SQL query
        Args:
            query: SQL query string
            params: Optional tuple of parameters
        Returns:
            Query results if SELECT, otherwise number of affected rows
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    try:
                        cur.execute(query, params)
                        if query.strip().upper().startswith('SELECT'):
                            return cur.fetchall()
                        else:
                            conn.commit()
                            return cur.rowcount
                    except errors.DuplicateTable as e:
                        # Handle duplicate table error
                        conn.rollback()
                        print(f"Error: Table already exists. Details: {e}")
                        return None
                    except errors.UniqueViolation as e:
                        # Handle unique constraint violation
                        conn.rollback()
                        print(f"Error: Unique constraint violation. Details: {e}")
                        return None
                    except errors.ProgrammingError as e:
                        # Handle SQL syntax errors or invalid queries
                        conn.rollback()
                        print(f"Error: Invalid SQL query. Details: {e}")
                        return None
                    except errors.Error as e:
                        # Handle all other PostgreSQL errors
                        conn.rollback()
                        print(f"Database error: {e}")
                        return None
                    except Exception as e:
                        # Handle any other unexpected errors
                        conn.rollback()
                        print(f"Unexpected error: {e}")
                        return None
        except ConnectionError as e:
            print(f"Database connection error: {e}")
            return None

    def close_pool(self):
        """
        Close all connections in the pool
        """
        if self._pool:
            self._pool.closeall()
            print("All database connections closed")