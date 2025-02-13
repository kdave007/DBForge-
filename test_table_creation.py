import sys
import os

from models.postgres_model import PostgresModel
from models.table_generators import TableGenerator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.dbf_model import DBFModel
from models.db_connection import DBConnection
from config import DB_CONFIG

# Sample DBF file path (replace with your actual file path)
SAMPLE_DBF = "mockDBF/CANOTA.dbf"  # Update this path to your DBF file

def test_table_creation():
    """
    Test the process of:
    1. Reading DBF fields
    2. Generating table creation SQL
    3. Creating table in PostgreSQL
    """
    print("\nStarting Table Creation Test")
    print("-" * 50)

    try:
        # TODO: Step 1 - Create DBF model and read fields
        # Hint: Use DBFModel(SAMPLE_DBF) and read_field_info()
        dbf_model = DBFModel()
        fields = dbf_model.read_field_info()
        

        for field in fields:
            print(f'{field} \n ')
        
        # TODO: Step 2 - Generate table name
        # Hint: Use get_table_name()
        table_name = dbf_model.get_table_name()

        # TODO: Step 3 - Create database connection
        # Hint: Use DBConnection(DB_CONFIG)
        db = DBConnection(DB_CONFIG)

        # TODO: Step 4 - Generate CREATE TABLE query
        # Hint: Build the query using the fields from step 1
        # Format: CREATE TABLE table_name (field_name field_type, ...)
        pm = PostgresModel()
        table_query = pm.generate_table(table_name,fields)
        print(f'hey this is {table_query}')
        

        # TODO: Step 5 - Execute the query
        # Hint: Use db.execute_query(query)
        db.execute_query(table_query)
        db.close_pool()
        

        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nError during test: {e}")
        raise e

if __name__ == "__main__":
    test_table_creation()
