from controllers.table_creation_controller import TableCreationController
import config

def test_table_creation_controller():
    # Initialize the controller
    controller = TableCreationController()
    preview_en = config.FEATURE_FLAGS['preview_mode']
    exe_query= config.FEATURE_FLAGS['execute_query']
    custom_table_en = config.FEATURE_FLAGS['custom_table_name_en']
    custom_tab_name= config.FEATURE_FLAGS['table_name']

    try:
        # check if custom table name is enabled
        if(custom_table_en):
            result = controller.process_dbf(preview_en,exe_query, custom_tab_name)
        else:
            result = controller.process_dbf(preview_en,exe_query)
            print(f"Result: {result}")

        
    finally:
        # Always cleanup resources, even if tests fail
        controller.cleanup()

# Run the test
test_table_creation_controller()