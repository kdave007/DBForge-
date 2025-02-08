from models import DBFModel

# Sample DBF file path (replace with your actual file path)
SAMPLE_DBF = "mockDBF/PARTVTA.dbf"

def test_dbf_model(file_path):
    print(f"\nTesting DBF Model with file: {file_path}")
    
    # Create instance
    dbf_model = DBFModel(file_path)
    
    # Test validation
    print("\nValidating DBF file:")
    valid = dbf_model.validate_dbf()
    print(f"Validation result: {valid}")
    
    if valid:
        # Test field information
        print("\nField Information:")
        fields = dbf_model.read_field_info()
        for field in fields:
            print(f"Field: {field['name']}, Type: {field['type']}, Length: {field['length']}, Decimal: {field['decimal']}")
        
        # Test table name
        print("\nTable Name:")
        table_name = dbf_model.get_table_name()
        print(f"Generated table name: {table_name}")

if __name__ == "__main__":
    # Run the test
    test_dbf_model(SAMPLE_DBF)
