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
    directory : Path = Configuration.TEMPORARY /'raw-videos'
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
            posts, 0
        ):
            executor.submit(
                __MPD, number, url, directory
            )
