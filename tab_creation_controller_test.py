from controllers.table_creation_controller import TableCreationController

def test_table_creation_controller():
    # Initialize the controller
    controller = TableCreationController()

    # Test without preview
    print("Testing without preview:")
    result = controller.process_dbf(preview_en=False, exe_query=True)
    print(f"Result: {result}")

    # Test with preview
    print("\nTesting with preview:")
    result = controller.process_dbf(preview_en=True, exe_query=True)
    print(f"Result: {result}")

# Run the test
test_table_creation_controller()