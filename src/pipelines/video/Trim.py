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

        # input first
        '-i', str(path),

        # 🔥 accurate seeking (frame-safe)
        '-ss', str(start),
        '-t', str(duration),

        # video re-encode
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # audio re-encode
        '-c:a', 'aac',
        '-b:a', '192k',

        # 🔥 force proper sync
        # '-af', 'aresample=async=1', # possible audio-sync issues

        # timestamp safety
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