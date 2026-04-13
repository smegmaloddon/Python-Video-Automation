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
        '-y',

        '-f', 'concat',
        '-safe', '0',
        '-fflags', '+genpts+discardcorrupt',
        '-avoid_negative_ts', 'make_zero',
        '-i', str(document),

        '-vf', 'fps=30',

        '-fps_mode', 'cfr',

        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-x264-params', 'keyint=60:min-keyint=60:scenecut=0',

        '-af', 'aresample=async=1:first_pts=0,asetpts=PTS-STARTPTS',

        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-ac', '2',

        '-movflags', '+faststart',
        '-max_muxing_queue_size', '9999',

        str(output)
    ]

    FFMPEG.Run(
        process=process
    )

    
