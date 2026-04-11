# imports
from pathlib import Path

# user imports
from src.utils import JSON5, Directory, Configuration, Temporary
from src.workflows.shorts import Videos

def __Fetch(
    channel : str
) -> None:
    
    # update channel & content
    Temporary.channel = channel
    
    # fetch correct dictionary
    dictionary : dict = JSON5.Read(
        path=Configuration.DATA /'configuration.json5'
    )
    dictionary = dictionary.get(
        Temporary.channel, None
    )

    # error handling
    if dictionary == None:

        raise KeyError(
            'Content not found'
        )
    
    Temporary.content = dictionary

def Run(
) -> None:
    
    # placeholder channel variable
    channel : str = 'placeholder-channel'
    
    # edit & fetch data for Temporary.py
    __Fetch(
        channel=channel
    )

    Videos.Run()

# entry
if __name__ == '__main__':

    # temporary cleanse
    Directory.Cleanse(
        folder=Configuration.TEMPORARY
    )

    Run()