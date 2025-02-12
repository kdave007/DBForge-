from models.field_filter import FieldFilter

def test_field_filter():
    """Test FieldFilter functionality"""
    print("\nTesting FieldFilter:")
    print('-' * 50)
    
    # Test 1: Basic configuration
    print("\nTest 1: Basic configuration")
    filter = FieldFilter()
    filter.configure(['FIELD1', 'FIELD2'])
    print(f"Excluded fields: {filter.excluded_fields}")
    print(f"Is configured: {filter.is_configured}")
    
    # Test 2: Add/Remove fields
    print("\nTest 2: Add/Remove fields")
    filter = FieldFilter()
    filter.add_excluded_field('FIELD1')
    filter.add_excluded_field('FIELD2')
    print(f"After adding: {filter.excluded_fields}")
    
    filter.remove_excluded_field('FIELD1')
    print(f"After removing FIELD1: {filter.excluded_fields}")
    print(f"Is configured: {filter.is_configured}")
    
    # Test 3: Clear fields
    print("\nTest 3: Clear fields")
    filter.clear_excluded_fields()
    print(f"After clearing: {filter.excluded_fields}")
    print(f"Is configured: {filter.is_configured}")
    
    # Test 4: Filter actual fields
    print("\nTest 4: Filter fields")
    # Sample fields like they would come from DBF
    sample_fields = [
        {'name': 'FIELD1', 'type': 'C', 'length': 10},
        {'name': 'FIELD2', 'type': 'N', 'length': 5},
        {'name': 'FIELD3', 'type': 'C', 'length': 15}
    ]
    
    filter.configure(['FIELD1', 'FIELD2'])
    filtered = filter.included_fields(sample_fields)
    print("\nOriginal fields:")
    for f in sample_fields:
        print(f"- {f['name']}")
    
    print("\nFiltered fields (excluded FIELD1, FIELD2):")
    for f in filtered:
        print(f"- {f['name']}")
    
    # Test 5: Method chaining
    print("\nTest 5: Method chaining")
    filter = (FieldFilter()
        .add_excluded_field('FIELD1')
        .add_excluded_field('FIELD2')
        .configure())
    print(f"Excluded fields after chaining: {filter.excluded_fields}")

def test_error_handling():
    """Test error cases"""
    print("\nTesting Error Handling:")
    print('-' * 50)
    
    # Test 1: Try to filter without configuring
    print("\nTest 1: Filter without configure")
    filter = FieldFilter()
    filter.add_excluded_field('FIELD1')
    
    try:
        filter.included_fields([{'name': 'TEST'}])
        print("Error: Should have raised ValueError")
    except ValueError as e:
        print(f"Success: Caught expected error - {e}")

if __name__ == "__main__":
    test_field_filter()
    test_error_handling()
