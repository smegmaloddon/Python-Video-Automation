# imports
from pathlib import Path
import shutil

# user imports
from src.utils import Configuration, Temporary, FFMPEG, UUID
from src.pipelines.video import Trim, Ratio

# create separator & neccessary components
def Run(
) -> None:
    
    # fetch configuration & variables
    configuration : dict = Temporary.content['video'].get(
        'separator-config', {}
    )
    
    # fetch video & check it exists
    video : str = configuration.get(
        'video', None
    )
    video : Path = Configuration.ASSETS /'videos' /'separators' /f'{video}'

    if not video.exists():

        raise FileNotFoundError()
    
    # copy file to temporary
    file : Path = Configuration.TEMPORARY /'separator.mp4'
    shutil.copy(
        str(video),
        str(file)
    )
    
    # fetch length & trim
    length : float = configuration.get(
        'length', 0.75
    )
    Trim.Run(
        path=file,
        start=0,
        end=length
    )

    # detect if shorts & format aspect ratio
    Ratio.Run(
        videos=[file],
        ratio='9x16' if Temporary.shorts else '16x9'
    )    
