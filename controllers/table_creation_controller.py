from controllers import SQLGeneratorController
from controllers.preview_controller import PreviewController
from models.db_connection import DBConnection
from controllers.dbf_controller import DBFController

class TableCreationController:
    def __init__(self):
        """Initialize models and other controllers"""
        self.sql_gen_controller = SQLGeneratorController()
        self.dbf_controller = DBFController()
        #self.db_connection = DBConnection()
        

    def process_dbf(self, preview_en : bool):

        try:
           # Get DBF data using existing DBFController
            fields = self.dbf_controller.read_dbf_fields()
            name = self.dbf_controller.get_file_name()

            if not fields or not name:
                return "Failed to read DBF file"

           # Generate table query
            sql_query = self.sql_gen_controller.gen_create_table(name, fields)
            
            if not sql_query:
                return "Failed to generate table query"

           # create preview 
            if preview_en:
                self.preview_controller = PreviewController()
                # pass the sql query to save preview and the table name
                preview_path = self.preview_controller.save_preview(sql_query, name)

                if preview_path:
                    print(f"Preview saved to: {preview_path}")
        
            
            return sql_query





        
        except Exception as e:
            return null
