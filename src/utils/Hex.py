# imports 
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary

# functions
def Darken(
    color: str, 
    factor: float = 0.4
) -> str:
    
    color = color.lstrip("#")

    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)

    return f"#{r:02x}{g:02x}{b:02x}"