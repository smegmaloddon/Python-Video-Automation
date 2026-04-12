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
    assert all(
        isinstance(
            value, (int, float)
        ) for value in (
            number, lowest, highest)
        ), 'Parameters must be numeric'

    # clamp
    placeholder : float = max(
        lowest, min(
            number, highest
        )
    ) if number else 0 # fallback

    return placeholder