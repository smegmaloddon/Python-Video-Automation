# imports
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# user imports 
from src.utils import Configuration, Temporary, FFMPEG, UUID, Directory

# functions
def __Convert(
    video : Path,
    filter : tuple
) -> None:
    
    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'
    
    # build process
    process: list[str] = [
        Configuration.FFMPEG,
        '-i', str(video),

        *filter,

        '-map', '0:v',
        '-map', '0:a?',

        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '128k',

        str(output),
    ]

    # run the process
    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=video,
        new=output
    )

def Run(
    videos : list[Path],
    ratio : str = '9x16' # pre-set to 9x16 AspectRatio
) -> None:
    
    # verify parameters
    assert videos is not None and len(
        videos 
    ) != 0 and ratio is not None

    # setup different aspect ratios
    dictionary: dict = {
        '9x16': ('-vf', "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)'"),
        '16x9': ('-vf', "crop='min(iw,ih*16/9)':'min(ih,iw*9/16)'")
    }

    # fetch ratio process line & confirm
    filter : tuple = dictionary.get(
        ratio, None
    )
    assert filter is not None, 'Aspect Ratio does not exist'

    # thread downloads for speed
    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:
        
        # create futures list
        futures : list = [
            executor.submit(
                __Convert, video, filter
            )
            for video in videos
        ]

        # wait
        for future in futures:

            future.result()