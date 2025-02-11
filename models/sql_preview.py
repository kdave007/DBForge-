from typing import Optional
import os
from pathlib import Path
from datetime import datetime
from config import PATH_CONFIG

class SQLPreview:
    """Handles SQL preview file generation"""
    
    def __init__(self):
        self.output_dir = Path(PATH_CONFIG['sql_output'])
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def save_preview(self, table_name: str, sql_content: str, suffix: Optional[str] = None) -> str:
        """
        Save SQL content to a preview file
        
        Args:
            table_name: Name of the table
            sql_content: SQL query content
            suffix: Optional suffix for the filename
            
        Returns:
            str: Path to the generated file
        """
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename = f"{table_name}_{timestamp}"
        if suffix:
            filename = f"{filename}_{suffix}"
        filename = f"{filename}.sql"
        
        # Full path for the file
        file_path = self.output_dir / filename
        
        # Add header comment to SQL
        header = f"-- SQL Preview generated for table: {table_name}\n"
        header += f"-- Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Write to file
        with open(file_path, 'w') as f:
            f.write(header + sql_content)
        
        return str(file_path)
