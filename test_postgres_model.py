# test_postgres_model.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.dbf_model import DBFModel
from models.postgres_model import PostgresModel
import config  # Import config to use DB_CONFIG

def test_integration():
    """
    Test integration between DBFModel and PostgresModel
    """
    try:
        # Initialize models
        dbf_model = DBFModel()  # Will use path from config.ini
        postgres_model = PostgresModel(config.DB_CONFIG)  # Use proper DB config
        
        # Read field information
        fields = dbf_model.read_field_info()
        t_name = dbf_model.get_table_name()

        # Print field information
        print("\nField Information:")
        print('-' * 50)
        for field in fields:
            print(f"Field: {field['name']}, Type: {field['type']}, Length: {field['length']}")
        
        print(f"\nTable Name: {t_name}")
        print('-' * 50)

        # Generate table SQL (will create preview file if preview_mode is true)
        result = postgres_model.generate_table(t_name, fields)
        
        print("\nResult:")
        print('-' * 50)
        print(result)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error during integration test: {e}")

if __name__ == "__main__":
    test_integration()