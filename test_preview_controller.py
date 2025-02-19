from controllers.dbf_controller import DBFController
from controllers.preview_controller import PreviewController
from models import postgres_model
from models.postgres_model import PostgresModel

def main():
    preview_con = PreviewController()
    dbf_con = DBFController()
    postgres_model = PostgresModel()

    fields = dbf_con.read_dbf_fields()
    name = dbf_con.get_file_name()

    print(f' {fields}')

    sql_create = postgres_model.generate_table(name,fields)

    preview_con.save_preview(sql_create,name)

    

   

if __name__ == "__main__":
    main()