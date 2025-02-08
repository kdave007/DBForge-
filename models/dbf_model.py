from dbfread import DBF
from typing import List, Dict, Any
import os

class DBFModel:
    def __init__(self, dbf_path: str) -> None:
        self.dbf_path = dbf_path
        self.dbf_data: List[Dict[str, Any]] = []

    def validate_dbf(self) -> bool:
        """
        Validate if the file exists, has .dbf extension and can be opened.
        
        Returns:
            bool: True if valid, False otherwise
        """
        # Check if file exists
        if not os.path.exists(self.dbf_path):
            print(f"Error: File {self.dbf_path} does not exist")
            return False
            
        # Check file extension
        if not self.dbf_path.lower().endswith('.dbf'):
            print(f"Error: File {self.dbf_path} is not a DBF file")
            return False
            
        # Try to open the DBF file
        try:
            with DBF(self.dbf_path) as dbf:
                return True
        except Exception as e:
            print(f"Error reading DBF file {self.dbf_path}: {e}")
            return False

    def read_file_info(self) -> List[Dict[str, Any]]:
        """
        Read and return field information from the DBF file.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing field information
                                 Each dict should have: name, type, length, decimal
        """
        valid = self.validate_dbf(dbf_path)
        if not valid:
            return []

        with DBF(self.dbf_path) as dbf:
            for field in dbf.fields:
                print(field.field_name, field.field_type, field.field_length, field.decimal_count)