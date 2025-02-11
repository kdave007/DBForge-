# models/table_generators.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from config import FEATURE_FLAGS, get_table_mode

class TableGenerator(ABC):
    """Base class for table generation strategies"""
    def __init__(self, postgres_model: 'PostgresModel'):
        self.postgres_model = postgres_model
    
    @abstractmethod
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]]) -> str:
        pass

    def _build_sql(self, table_name: str, fields: List[str]) -> str:
        return f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(fields) + "\n);"
    
    def _get_field_definition(self, field: Dict[str, Any]) -> str:
        """
        Generate field definition including NULL/NOT NULL constraint
        """
        f_name = field['name']
        f_type = self.postgres_model.convert_field_type(field)
        
        # By default, allow NULL values unless explicitly marked as NOT NULL
        null_constraint = "NOT NULL" if field.get('not_null', False) else ""
        
        # For character fields, add default '' for empty strings if needed
        if f_type.startswith(('VARCHAR', 'CHAR')) and field.get('empty_as_null', False) is False:
            return f"{f_name} {f_type} DEFAULT '' {null_constraint}"
        
        return f"{f_name} {f_type} {null_constraint}".strip()

class BasicGenerator(TableGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [f"{primary_key} SERIAL PRIMARY KEY"]
        
        for field in fields:
            sql_fields.append(self._get_field_definition(field))
            
        return self._build_sql(table_name, sql_fields)

class TimestampGenerator(BasicGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        # Get base fields from parent class
        sql_fields = [
            f"{primary_key} SERIAL PRIMARY KEY",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL"
        ]
        
        # Add DBF fields using parent class logic
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

def get_generator(postgres_model: 'PostgresModel') -> TableGenerator:
    """
    Factory function to get the appropriate table generator based on configuration
    """
    mode = get_table_mode()
    
    if mode == 'audit':
        return AuditGenerator(postgres_model)
    elif mode == 'timestamp':
        return TimestampGenerator(postgres_model)
    else:
        return BasicGenerator(postgres_model)