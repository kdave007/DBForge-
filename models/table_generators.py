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

class BasicGenerator(TableGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [f"{primary_key} SERIAL PRIMARY KEY"]
        
        for field in fields:
            f_name = field['name']
            f_type = self.postgres_model.convert_field_type(field)
            sql_fields.append(f'{f_name} {f_type}')
            
        return self._build_sql(table_name, sql_fields)

class TimestampGenerator(BasicGenerator):
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        # Get base fields from parent class
        sql_fields = [
            f"{primary_key} SERIAL PRIMARY KEY",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]
        
        # Add DBF fields using parent class logic
        for field in fields:
            f_name = field['name']
            f_type = self.postgres_model.convert_field_type(field)
            sql_fields.append(f'{f_name} {f_type}')
            
        return self._build_sql(table_name, sql_fields)

class AuditGenerator(TimestampGenerator):
    """Adds both created_at and updated_at timestamps"""
    def generate_table(self, table_name: str, fields: List[Dict[str, Any]], primary_key: str) -> str:
        sql_fields = [
            f"{primary_key} SERIAL PRIMARY KEY",
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]
        
        for field in fields:
            f_name = field['name']
            f_type = self.postgres_model.convert_field_type(field)
            sql_fields.append(f'{f_name} {f_type}')
            
        return self._build_sql(table_name, sql_fields)

def get_generator(postgres_model) -> TableGenerator:
    """Factory function to get the appropriate table generator based on configuration"""
    mode = get_table_mode()
    
    if mode == 'audit':
        return AuditGenerator(postgres_model)
    elif mode == 'timestamp':
        return TimestampGenerator(postgres_model)
    else:  # 'basic' or any invalid mode
        return BasicGenerator(postgres_model)