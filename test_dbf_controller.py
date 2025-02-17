# test_dbf_controller.py

from controllers.dbf_controller import DBFController

def main():
    dbf_controller = DBFController()
    fields = dbf_controller.read_dbf_fields()
    file_name = dbf_controller.get_file_name()
    print(f"Fields: {fields}")
    print(f"File Name: {file_name}")

if __name__ == "__main__":
    main()