import os
import configparser
from pathlib import Path
import sys
from typing import Any, Dict

# Default configuration values
DEFAULT_CONFIG = {
    'paths': {
        'dbf_directory': '../mockDBF/CANCFFI.DBF',
        'sql_output': '../'
    },
    'features': {
        'table_mode': 'raw',  # raw, basic, timestamp, audit
        'preview_mode': 'false',
        'preview_ext': 'txt',   # txt, sql
        'execute_query': 'false',
        'custom_table_name_en': 'false',
        'table_name': 'default_table'
    },
    'database': {
        'host': 'localhost',
        'port': '5432',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'default_password'
    }
}

# Configuration validation rules
CONFIG_RULES = {
    'table_mode': ['basic', 'timestamp', 'audit'],
    'preview_ext': ['txt', 'sql']
}

def validate_config_value(key: str, value: str) -> str:
    """Validate configuration values against rules."""
    if key in CONFIG_RULES:
        if value not in CONFIG_RULES[key]:
            print(f"Warning: Invalid {key} value '{value}'. Using default: {DEFAULT_CONFIG['features'][key]}")
            return DEFAULT_CONFIG['features'][key]
    return value

def load_config(config_path: str) -> configparser.ConfigParser:
    """Load configuration from a file with defaults."""
    config = configparser.ConfigParser()
    
    # First load defaults
    config.read_dict(DEFAULT_CONFIG)
    
    # Then try to load user config
    if os.path.exists(config_path):
        try:
            config.read(config_path, encoding='utf-8')
        except Exception as e:
            print(f"Warning: Error reading config file {config_path}: {e}")
            print("Using default configuration")
    else:
        print(f"Warning: Config file not found at {config_path}")
        print("Using default configuration")
    
    return config

# Get the directory where the executable/script is located
def get_app_path():
    """Get the application base path that works both in dev and PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return Path(sys.executable).parent
    else:
        # Running in development
        return Path(__file__).resolve().parent

BASE_DIR = get_app_path()

# Load public configuration
CONFIG = load_config(os.path.join(BASE_DIR, 'config.ini'))

# Load secure configuration from a separate location
SECURE_CONFIG_PATH = os.getenv('DBFORGE_SECURE_CONFIG', os.path.join(BASE_DIR, 'secure', 'secure_config.ini'))
SECURE_CONFIG = load_config(SECURE_CONFIG_PATH)

def get_config_value(section: str, key: str, default: Any = None, as_boolean: bool = False) -> Any:
    """
    Get configuration value with validation and type conversion.
    
    Args:
        section: Configuration section name
        key: Configuration key
        default: Default value if not found
        as_boolean: Whether to convert value to boolean
    """
    try:
        if as_boolean:
            return CONFIG[section].getboolean(key, default)
        value = CONFIG[section].get(key, default)
        return validate_config_value(key, value)
    except Exception as e:
        print(f"Warning: Error getting config value [{section}]{key}: {e}")
        return default

# Path configuration
PATH_CONFIG = {
    'dbf_directory': get_config_value('paths', 'dbf_directory', DEFAULT_CONFIG['paths']['dbf_directory']),
    'sql_output': get_config_value('paths', 'sql_output', DEFAULT_CONFIG['paths']['sql_output'])
}

# Feature flags (public configuration)
FEATURE_FLAGS = {
    'table_mode': get_config_value('features', 'table_mode', DEFAULT_CONFIG['features']['table_mode']),
    'preview_mode': get_config_value('features', 'preview_mode', False, as_boolean=True),
    'preview_ext': get_config_value('features', 'preview_ext', DEFAULT_CONFIG['features']['preview_ext']),
    'execute_query': get_config_value('features', 'execute_query', False, as_boolean=True),
    'custom_table_name_en': get_config_value('features', 'custom_table_name_en', False, as_boolean=True),
    'table_name': get_config_value('features', 'table_name', DEFAULT_CONFIG['features']['table_name'])
}

# Database configuration (secure configuration)
DB_CONFIG = {
    'host': SECURE_CONFIG['database']['host'],
    'port': SECURE_CONFIG['database'].getint('port', int(DEFAULT_CONFIG['database']['port'])),
    'database': SECURE_CONFIG['database']['database'],
    'user': SECURE_CONFIG['database']['user'],
    'password': SECURE_CONFIG['database']['password']
}

def get_table_mode() -> str:
    """Get the table creation mode from configuration."""
    return FEATURE_FLAGS['table_mode']

def get_preview_mode() -> bool:
    """Get whether preview mode is enabled."""
    return FEATURE_FLAGS['preview_mode']

def get_preview_ext() -> str:
    """Get the file extension for preview files."""
    return FEATURE_FLAGS['preview_ext']

def get_execute_query() -> bool:
    """Get whether query execution is enabled."""
    return FEATURE_FLAGS['execute_query']

def is_custom_table_name_enabled() -> bool:
    """Get whether custom table name feature is enabled."""
    return FEATURE_FLAGS['custom_table_name_en']

def get_custom_table_name() -> str:
    """Get the table name from configuration."""
    return FEATURE_FLAGS['table_name']