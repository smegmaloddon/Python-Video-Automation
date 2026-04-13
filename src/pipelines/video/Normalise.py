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

        '-fflags', '+genpts+discardcorrupt',
        '-avoid_negative_ts', 'make_zero',
        '-i', str(path),

        # force clean video timing
        '-vf', 'fps=30',

        # FULL VIDEO RE-ENCODE
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # FULL AUDIO RESET (this is the important part)
        '-af', 'aresample=48000,asetpts=PTS-STARTPTS',

        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-ac', '2',

        # strict CFR enforcement
        '-fps_mode', 'cfr',

        # kill timestamp weirdness
        '-max_muxing_queue_size', '9999',
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