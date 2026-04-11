# imports
from pathlib import Path

# user imports
from src.utils import Directory, Configuration, Temporary
from src.pipelines.video import Trim, Speed, Merge, Ratio
from src.pipelines.web import Posts, Rank
from src.helpers import Download

# constants
DEFAULT_LIST_COUNT : tuple = [8, 24]

# functions
def Run(
) -> None:
    
    # fetch video count
    target : int = Temporary.content['video'].get(
        'count', DEFAULT_LIST_COUNT # default to tuple
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

    Download.Posts(
        posts=posts
    )
    