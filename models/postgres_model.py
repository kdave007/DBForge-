# postgres_model.py
from typing import List, Dict, Any
import config
from .db_connection import DBConnection
from .type_mapping import TypeMapping
from .table_generators import get_generator
from .sql_preview import SQLPreview

class PostgresModel:
    def __init__(self, db_config: Dict[str, str] = config.DB_CONFIG) -> None:
        """
        Initialize with database connection parameters
        """
        self.db_config = db_config
        
        # Debug print to check feature flags
        print("\nDebug - Feature Flags:")
        print(f"All flags: {config.FEATURE_FLAGS}")
        print(f"Preview mode: {config.FEATURE_FLAGS.get('preview_mode', False)}")
        
        self.preview = SQLPreview() if config.FEATURE_FLAGS.get('preview_mode', False) else None
        print(f"Preview object created: {self.preview is not None}")
        
        # Delegate to factory function
        self.generator = get_generator(self)

    def convert_field_type(self, dbf_field: Dict[str, Any]) -> str:
        """
        Convert DBF field type to PostgreSQL type
        """
        try: 
            field_type = dbf_field['type'].upper()
            f_length = dbf_field['length']
            f_decimal = dbf_field['decimal']

            if not isinstance(f_length, int) or f_length <= 0:
                raise ValueError("Length must be a positive integer")
            if not isinstance(f_decimal, int) or f_decimal < 0:
                raise ValueError("Decimal must be a non-negative integer")

            return TypeMapping.get_type(field_type, f_length, f_decimal)
        
        except KeyError as e:
            raise KeyError(f"Missing required field: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid field value: {e}")

    def generate_table(self, table_name: str, fields: List[Dict[str, Any]]) -> str:
        """
        Generate CREATE TABLE SQL statement and optionally save preview
        
        Args:
            table_name: Name of the table to create
            fields: List of field definitions
            
        Returns:
            str: CREATE TABLE SQL statement or preview file path
        """
        if not table_name or not isinstance(table_name, str):
            raise ValueError("Table name must be a non empty string")
            
        # Check for existing ID fields
        existing_ids = {'id', 'rowid', 'record_id'}
        field_names = {field['name'].lower() for field in fields}
        
        # Choose a safe primary key name
        primary_key = next(
            (f"local_{name}" for name in existing_ids if f"local_{name}" not in field_names),
            "local_rowid"
        )    

        # Generate SQL
        sql = self.generator.generate_table(
            table_name=table_name,
            fields=fields,
            primary_key=primary_key
        )
        
        # Debug print for preview mode
        print(f"\nDebug - Generate Table:")
        print(f"Preview mode active: {self.preview is not None}")
        print(f"SQL Generated: {sql[:100]}...")  # Show first 100 chars of SQL
        
        # If in preview mode, save to file
        if self.preview:
            preview_path = self.preview.save_preview(table_name, sql)
            print(f"Preview saved to: {preview_path}")
            return f"SQL Preview saved to: {preview_path}"
            
        return sql
