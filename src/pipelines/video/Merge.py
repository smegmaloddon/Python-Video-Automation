# imports
from pathlib import Path

# user imports
from src.utils import Configuration, Temporary, Directory, FFMPEG

# functions
def Videos(
    videos : list[Path] = None,
    output : Path = Configuration.TEMPORARY /'video.mp4'
) -> None:
    
    # verify 'videos'
    assert videos is not None and len(
        videos
    ) != 0, 'Videos should not be None /or empty'

    # init document
    document : Path = Configuration.TEMPORARY /'videos.txt'

    # create concat file for ffmpeg
    with open(
        file=document, 
        mode='w', 
        encoding='utf-8'
    ) as file:
        
        # write into video.txt
        for video in videos:

            file.write(
                f"file '{video.as_posix()}'\n"
            )

        file.close()

    # build process
    process = [
        Configuration.FFMPEG,

        # overwrite output safely
        '-y',

        # input concat demuxer (safe mode)
        '-f', 'concat',
        '-safe', '0',
        '-protocol_whitelist', 'file,http,https,tcp,tls',

        # input file
        '-i', str(document),

        # video re-encode (safe + compatible)
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # audio re-encode (standard safe AAC)
        '-c:a', 'aac',
        '-b:a', '192k',

        # enforce consistent timing
        '-r', '30',

        # MP4 streaming optimization
        '-movflags', '+faststart',

        # strict error handling
        '-fflags', '+genpts',
        '-avoid_negative_ts', 'make_zero',

        str(output),
    ]

    FFMPEG.Run(
        process=process
    )

    
