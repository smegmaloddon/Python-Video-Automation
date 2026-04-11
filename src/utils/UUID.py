# imports 
import uuid

# user imports
from src.utils import Math

# constants
LOWEST_UUID : int = 1
HIGHEST_UUID : int = 5

# functions
def Create(
    number : int = 4
) -> str:
    
    # verify 'number' is an integer
    assert number is int, 'Parameter should be an integer'

    # clamp using constants & number
    number = Math.Clamp(
        number=number,
        lowest=LOWEST_UUID,
        highest=HIGHEST_UUID
    )
    
    # build function key
    func : str = f'uuid{number}'

    # fetch uuid
    placeholder : str = uuid[func]()

    return placeholder