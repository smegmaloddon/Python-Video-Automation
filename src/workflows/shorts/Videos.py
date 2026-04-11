# imports
from pathlib import Path

# user imports
from src.utils import Directory, Configuration, Temporary
from src.pipelines.video import Trim, Speed, Merge, Ratio
from src.pipelines.web import Posts

# constants
DEFAULT_TUPLE_COUNT : tuple = (8, 24)

# functions
def Run(
) -> None:
    
    target : int = Temporary.content['video'].get(
        'count', DEFAULT_TUPLE_COUNT # default to tuple
    )
    target = target[0] if not Temporary.shorts else target[1] # select either short-form or long-form count
    
    posts : list[dict] = Posts.Fetch(
        archive=Temporary.content['web']['archive'], # send subreddits to fetch data from,
        video=True, # only require videos,
        requirement=target
    )

    print(len(posts))