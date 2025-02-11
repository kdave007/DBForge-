import configparser
from pathlib import Path
import os

def load_config():
    """Load and validate configuration from INI file"""
    config = configparser.ConfigParser()
    
    # Set defaults
    config.read_dict({
        'paths': {
            'dbf_directory': 'mockDBF/',
            'sql_output_directory': 'generated_sql/'
        },
        'database': {
            'host': 'localhost',
            'port': '5432',
            'database': 'dbfields_db',
            'user': 'postgres',
            'password': 'secret'
        },
        'features': {
            'table_mode': 'basic',
            'preview_mode': 'false'  # Add default for preview mode
        }
    })
    
    # Load user config if exists
    config_path = Path(__file__).parent / 'config.ini'
    if config_path.exists():
        config.read(config_path)
    
    return config

# Initialize configuration
CONFIG = load_config()

# Expose typed configurations
DB_CONFIG = {
    'host': CONFIG['database']['host'],
    'port': CONFIG['database'].getint('port'),
    'database': CONFIG['database']['database'],
    'user': CONFIG['database']['user'],
    'password': CONFIG['database']['password']
}

PATH_CONFIG = {
    'dbf': Path(CONFIG['paths']['dbf_directory']),
    'sql_output': Path(CONFIG['paths']['sql_output_directory'])
}

# Feature flags and settings 
# Mode can be: basic (pk only), timestamp (pk + created_at), audit (pk + created_at + updated_at)
FEATURE_FLAGS = {
    'table_mode': CONFIG['features']['table_mode'],
    'preview_mode': CONFIG['features'].getboolean('preview_mode', False)  # Convert to boolean
}

def get_table_mode():
    """Get the current table generation mode"""
    mode = FEATURE_FLAGS['table_mode'].lower()
    if mode not in ['basic', 'timestamp', 'audit']:
        return 'basic'  # Default to basic mode if invalid setting
    return mode