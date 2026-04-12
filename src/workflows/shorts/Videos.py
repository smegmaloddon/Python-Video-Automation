# imports
from pathlib import Path

# user imports
from src.utils import Directory, Configuration, Temporary, Threads
from src.pipelines.video import Trim, Speed, Merge, Ratio
from src.pipelines.web import Posts, Rank
from src.helpers import Download, Selector, Separators

# constants
DEFAULT_LIST_COUNT : list = [8, 24]
DEFAULT_LIST_LENGTH : list = [8, 12]

# functions
def Run(
) -> None:
    
    # fetch video count
    target : int = Temporary.content['video'].get(
        'count', DEFAULT_LIST_COUNT # default to list
    )
    target = target[1] if not Temporary.shorts else target[0] # select either short-form or long-form count
    
    # fetch posts & rank
    posts : list[dict] = Posts.Fetch(
        archive=Temporary.content['web']['archive'], # send subreddits to fetch data from,
        video=True, # only require videos,
        requirement=target
    )
    posts = Rank.Rank(
        posts=posts,
        requirement=target
    )

    # download posts[] to temp /raw-videos
    Download.Posts(
        posts=posts
    )

    # fetch aspect ratio depending on if shorts /or long-form
    ratio : str = '9x16' if Temporary.shorts else '16x9'

    # fetch videos path
    path : Path = Configuration.TEMPORARY /'videos'

    # format into shorts /or long-form
    Ratio.Run(
        videos=[
            video for video in path.iterdir()
        ], # fetch paths of videos
        ratio=ratio
    )

    # fetch video length
    length : int = Temporary.content['video'].get(
        'length', DEFAULT_LIST_LENGTH # default to list
    )
    length = length[1] if not Temporary.shorts else length[0] # select either short-form or long-form length

    # fetch the best part of each video
    selectors : list[dict] = Selector.Run(
        videos=[
            video for video in path.iterdir()
        ], # fetch paths of videos
        between=length /2 # <- & ->
    )

    # loop through & format
    arguments : list = []
    for selector in selectors:

        # fetch start & end
        start : float = selector['Start']
        end : float = selector['End']

        # fetch path
        video : Path = selector['Path']

        # add to arguments
        arguments.append(
            {

                'path': video,
                'start': start,
                'end': end
            }
        )

    # thread funcs with **arguments for efficiency
    # trim videos
    Threads.Thread(
        func=Trim.Run,
        items=arguments
    )

    # fetch video speed
    speed : float = Temporary.content['video'].get(
        'speed', None # default to None
    )

    # speed might not be included
    if speed != None:

        speed = speed[1] if not Temporary.shorts else speed[0] # select either short-form or long-form speed

        # prepare Speed.py arguments
        arguments : list = [] # reset

        for video in path.iterdir():

            # add argument for index of path.iterdir()
            arguments.append(

                {

                    'path': video,
                    'multiplier': speed
                } 
            )

        # thread functions
        Threads.Thread(
            func=Speed.Speed,
            items=arguments
        )
        
        # fetch separator config /or ignore
        separator : {} | None = Temporary.content['video'].get(
            'separator-config', None
        )
        if separator:

            # create neccessary separator files
            Separators.Run()
