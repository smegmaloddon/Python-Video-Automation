# imports
from pathlib import Path
import shutil
import random

# user imports
from src.utils import Directory, Configuration, Temporary, Threads, Title, Keywords, FFMPEG
from src.pipelines.video import Trim, Speed, Merge, Ratio, Normalise
from src.pipelines.web import Posts, Rank
from src.pipelines.audio import Music
from src.helpers import Download, Selector, Separators, Rankings

# constants
DEFAULT_LIST_COUNT : list = [8, 24]
DEFAULT_LIST_LENGTH : list = [8, 12]
AMOUNT_OF_KEYWORDS_FOR_TITLE : int = 8

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

    # fetch videos path
    path : Path = Configuration.TEMPORARY /'videos'

    # fetch video length
    length : int = Temporary.content['video'].get(
        'length', DEFAULT_LIST_LENGTH # default to list
    )
    length = length[1] if not Temporary.shorts else length[0] # select either short-form or long-form length

    # fetch the best part of each video
    selectors : list[dict] = Selector.Run(
        videos=[
            video for video in sorted(path.iterdir())
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

    # fetch aspect ratio depending on if shorts /or long-form
    ratio : str = '9x16' if Temporary.shorts else '16x9'

    # format into shorts /or long-form
    Ratio.Run(
        videos=[
            video for video in sorted(path.iterdir())
        ], # fetch paths of videos
        ratio=ratio
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

        for video in sorted(path.iterdir()):

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
            sorted(path.iterdir()), 0
        ):
            
            # create new path & copy separator to it
            selected : Path = Configuration.TEMPORARY /'separators' /f'separator-{number}.mp4'
            
            shutil.copy2(
                Configuration.TEMPORARY /'separator.mp4',
                selected
            ) # this is done since ffmpeg cant work with one file, multiple times

        # create merge list --[video-1, separator-1, video-2, separator-2]
        for number, video in enumerate(
            sorted(path.iterdir()), 0
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
            video for video in sorted(path.iterdir())
        ]

    # normalise each video before merge
    arguments : list = []
    for video in path.iterdir():

        arguments.append(

            {

                'path': video
            }
        )

    # thread normalise
    Threads.Thread(
        func=Normalise.Normalise,
        items=arguments
    )

    # add background music to videos if required
    arguments : list = []
    for video in path.iterdir():

        silent : bool = FFMPEG.SilenceThreshold(
            path=video
        )
        if not silent:

            continue

        # add video
        arguments.append(

            {

                'file': video
            }
        )

    # add in threads
    Threads.Thread(
        func=Music.BackgroundMusic,
        items=arguments
    )

    # merge
    Merge.Videos(
        videos=merge
    )

    # normalise at the end of merge
    Normalise.Normalise(
        path=Configuration.TEMPORARY /'video.mp4'
    )

    # create keywords table
    keywords : list = []
    for number in range(
        AMOUNT_OF_KEYWORDS_FOR_TITLE
    ):
        
        # fetch a keyword
        keyword : str = Keywords.Keywords(
            text=random.choice(
                seq=posts
            )['title']
        )

        # insert
        keywords.append(
            keyword
        )

    # add rankings
    if Temporary.content['video'].get(
        'rank-config', None
    ) != None:
        
        # add 1 -> 5 rank
        Rankings.Run(
            posts=posts,
            videos=list( # process videos into sorted list
                sorted(
                    path.iterdir() 
                )
            )
        )

        # add hook
        Rankings.Title()

    # avoid ai usage for debug
    if 1==1:

        return

    # fetch video title
    title : str = Title.Run(
        data={

            'Videos Used': len(
                list(
                    path.iterdir()
                )
            ),
            'Keywords /Topics': keywords
        } # present data to use
    )
    print(title)

    

    