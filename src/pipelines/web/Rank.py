# imports
from pathlib import Path

# functions
def Rank(
    posts : list[dict] = None,
    requirement : int = 8 # strict limit
) -> list[dict]:
    
    # verify posts != None
    assert posts is not None and len(
        posts
    ) != 0, 'Posts should not be None /or empty'

    # sort & return only requirement
    placeholder : list[dict] = sorted(
        posts, 
        key=lambda post: post['ups'], 
        reverse=True
    )
    placeholder = placeholder[:requirement]

    return placeholder