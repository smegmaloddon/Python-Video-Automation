# imports
from pathlib import Path
import shutil

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

    # init merge list
    merge : list = []
    
    # fetch separator config /or ignore
    separator : dict | None = Temporary.content['video'].get(
        'separator-config', None
    )
    if separator:

        # create neccessary separator files
        Separators.Run()

        # create separator directory
        Path.mkdir(
            Configuration.TEMPORARY /'separators'
        )

        # loop through videos
        for number, video in enumerate(
            path.iterdir(), 0
        ):
            
            # create new path & copy separator to it
            selected : Path = Configuration.TEMPORARY /'separators' /f'separator-{number}.mp4'
            
            shutil.copy(
                Configuration.TEMPORARY /'separator.mp4',
                selected
            ) # this is done since ffmpeg cant work with one file, multiple times

        # create merge list --[video-1, separator-1, video-2, separator-2]
        for number, video in enumerate(
            path.iterdir(), 0
        ):

            merge.append(
                Configuration.TEMPORARY /'videos' /f'video-{number}.mp4'
            )
            merge.append(
                Configuration.TEMPORARY /'separators' /f'separator-{number}.mp4' # separator
            )

    # no separators, simple array
    else:

        merge : list = [
            video for video in path.iterdir()
        ]

    # merge
    Merge.Videos(
        videos=merge
    )
