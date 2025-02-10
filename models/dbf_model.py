from dbfread import DBF
from typing import List, Dict, Any, Optional
import os
from config import PATH_CONFIG

class DBFModel:
    def __init__(self, dbf_filename: Optional[str] = None) -> None:
        """
        Initialize DBFModel with an optional filename/path.
        If no filename is provided, it will use the path from config.ini
        If a filename is provided, it will be used as is (if it's a full path)
        or joined with the config directory (if it's just a filename)
        
        Args:
            dbf_filename (Optional[str]): Path to DBF file or filename (optional)
        """
        if dbf_filename is None:
            # Use path directly from config
            self.dbf_path = str(PATH_CONFIG['dbf'])  # Convert Path to string
        else:
            # If it looks like a full path, use it as is
            if os.path.isabs(dbf_filename) or '../' in dbf_filename:
                self.dbf_path = dbf_filename
            else:
                # Otherwise join it with the config directory
                self.dbf_path = str(os.path.join(PATH_CONFIG['dbf'], dbf_filename))  # Convert Path to string
                
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
        if not str(self.dbf_path).lower().endswith('.dbf'):  # Convert to string before using lower()
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