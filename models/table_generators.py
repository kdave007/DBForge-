# models/table_generators.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from config import FEATURE_FLAGS, get_table_mode
from .type_mapping import TypeMapping  # Use TypeMapping directly

class TableGenerator(ABC):
    """Base class for table generation strategies"""
    
    @abstractmethod
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        pass

    def _build_sql(self, table_name: str, fields: List[str]) -> str:
        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(fields) + "\n);"
    
    def _get_field_definition(self, field: Dict[str, Any]) -> str:
        """
        Generate field definition including NULL/NOT NULL constraint
        
        Args:
            field: Dictionary containing field properties (type, length, decimal, etc.)
            
        Returns:
            str: SQL field definition string
            
        Raises:
            KeyError: If required field properties are missing
            ValueError: If field values are invalid
        """
        try:
            # Extract and validate field name
            if 'name' not in field:
                raise KeyError("name")
            f_name = field['name']
            
            # Extract and validate type properties
            field_type = field['type'].upper()
            f_length = field['length']
            f_decimal = field['decimal']

            # Validate numeric properties
            if not isinstance(f_length, int) or f_length <= 0:
                raise ValueError("Length must be a positive integer")
            if not isinstance(f_decimal, int) or f_decimal < 0:
                raise ValueError("Decimal must be a non-negative integer")

            # Get PostgreSQL type
            f_type = TypeMapping.get_type(field_type, f_length, f_decimal)
            
            # Handle NULL/NOT NULL constraint
            null_constraint = "NOT NULL" if field.get('not_null', False) else ""
            
            # Handle default values for character fields
            if f_type.startswith(('VARCHAR', 'CHAR')) and field.get('empty_as_null', False) is False:
                return f"{f_name} {f_type} DEFAULT '' {null_constraint}"
            
            return f"{f_name} {f_type} {null_constraint}".strip()
            
        except KeyError as e:
            raise KeyError(f"Missing required field property: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid field value: {e}")
        except Exception as e:
            raise Exception(f"Error creating field definition: {e}")

class RawGenerator(TableGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = []  # Fix: Initialize as empty list
        
        for field in fields:
            sql_fields.append(self._get_field_definition(field))
            
        return self._build_sql(table_name, sql_fields)

class BasicGenerator(RawGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [f"{primary_key} SERIAL PRIMARY KEY"]
        
        for field in fields:
            sql_fields.append(self._get_field_definition(field))
            
        return self._build_sql(table_name, sql_fields)

class TimestampGenerator(BasicGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [
            f"{primary_key} SERIAL PRIMARY KEY",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL"
        ]
        
        for field in fields:
            sql_fields.append(self._get_field_definition(field))
            
        return self._build_sql(table_name, sql_fields)

class AuditGenerator(TimestampGenerator):
    """Adds both created_at and updated_at timestamps"""
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [
            f"{primary_key} SERIAL PRIMARY KEY",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL",
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL"
        ]
        
        for field in fields:
            sql_fields.append(self._get_field_definition(field))
            
        return self._build_sql(table_name, sql_fields)

def get_generator() -> TableGenerator:
    """Factory function to get the appropriate table generator based on configuration"""
    mode = get_table_mode()
    
    if mode == 'audit':
        return AuditGenerator()
    elif mode == 'timestamp':
        return TimestampGenerator()
    elif mode == 'basic':
        return BasicGenerator()
    else:
        return RawGenerator()