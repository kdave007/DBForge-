# test_postgres_model.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.dbf_model import DBFModel
from models.postgres_model import PostgresModel
from models.field_filter import FieldFilter
import config

def test_integration():
    """
    Test integration between DBFModel and PostgresModel with field filtering
    """
    try:
        # Initialize models
        dbf_model = DBFModel()
        postgres_model = PostgresModel(config.DB_CONFIG)
        
        # Create field filter
        field_filter = FieldFilter()
        
        # Read field information
        fields = dbf_model.read_field_info()
        t_name = dbf_model.get_table_name()

        # Print original fields
        print("\nOriginal Fields:")
        print('-' * 50)
        for field in fields:
            print(f"Field: {field['name']}, Type: {field['type']}, Length: {field['length']}")
        
        # Add some fields to exclude
        field_filter.configure()  # Example field to exclude
        
        # Get filtered fields
        filtered_fields = field_filter.included_fields(fields)
        
        # Print filtered fields
        print("\nFiltered Fields (after excluding 'BAN_MOSTRA'):")
        print('-' * 50)
        for field in filtered_fields:
            print(f"Field: {field['name']}, Type: {field['type']}, Length: {field['length']}")
        
        print(f"\nTable Name: {t_name}")
        print('-' * 50)

        # Generate table SQL with filtered fields
        result = postgres_model.generate_table(t_name, filtered_fields)
        
        print("\nResult:")
        print('-' * 50)
        print(result)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error during integration test: {e}")

if __name__ == "__main__":
    test_integration()