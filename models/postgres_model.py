# postgres_model.py
from typing import List, Dict, Any
from .db_connection import DBConnection
from .type_mapping import TypeMapping

class PostgresModel:
    def __init__(self, db_config: Dict[str, str]) -> None:
        """
        Initialize with database connection parameters
        """
        self.db_config = db_config

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


    def generate_table(self, table_name : str, fields : Dict[str, Any]) -> str :
        """
            Generate CREATE TABLE SQL statement
            Args:
                table_name: Name of the table to create
                fields: List of field definitions
            Returns:
                str: CREATE TABLE SQL statement
        """
        if not table_name or not isinstance(table_name,str):
            raise ValueError("Table name must be a non empty string")

         # Check for existing ID fields
        existing_ids = {'id', 'rowid', 'record_id', 'primary_key'}
        field_names = {field['name'].lower() for field in fields}
        
        # Choose a safe primary key name
        primary_key = next(
            (f"local_{name}" for name in existing_ids if f"local_{name}" not in field_names),
            "local_rowid"
        )    

        # Generate field definitions
        sql_field_definitions  = [f"{primary_key} SERIAL PRIMARY KEY"]
        for field in fields:
            f_name = field['name']
            f_type = self.convert_field_type(field)
            sql_field_definitions.append(f'{f_name} {f_type}')

         # Build SQL
        sql_str = f"CREATE TABLE {table_name} (\n"
        sql_str += ",\n".join(f'  {fd}' for fd in sql_field_definitions)
        sql_str += "\n);"

        return sql_str 
