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
    process : list = [
        Configuration.FFMPEG,
        '-i', video,
        *filter,
        '-c:a', 'copy',
        output
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
    ratio : str = None
) -> None:
    
    # verify parameters
    assert videos is not None and len(
        videos 
    ) != 0 and ratio is not None

    # setup different aspect ratios
    dictionary : dict = {

        '9x16': ('-vf', 'crop=iw:iw*16/9'),
        '16x9': ('-vf', 'crop=ih*16/9:ih')
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
        
        for video in videos:

            executor.submit(
                __Convert, video, filter
            )