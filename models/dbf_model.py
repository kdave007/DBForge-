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

    def read_field_info(self) -> List[Dict[str, Any]]:
        """
        Read and return field information from the DBF file.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing field information
                                 Each dict should have: name, type, length, decimal
        """
        valid = self.validate_dbf()
        if not valid:
            return []

        field_info = []
        try:
            with DBF(self.dbf_path) as dbf:
                for field in dbf.fields:
                    field_info.append({
                        'name': field.name,
                        'type': field.type,
                        'length': field.length,
                        'decimal': field.decimal if hasattr(field, 'decimal') else 0
                    })
            return field_info
        
        except Exception as e:
            print(f"Error reading DBF file {self.dbf_path}: {e}")
            return []

    def get_table_name(self) -> str:
        """
        Get the table name from the DBF file (usually the file name without extension).
        Makes the name database-friendly by:
        - Converting to lowercase
        - Replacing spaces with underscores
        - Removing special characters
        
        Returns:
            str: The sanitized table name
        """
        import re
        
        # Get the base filename without extension
        file_name = os.path.basename(self.dbf_path)
        table_name = os.path.splitext(file_name)[0]
        
        # Make it database-friendly
        table_name = table_name.lower()  # Convert to lowercase
        table_name = re.sub(r'\s+', '_', table_name)  # Replace spaces with underscores
        table_name = re.sub(r'[^a-z0-9_]', '', table_name)  # Remove special chars
        
        return table_name