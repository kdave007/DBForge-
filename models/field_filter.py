
class FieldFilter:
    def __init__(self):
        #List of fields to remove
        self.excluded_fields = []

    def add_excluded_field(self, field_name: str):
        """
            Add a field to be excluded from the table generation
            
            Args:
                field_name: Name of the field to exclude
        """
        field_name = field_name.lower()
        self.excluded_fields.append(field_name) 

    def remove_excluded_field(self, field_name: str): 
        """
            Remove a field from the exclusion list
            
            Args:
                field_name: Name of the field to remove from exclusion
        """
        field_name = field_name.lower()
        if field_name in self.excluded_fields:
            self.excluded_fields.remove(field_name)  
    
    def clear_excluded_fields(self):
        """Clear all excluded fields"""
        self.excluded_fields = []

    def filter_fields(self, fields: list) -> list :
        """
        Filter out excluded fields from the field list
        
        Args:
            fields: List of field dictionaries from DBF
            
        Returns:
            list: New list with excluded fields removed
        """
        # Create an empty list for our filtered fields
        filtered_fields = []
        
        # Go through each field
        for field in fields:
            # Get the field name in lowercase
            field_name = field['name'].lower()
            
            # If field is not in excluded list, keep it
            if field_name not in self.excluded_fields:
                filtered_fields.append(field)
        
        # Return the filtered list
        return filtered_fields