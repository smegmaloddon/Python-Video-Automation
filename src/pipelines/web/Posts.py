# imports
import requests
import random
import time
from pathlib import Path

# user imports
from src.utils import Temporary, Configuration

# constants
TIME_LIST : list[str] = [

    # 'day',
    # 'week',
    'month',
    'year',
    'all'
]
QUERY_LIST: list[str] = [

    'hot', 
    'new',
    'top',
    'rising',
    # 'controversial'
]
TIME_DELAY : float = 0.75
HEADERS : dict[str : str] = {
    'User-Agent': 'my-reddit-app/0.1'
}

# functions
def __Request(
    archive : list 
) -> list:
    
    # avoid using proxies
    time.sleep(
        TIME_DELAY
    )
    
    # fetch random subreddit to scrape
    page : str = random.choice(
        seq=archive
    )

    # fetch url parameters
    timezone : str = random.choice(
        seq=TIME_LIST
    )
    query : str = random.choice(
        seq=QUERY_LIST
    )
    
    # build url & send
    url : str = f'https://www.reddit.com/r/{page}/{query}.json?t={timezone}'

    # await response & validate
    response : requests.Response = requests.get(
        url, headers=HEADERS
    )

    # request failed, try again
    if response.status_code !=200:
        
        print(
            f'failed : {url}'
        )
        return []

    # convert to .json & fetch list of posts
    data : dict = response.json()
    placeholder : list = [
        post['data']
        for post in data['data']['children']
    ]

    return placeholder

def __Filter(
    posts : list
) -> None:
    
    # init selected
    selected : list = []

    # loop through posts
    for post in posts:

        boolean : bool = post.get(
            'is_video', False
        )
        if boolean:

            # add video formatted post to selected
            selected.append(
                post
            )

    return selected

def Fetch(
    archive : list,
    video : bool = False,
    requirement : int = 48 # requirement but not a limit
) -> list[dict]:
    
    # verify 'archive'
    assert archive != None and len(
        archive
    ) != 0 

    # init variables
    selected : list[dict] = []
    previous : list[str] = [] # TODO : set to posts.json5

    flag : bool = True
    while flag:

        posts : list = __Request(
            archive=archive
        )

        # filter to only video formatted posts
        if video:

            posts = __Filter(
                posts=posts
            )
        
        # filter already selected videos
        placeholder : list = []
        for post in posts:

            # fetch & search list for previous post id
            unique : str = post['id']
            if not unique in previous:

                # append respectfully
                previous.append(
                    unique
                )
                placeholder.append(
                    post
                )

        # merge lists
        selected = selected +placeholder

        # check flag requirements
        if len(
            selected
        ) >=requirement:
            
            # end while loop
            flag = False
            break

    return selected