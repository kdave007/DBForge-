# test_postgres_model.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.dbf_model import DBFModel
from models.postgres_model import PostgresModel

def test_integration():
     """
    Test integration between DBFModel and PostgresModel
    """
     try:
        # Initialize models
        dbf_model = DBFModel()
        postgres_model = PostgresModel({})  # Empty config
        
        # Set DBF path
        dbf_path = "mockDBF/PARTVTA.dbf"

        
        fields = dbf_model.read_field_info()
        t_name = dbf_model.get_table_name()

        print('\n'.join(f'{field}' for field in fields))
        print(t_name)

        result = postgres_model.generate_table(t_name,fields)

        print(result)



     except FileNotFoundError:
        print(f"Error: DBF file not found at {dbf_path}")
     except Exception as e:
        print(f"Error during integration test: {e}")

if __name__ == "__main__":
    test_integration()