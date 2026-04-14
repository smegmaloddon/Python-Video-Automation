# imports
from pathlib import Path
import random
import requests

# user imports
from src.utils import Configuration, Temporary, FFMPEG, UUID, Directory
from src.helpers import Download

# constants
PIXABAY_API_KEY : str = '53636883-18dd4c5344673acec1a9a2a12'

# functions
def BackgroundMusic(
    file : Path,
    parameters : list = [
        'funk'
    ]
) -> None:
    
    # verify parameters
    assert file is not None and file.exists(), 'File does not fit requirements'

    # build url
    url : str = f'https://pixabay.com/music/search/funk/'

    # build parameters
    parameters = {
        "key": PIXABAY_API_KEY,
        # "q": "funk",
        # # "media_type": "music",
        # "per_page": 50
    }

    # fetch response
    response = requests.get(
        url
        # params=parameters
    )
    data = response.json()

    # fetch tracks
    tracks : dict = data['hits']
    print(tracks)
    track : dict = random.choice(
        seq=tracks
    )

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp3'

    # fetch & download audio
    audio : str = track['audio_url']
    Download.Audio(
        url=audio,
        output=output
    )
