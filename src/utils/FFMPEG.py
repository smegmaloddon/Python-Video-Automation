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
        check=True,
        stdout=subprocess.DEVNULL if hide else subprocess.PIPE,
        stderr=subprocess.DEVNULL if hide else subprocess.PIPE
    )

def Length(
    path : Path = None
) -> float:
    
    # verify 'path'
    assert path is not None and path.exists(), 'Path does not fit requirements'

    # build process
    process : list = [
        Configuration.FFPROBE,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(
            path
        )
    ]

    # fetch result
    result = subprocess.run(
        process,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    # return only the length
    return float(
        result.stdout.strip()
    )

def Audio(
    path : Path
) -> bool:
    
    # verify 'path'
    assert path is not None and path.exists(), 'Path must exist'

    # build process
    process : list = [
        Configuration.FFPROBE,
        '-v', 'error',
        '-select_streams', 'a',
        '-show_entries', 'stream=index',
        '-of', 'csv=p=0',
        str(
            path
        )
    ]

    result = subprocess.run(
        process,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    # return True /or False
    return bool(
        result.stdout.strip()
    )