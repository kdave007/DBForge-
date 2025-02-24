from controllers.table_creation_controller import TableCreationController
import config

def test_table_creation_controller():
    # Initialize the controller
    controller = TableCreationController()
    preview_en = config.FEATURE_FLAGS['preview_mode']
    exe_query= config.FEATURE_FLAGS['execute_query']

    try:
        # Test without preview
        print("Testing without preview:")
        result = controller.process_dbf(preview_en,exe_query )
        print(f"Result: {result}")

        
    finally:
        # Always cleanup resources, even if tests fail
        controller.cleanup()

# Run the test
test_table_creation_controller()