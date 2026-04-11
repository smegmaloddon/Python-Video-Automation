# imports
import random
import math

# functions
def Clamp(
    number : float,
    lowest : float = 0.0,
    highest : float = 1e38
) -> float:
    
    # verify variables are correct datatypes
    assert number is float and lowest is float and highest is float, 'Parameter does not meet the correct requirements'

    # clamp
    placeholder : float = max(
        lowest, min(
            number, highest
        )
    ) if number else 0 # fallback

    return placeholder