from models.postgres_model import PostgresModel 

class SQLGeneratorController:
    def __init__(self):
        self.gen = PostgresModel()

    def gen_create_table(self, table_name, fields) -> str :
        """
        Args:
            table_name (str): Name of the SQL table
            fields (list): List of DBF field definitions from DBFController
        
        Returns:
            str: SQL CREATE TABLE statement
        """
        try:
            return self.gen.generate_table(table_name, fields)
        except Exception as e:
            # Add error handling/logging
            print(f"Error generating SQL: {e}")
            return None

    def validate_table_name(self, name) -> bool :
        """ if valid string and length return true"""
        return isinstance(name, str) and len(name) > 0