from typing import Callable

class TypeMapping:
    """
    Handles type conversion between DBF and PostgreSQL
    Field Types:
    C => char/varchar 
    N => numeric
    D => date
    L => boolean
    M => text (memo field in FPT/DBT)
    B => bytea (binary memo field)
    G => bytea (general binary field)
    F => double precision
    """
    _MAPPING: dict[str, Callable[[int, int], str]] = {
        'C': lambda f_length, f_decimal : f'VARCHAR({f_length})',
        'N': lambda f_length, f_decimal : f'NUMERIC({f_length},{f_decimal})' if f_decimal > 0 else f'NUMERIC({f_length})',
        'D': lambda f_length, f_decimal : 'DATE',
        'L': lambda f_length, f_decimal : 'BOOLEAN',
        'M': lambda f_length, f_decimal : 'TEXT',  # Memo field (text)
        'B': lambda f_length, f_decimal : 'BYTEA', # Binary memo field
        'G': lambda f_length, f_decimal : 'BYTEA', # General binary field
        'F': lambda f_length, f_decimal : 'DOUBLE PRECISION'
    }

    @classmethod
    def get_type(cls, dbf_type : str, length : int, decimal : int) -> str :
        """
        Get PostgreSQL type for given DBF field
        
        Args:
            dbf_type: DBF field type
            length: Field length
            decimal: Decimal places (for numeric fields)
            
        Returns:
            str: PostgreSQL data type
            
        Raises:
            ValueError: If DBF field type is not supported
        """
        dbf_type = dbf_type.upper()
        if dbf_type in cls._MAPPING:
            return cls._MAPPING[dbf_type](length,decimal)
        raise ValueError(f"Unsupported DBF field type: {dbf_type}")

    @classmethod 
    def add_mapping(cls, dbf_type : str, callback_function : callable) -> None :
        """
        Add or update a type mapping
        
        Args:
            dbf_type: DBF field type to map
            callback_function: Function that returns PostgreSQL type
            
        Raises:
            TypeError: If callback is not callable
        """   
        if not callable(callback_function):
            raise TypeError('callback must be a function')

        cls._MAPPING[dbf_type.upper()] = callback_function