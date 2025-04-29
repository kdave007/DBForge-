from models.sql_preview import SQLPreview
import config

class PreviewController:
    def __init__(self) -> None:
        try:
            self.gen = SQLPreview()
        except ValueError as e:
            raise RuntimeError(f"Failed to initialize preview generator: {e}")

    
    def save_preview(self, content: str, table_name: str) -> str | None :
        """Save SQL preview to a file.
    
        Args:
            content: Raw SQL string to save (e.g., "CREATE TABLE ...")  # <-- Ensure this is the SQL query, not a dictionary of fields
            table_name: Target table name for filename
                
        Returns:
            str: Path to saved file if successful
            None: If saving failed
    """
        try:
            # Validate that content is a SQL query string and not a dictionary
            if not isinstance(content, str) or not content.strip().upper().startswith(("CREATE TABLE", "ALTER TABLE", "DROP TABLE")):
                raise ValueError(
                    f"Invalid content type. Expected a SQL query string starting with 'CREATE TABLE', 'ALTER TABLE', or 'DROP TABLE'. Got: {type(content)}"
             )
             
            return self.gen.save_preview(table_name, content ,None)

        except (IOError, ValueError, KeyError) as e:
            print(f"Preview save failed: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

