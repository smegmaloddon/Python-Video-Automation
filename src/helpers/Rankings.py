# imports
from pathlib import Path
import random

# user imports
from src.utils import Configuration, Temporary, UUID, FFMPEG, Directory, Keywords

# constants
COLORS : list[str] = [

    # gold
    "\#FFDC51",

    # silver
    "\#E0E0E0",

    # bronze
    "\#FF9152"
]
DEFAULT_PIXEL_VERTICAL_GAP : int = 60
DEFAULT_PIXEL_HORIZONTAL_GAP : int = 45
TEXT_GAP_ACROSS_PIXELS : int = 25
FONT : str = 'C\\:/Windows/Fonts/arial.ttf'
FONT_SIZE : int = 48

# functions
def __CreateRanks(
    count : int = 0
) -> None:
    
    # init filters
    filters : list = []

    # fetch font
    font : str = Temporary.content['video'].get(
        'font', FONT
    )
    if font != FONT:

        # if custom font, find & convert to ffmpeg safe path
        font : Path = Configuration.ASSETS /'fonts' /f'{font}'
        if not font.exists():

            raise FileNotFoundError(
                'Font.ttf file not found'
            )
        
        font : str = FFMPEG.ConvertPath(
            path=font
        )

    # loop through count
    for number in range(
        count
    ):
        
        # fetch color
        color = COLORS[number] if number <len(
            COLORS
        ) else 'white'

        # update number
        number = number +1

        # fetch vertical
        vertical : str = (
            number
        ) *DEFAULT_PIXEL_VERTICAL_GAP

        # fetch font size
        size : int = Temporary.content['video'].get(
            'font-size', FONT_SIZE
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{number}':"
            f"x={DEFAULT_PIXEL_HORIZONTAL_GAP}:y={vertical}:"
            f"fontsize={size}:"
            f"fontcolor={color}:"
            f"borderw=4:"
            f"bordercolor=black"   
        )

    # create -vf string
    placeholder : str = ','.join(
        filters
    )

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # build process
    process = [
        Configuration.FFMPEG,
        '-y',
        '-i', str(Configuration.TEMPORARY / 'video.mp4'),

        '-vf', placeholder,

        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        '-vsync', 'cfr',

        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',

        '-movflags', '+faststart',

        str(output)
    ]

    # run process
    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=Configuration.TEMPORARY /'video.mp4',
        new=output
    )

def Run(
    posts : list[dict],
    videos : list[Path]
) -> None:
    
    # verify parameters
    assert posts is not None and videos is not None and len(
        posts
    ) == len(
        videos
    ) and len(
        videos 
    ) != 0, 'Parameters do not meet the requirements'

    # fetch count of videos
    count : int = len(
        videos
    )

    # create pseudo numbers for ranks
    __CreateRanks(
        count=count
    )

    # fetch ranking numbers, != 1
    numbers : list[int] = [
        number for number, _ in enumerate(
            videos, 1
        ) if number != 1
    ]

    # loop through videos
    for number, video in enumerate(
        videos
    ):
        
        # fetch rank & remove
        rank : int = 1

        # check that it shouldn't use rank 1
        if len(
            numbers
        ) != 0:
            
            rank : int = random.choice(
                seq=numbers
            )
            numbers.remove(
                rank
            )

        keywords : list = Keywords.Keywords(
            text=posts[number]['title']
        )
        keyword : str = keywords[0] if len(
            keywords
        ) >=1 else 'huh, hey there!'

        print(keyword, video.name, rank)

