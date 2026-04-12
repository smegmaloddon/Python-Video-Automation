# imports
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary, FFMPEG, Directory, UUID

def Normalise(
    path : Path = None
) -> None:
    
    # verify 'path'
    assert path is not None and path.exists(), 'Path should not be None /or empty'

    # init output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # build process
    process = [
        Configuration.FFMPEG,
        '-y',
        '-i', str(path),

        '-c:v', 'libx264',
        '-c:a', 'aac',

        '-r', '30',
        '-pix_fmt', 'yuv420p',
        '-vsync', 'cfr',

        '-af', 'aresample=async=1',

        '-movflags', '+faststart',

        str(output)
    ]

    # run process
    FFMPEG.Run(
        process=process
    )

    # replace
    Directory.Replace(
        old=path,
        new=output
    )