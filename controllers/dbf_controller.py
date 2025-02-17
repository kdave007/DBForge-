
from models.dbf_model import DBFModel

class DBFController():
    def __init__(self):
        self.dbf_model = DBFModel()
    
    def read_dbf_fields(self):
        """
            Reads a DBF file and returns its columns and file name.
        """
        try:
            fields = self.dbf_model.read_field_info()
            return fields
        except Exception as e:
            print(f"Error reading DBF file: {e}")
            return None

    def get_file_name(self):
        """
            Reads a DBF file and returns its columns and file name.
        """
        try:
            f_name = self.dbf_model.get_table_name()
            return f_name
        except Exception as e:
            print(f"Error reading DBF file: {e}")
            return None

    