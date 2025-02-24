from dataclasses import dataclass
from typing import Optional

from controllers import SQLGeneratorController
from controllers.preview_controller import PreviewController
from controllers.db_controller import DBConnection
from controllers.dbf_controller import DBFController
from config import DB_CONFIG

@dataclass
class ProcessResult:
    success: bool
    message: str
    sql_query: Optional[str] = None
    preview_path: Optional[str] = None

class TableCreationController:
    def __init__(self):
        """Initialize models and other controllers"""
        self.sql_gen_controller = SQLGeneratorController()
        self.dbf_controller = DBFController()
        self.preview_controller = None
        self.db_connection = None

    def _get_db_connection(self) -> Optional[DBConnection]:
        """
        Get or create a database connection.
        """
        try:
            if self.db_connection is None:
                self.db_connection = DBConnection(DB_CONFIG, 1, 1)
            else:
                self.db_connection.ensure_pool_is_open()
            return self.db_connection
        except Exception as e:
            print(f"Error getting database connection: {e}")
            return None

    def _sanitize_table_name(self, name: str) -> str:
        """
        Sanitize and validate table name for PostgreSQL.
        
        Args:
            name: The proposed table name
            
        Returns:
            Sanitized table name
            
        Raises:
            ValueError: If table name is invalid
        """
        import re
        
        # PostgreSQL reserved words to check against
        RESERVED_WORDS = {
            'table', 'select', 'from', 'where', 'insert', 'update', 'delete',
            'drop', 'create', 'alter', 'index', 'constraint', 'references',
            'primary', 'foreign', 'key', 'unique', 'check', 'group', 'by',
            'having', 'order', 'limit', 'offset', 'union', 'intersect', 'except'
        }
        
        # Convert to lowercase
        name = name.lower().strip()
        
        # Check length
        if len(name) < 1 or len(name) > 63:  # PostgreSQL limit is 63 characters
            raise ValueError("Table name must be between 1 and 63 characters")
            
        # Check if it's a reserved word
        if name in RESERVED_WORDS:
            raise ValueError(f"'{name}' is a reserved SQL keyword")
            
        # Check if starts with letter
        if not name[0].isalpha():
            raise ValueError("Table name must start with a letter")
            
        # Remove any characters that aren't letters, numbers, or underscores
        sanitized = re.sub(r'[^a-z0-9_]', '_', name)
        
        # Replace multiple underscores with single underscore
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove trailing underscore
        sanitized = sanitized.rstrip('_')
        
        if sanitized != name:
            print(f"Warning: Table name sanitized from '{name}' to '{sanitized}'")
            
        return sanitized

    def process_dbf(self, preview_en: bool, exe_query: bool, custom_tab_name: str = None) -> ProcessResult:
        """
        Process the DBF file, generate SQL, and optionally execute the query and save a preview.

        Args:
            preview_en (bool): Whether to generate a preview.
            exe_query (bool): Whether to execute the SQL query.
            custom_tab_name (str, optional): Custom table name to use.

        Returns:
            ProcessResult: A dataclass containing the result of the operation.
        """
        try:
            # Get DBF data using existing DBFController
            fields = self.dbf_controller.read_dbf_fields()
            name = self.dbf_controller.get_file_name()

            if not fields or not name:
                return ProcessResult(success=False, message="Failed to read DBF file")

            if custom_tab_name:
                try:
                    name = self._sanitize_table_name(custom_tab_name)
                    print(f"Using custom table name: {name}")
                except ValueError as e:
                    return ProcessResult(
                        success=False,
                        message=f"Invalid table name: {str(e)}"
                    )
            else:
                try:
                    name = self._sanitize_table_name(name)
                except ValueError as e:
                    return ProcessResult(
                        success=False,
                        message=f"Invalid table name: {str(e)}"
                    )

            # Generate table query
            sql_query = self.sql_gen_controller.gen_create_table(name, fields)
            if not sql_query:
                return ProcessResult(success=False, message="Failed to generate table query")

            # Create preview if enabled
            preview_path = None
            if preview_en:
                print(f' ------------ preview_en  {preview_en} ')
                self.preview_controller = PreviewController()
               
                preview_path = self.preview_controller.save_preview(sql_query, name)
                if not preview_path:
                    return ProcessResult(
                        success=False,
                        message="Failed to save preview",
                        sql_query=sql_query,
                    )
                print(f"Preview saved to: {preview_path}")

            # Execute query if enabled
            if exe_query:
                print(f' ------------ exe query {exe_query} ')
                db = self._get_db_connection()
                if db is None:
                    return ProcessResult(
                        success=False,
                        message="Failed to establish database connection",
                        sql_query=sql_query,
                        preview_path=preview_path,
                    )

                result = db.execute_query(sql_query)
                if result is None:
                    return ProcessResult(
                        success=False,
                        message="Query execution failed",
                        sql_query=sql_query,
                        preview_path=preview_path,
                    )

            # Return success with SQL query and preview path (if applicable)
            return ProcessResult(
                success=True,
                message="Process completed successfully",
                sql_query=sql_query,
                preview_path=preview_path,
            )

        except Exception as e:
            print(f"Unexpected error: {e}")
            return ProcessResult(
                success=False,
                message=f"Unexpected error: {e}",
                sql_query=sql_query if 'sql_query' in locals() else None,
                preview_path=preview_path if 'preview_path' in locals() else None,
            )

    def cleanup(self):
        """
        Clean up resources when done with the controller.
        Call this method when you're completely done with database operations.
        """
        if self.db_connection and self.db_connection._pool:
            self.db_connection.close_pool()
            self.db_connection = None