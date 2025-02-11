from dbfread import DBF
from typing import List, Dict, Any, Optional, Tuple
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
                self.dbf_path = str(os.path.join(PATH_CONFIG['dbf'], dbf_filename))
        
        self.dbf_data: List[Dict[str, Any]] = []
        # Store paths to memo files
        self.memo_files = self._find_memo_files()

    def _find_memo_files(self) -> Dict[str, str]:
        """
        Find associated memo files (FPT, DBT) for the DBF file.
        
        Returns:
            Dict[str, str]: Dictionary with memo file types and their paths
        """
        memo_files = {}
        base_path = os.path.splitext(self.dbf_path)[0]
        
        # Check for FPT file
        fpt_path = f"{base_path}.fpt"
        if os.path.exists(fpt_path):
            memo_files['fpt'] = fpt_path
        
        # Check for DBT file
        dbt_path = f"{base_path}.dbt"
        if os.path.exists(dbt_path):
            memo_files['dbt'] = dbt_path
            
        return memo_files

    def has_memo_fields(self) -> bool:
        """
        Check if the DBF file has associated memo fields.
        
        Returns:
            bool: True if memo files exist, False otherwise
        """
        return len(self.memo_files) > 0

    def validate_dbf(self) -> bool:
        """
        Validate if the file exists, has .dbf extension and can be opened.
        Also checks for associated memo files if they exist.
        
        Returns:
            bool: True if valid, False otherwise
        """
        # Check if file exists
        if not os.path.exists(self.dbf_path):
            print(f"Error: File {self.dbf_path} does not exist")
            return False
            
        # Check file extension
        if not str(self.dbf_path).lower().endswith('.dbf'):
            print(f"Error: File {self.dbf_path} is not a DBF file")
            return False
            
        # Try to open the DBF file and check memo files
        try:
            with DBF(self.dbf_path) as dbf:
                # If we have memo files, verify they can be accessed
                for memo_type, memo_path in self.memo_files.items():
                    if not os.path.exists(memo_path):
                        print(f"Warning: {memo_type.upper()} memo file exists but cannot be accessed: {memo_path}")
                return True
        except Exception as e:
            print(f"Error reading DBF file {self.dbf_path}: {e}")
            return False

    def read_field_info(self) -> List[Dict[str, Any]]:
        """
        Read and return field information from the DBF file.
        Includes information about memo fields if present.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing field information
                                 Each dict has: name, type, length, decimal
                                 For memo fields, additional memo_type will be included
        """
        valid = self.validate_dbf()
        if not valid:
            return []

        field_info = []
        try:
            with DBF(self.dbf_path) as dbf:
                for field in dbf.fields:
                    field_data = {
                        'name': field.name,
                        'type': field.type,
                        'length': field.length,
                        'decimal': field.decimal if hasattr(field, 'decimal') else 0,
                        # By default, allow NULL values for all fields
                        'not_null': False,
                        # For character fields, treat empty strings as NULL by default
                        'empty_as_null': True
                    }
                    
                    # If this is a memo field, add memo type information
                    if field.type in ['M', 'B', 'G']:  # Memo field types
                        if 'fpt' in self.memo_files:
                            field_data['memo_type'] = 'fpt'
                        elif 'dbt' in self.memo_files:
                            field_data['memo_type'] = 'dbt'
                            
                    field_info.append(field_data)
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