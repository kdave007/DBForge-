#!/usr/bin/env python3
import sys
import logging
import argparse
from datetime import datetime
from controllers.table_creation_controller import TableCreationController
import config

def setup_logging():
    """Configure logging to both file and console"""
    # Create logs directory if it doesn't exist
    from pathlib import Path
    Path("logs").mkdir(exist_ok=True)
    
    # Setup logging format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(f"logs/dbforge_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='DBForge - DBF to PostgreSQL Table Generator')
    
    parser.add_argument('--preview', action='store_true', 
                       help='Generate SQL preview files instead of executing them')
    parser.add_argument('--execute', action='store_true',
                       help='Execute the generated SQL queries')
    parser.add_argument('--table-name',
                       help='Custom table name to use instead of DBF filename')
    
    return parser.parse_args()

def main():
    """Main entry point of the application"""
    # Setup logging
    setup_logging()
    logging.info("--------------------Starting DBForge...----------------------")
    
    # Parse command line arguments
    args = parse_args()
    
    # Override config with command line arguments if provided
    if args.preview:
        config.FEATURE_FLAGS['preview_mode'] = 'true'
    if args.execute:
        config.FEATURE_FLAGS['execute_query'] = 'true'
    if args.table_name:
        config.FEATURE_FLAGS['custom_table_name_en'] = 'true'
        config.FEATURE_FLAGS['table_name'] = args.table_name
    
    # Log current configuration
    logging.info(f"Configuration: {config.FEATURE_FLAGS}")
    
    # Initialize controller
    controller = TableCreationController()
    
    try:
        preview_en = config.FEATURE_FLAGS['preview_mode']
        exe_query = config.FEATURE_FLAGS['execute_query']
        custom_table_en = config.FEATURE_FLAGS['custom_table_name_en']
        custom_tab_name = config.FEATURE_FLAGS['table_name']
        
        # Process DBF file
        if custom_table_en:
            logging.info(f"Processing DBF with custom table name: {custom_tab_name}")
            result = controller.process_dbf(preview_en, exe_query, custom_tab_name)
        else:
            logging.info("Processing DBF with default table name")
            result = controller.process_dbf(preview_en, exe_query)
        
        # Log result
        logging.info(f"Processing completed successfully: {result}")
        print(f"\nSuccess! Result: {result}")
        
    except Exception as e:
        logging.error(f"Error processing DBF: {str(e)}", exc_info=True)
        print(f"\nError: {str(e)}")
        sys.exit(1)
        
    finally:
        # Always cleanup resources
        try:
            controller.cleanup()
            logging.info("//////////// Cleanup completed /////////////")
        except Exception as e:
            logging.error(f"Error during cleanup: {str(e)}", exc_info=True)

if __name__ == '__main__':
    main()
