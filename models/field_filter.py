"""
FieldFilter: A class to manage field exclusion for database table generation.

Usage Examples:
--------------
1. Configure with list of fields:
    filter = FieldFilter()
    filter.configure(['FIELD1', 'FIELD2'])
    filtered_fields = filter.included_fields(original_fields)

2. Add fields one by one:
    filter = FieldFilter()
    filter.add_excluded_field('FIELD1')
    filter.add_excluded_field('FIELD2')
    filter.configure()
    filtered_fields = filter.included_fields(original_fields)

3. Method chaining:
    filtered_fields = (FieldFilter()
        .add_excluded_field('FIELD1')
        .add_excluded_field('FIELD2')
        .configure()
        .included_fields(original_fields))

Important Notes:
---------------
- Must call configure() before using included_fields()
- Field names are case-insensitive
- If all excluded fields are removed, filter becomes unconfigured
- Clear all exclusions with clear_excluded_fields()
"""

class FieldFilter:
    def __init__(self):
        """Initialize an empty field filter"""
        #List of fields to remove
        self.excluded_fields = []
        self.is_configured = False

    def add_excluded_field(self, field_name: str):
        """
        Add a field to exclusion list
        
        Args:
            field_name: Name of the field to exclude
            
        Returns:
            self: For method chaining
            
        Example:
            filter.add_excluded_field('FIELD1')
        """
        field_name = field_name.lower()
        if field_name not in self.excluded_fields:
            self.excluded_fields.append(field_name)
        return self  # Return self for method chaining

    def remove_excluded_field(self, field_name: str): 
        """
        Remove a field from exclusion list
        
        Args:
            field_name: Name of the field to remove
            
        Returns:
            self: For method chaining
            
        Note:
            If this removes the last field, filter becomes unconfigured
        """
        field_name = field_name.lower()
        if field_name in self.excluded_fields:
            self.excluded_fields.remove(field_name)

        # If no more excluded fields, mark as not configured
        if not self.excluded_fields:
            self.is_configured = False
        
        return self  # Return self for method chaining  
    
    def clear_excluded_fields(self):
        """
        Remove all fields from exclusion list
        
        Note:
            This also marks the filter as unconfigured
        """
        self.excluded_fields = []
        self.is_configured = False  # Reset configuration flag
        
    def configure(self, fields_to_exclude: list[str] = None):
        """
        Configure filter and mark as ready to use
        
        Args:
            fields_to_exclude: Optional list of fields to exclude
            
        Returns:
            self: For method chaining
            
        Examples:
            # Configure with fields
            filter.configure(['FIELD1', 'FIELD2'])
            
            # Or just mark as configured after adding fields
            filter.add_excluded_field('FIELD1')
            filter.configure()
        """
        if fields_to_exclude:
            for field in fields_to_exclude:
                self.add_excluded_field(field)
        
        self.is_configured = True
        return self     
    
    def included_fields(self, fields: list) -> list :
        """
        Get list of fields excluding the ones marked for exclusion
        
        Args:
            fields: List of field dictionaries from DBF
            
        Returns:
            list: New list with excluded fields removed
            
        Raises:
            ValueError: If filter is not configured
            
        Example:
            fields = [
                {'name': 'FIELD1', 'type': 'C', 'length': 10},
                {'name': 'FIELD2', 'type': 'N', 'length': 5}
            ]
            included = filter.included_fields(fields)
        """
        if not self.is_configured:
            raise ValueError("Must call configure() before filtering fields")

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