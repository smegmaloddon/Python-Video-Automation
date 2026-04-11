# imports
from pathlib import Path
import subprocess

# user imports
from src.utils import Temporary, Configuration

# functions
def Run(
    process : list = None,
    hide : bool = True
) -> None:
    
    # verify 'process'
    assert process is not None, 'Process must not be None'

    subprocess.run(
        process,
        check=True
    )