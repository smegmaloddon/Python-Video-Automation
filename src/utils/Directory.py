# imports
from pathlib import Path
import shutil

# functions
def Cleanse(
    folder : Path = None
) -> None:
    
    # verify 'folder' was provided & is not defaulted to None
    # verify 'folder' datatype is Path
    assert folder is not None and isinstance(
        folder, Path
    )



