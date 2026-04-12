# imports
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary, Directory, FFMPEG, UUID

# functions
def Run(
    path : Path,
    start : float = 0,
    end : float = 1
) -> None:
    
    # verify 'path'
    assert path is not None and path.exists(), 'Path does not exist /not given'

    # calculate duration & output path
    duration : float = end -start
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # build process
    process = [
        Configuration.FFMPEG,
        '-y',

        # input seeking (faster start)
        '-ss', str(start),
        '-i', str(path),

        # trim duration
        '-t', str(duration),

        # 🔥 re-encode video + audio (instead of stream copy)
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        '-c:a', 'aac',
        '-b:a', '192k',

        # 🔥 timestamp + compatibility safety
        '-fflags', '+genpts',
        '-avoid_negative_ts', 'make_zero',
        '-movflags', '+faststart',

        str(output)
    ]

    # run
    FFMPEG.Run(
        process=process
    )

    # replace path with output
    Directory.Replace(
        old=path,
        new=output
    )