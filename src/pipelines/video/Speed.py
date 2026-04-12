# imports
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary, Directory, UUID, FFMPEG

# functions
def Speed(
    path : Path = None,
    multiplier : float = 2.0,
    ignore : bool = True # if video length is too small
) -> None:
    
    # verify 'path'
    assert path is not None and path.exists(), 'Parameters do not meet the requirements'

    # detect ignore
    if ignore:

        # fetch length of current video & maximum of possible settings
        length : float = FFMPEG.Length(
            path=path
        )
        contest : float = Temporary.content['video'].get(
            'length', [16, 24]
        )
        contest = contest[1] if not Temporary.shorts else contest[0] # select either short-form or long-form length

        # if video is under the config requirement for length of videos
        if length <=contest:

            return

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # build process
    process = [
        Configuration.FFMPEG,
        '-y',
        '-i', str(path),

        # 🔥 video speed (correct)
        '-filter:v', f'setpts=PTS/{multiplier}',

        # 🔥 audio speed (SAFE handling for atempo limits)
        '-filter:a', f'atempo={1 if multiplier <= 0 else multiplier}',

        # 🔥 re-encode video properly
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # 🔥 re-encode audio properly
        '-c:a', 'aac',
        '-b:a', '192k',

        # 🔥 timing + compatibility safety
        '-r', '30',
        '-fflags', '+genpts',
        '-avoid_negative_ts', 'make_zero',

        str(output),
    ]

    # run process
    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=path,
        new=output
    )