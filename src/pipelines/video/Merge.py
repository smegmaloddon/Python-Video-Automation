# imports
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary, Directory

# functions
def Videos(
    videos : list = None
) -> None:
    
    # verify 'videos'
    assert videos is not None and len(
        videos
    ) != 0, 'Videos should not be None /or empty'

    