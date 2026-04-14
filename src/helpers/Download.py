# imports
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests

# user imports
from src.utils import Temporary, Configuration
from src.utils import FFMPEG

# functions
def __MPD(
    number : int,
    url : str,
    directory : Path
) -> None:
    
    process : list = [
        Configuration.FFMPEG,
        '-i', url,
        '-c', 'copy',
        str( 
            directory /f'video-{number}.mp4'
        )
    ]

    FFMPEG.Run(
        process=process
    )

# fetch .mpd posts of videos and download
def Posts(
    posts : list[dict],
    directory : Path = Configuration.TEMPORARY /'videos'
) -> None:
    
    # verify 'posts'
    assert posts is not None and len(
        posts
    ) != 0, 'Posts parameter does not meet the requirements'

    # create directory
    Path.mkdir(
        directory
    )

    # fetch .mpds
    mpds : list = [
        post['media']['reddit_video']['dash_url']
        for post in posts
    ]

    # thread downloads for speed
    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:
        
        for number, url in enumerate(
            mpds, 0
        ):
            
            executor.submit(
                __MPD, number, url, directory
            )

def Audio(
    url : str,
    output : Path
) -> None:
    
    # verify
    assert url is not None and output is not None and output.exists(), 'Parameters do not meet the requirements'

    # fetch & save audio
    data : any = requests.get(
        url=url
    ).content

    with open(
        file=output,
        mode='wb'
    ) as file:
        
        file.write(
            data
        )