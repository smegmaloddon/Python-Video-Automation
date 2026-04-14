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
DEFAULT_PIXEL_VERTICAL_GAP : int = 26
DEFAULT_PIXEL_HORIZONTAL_GAP : int = 24
TEXT_GAP_ACROSS_PIXELS : int = 22
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
            f"text='{number})':"
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
    return placeholder

def Run(
    posts : list[dict],
    videos : list[Path]
) -> None:
    
    # verify parameters
    assert posts is not None and videos is not None

    # init lists
    __posts : list = []

    # delete possible mismatches
    for number, video in enumerate(
        videos, 0
    ):
        
        # check if video exists
        present : Path = Configuration.TEMPORARY /'videos' /f'video-{number}.mp4'
        if not present.exists():

            continue
        
        # add posts
        __posts.append(
            posts[number]
        )

    # swap variables
    posts = __posts

    # fetch count of videos
    count : int = len(
        videos
    )

    # create pseudo numbers for ranks
    ranks : str = __CreateRanks(
        count=count
    )

    # fetch ranking numbers, != 1
    numbers : list[int] = [
        number for number, _ in enumerate(
            videos, 1
        ) if number != 1
    ]

    # fetch font size
    size : int = Temporary.content['video'].get(
        'font-size', FONT_SIZE
    )

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

    # fetch separator length
    separator : dict = Temporary.content['video'].get(
        'separator-config', None
    )
    separator : float = separator.get(
        'length', 0
    ) if separator != None else 0 # fetch separator length with fallback

    # init filters & duration
    filters : list = []
    duration : float = 0

    # fetch total length
    total : float = FFMPEG.Length(
        path=Configuration.TEMPORARY /'video.mp4'
    )

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

        # fetch keywords & keyword
        keywords : list = Keywords.Keywords(
            text=posts[number]['title']
        )
        keyword : str = keywords[0] if len(
            keywords
        ) >=1 else 'huh, hey there!'

        # fetch color
        color = COLORS[rank -1] if rank -1 <len(
            COLORS # rank -1 since rank is integer too high 
        ) else 'white'

        # fetch vertical
        vertical : str = (
            rank
        ) *DEFAULT_PIXEL_VERTICAL_GAP

        # fetch length of video
        length : float = FFMPEG.Length(
            path=video
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{keyword.upper()}':"
            f"x={DEFAULT_PIXEL_HORIZONTAL_GAP +TEXT_GAP_ACROSS_PIXELS}:y={vertical}:"
            f"fontsize={size}:"
            f"fontcolor={color}:"
            f"borderw=4:"
            f"bordercolor=black:"
            f"enable='between(t,{duration},{total})'"
        )

        # set duration
        duration = duration +length +separator

    # combine filters
    filters.append(
        ranks
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

        # 🔥 FIX TIMESTAMP + INPUT SAFETY
        '-fflags', '+genpts+discardcorrupt',
        '-avoid_negative_ts', 'make_zero',
        '-i', str(Configuration.TEMPORARY / 'video.mp4'),

        # 🔥 VIDEO FILTERS
        '-vf', placeholder,

        # 🔥 FORCE CLEAN FRAME PIPELINE
        '-fps_mode', 'cfr',
        '-r', '30',

        # 🔥 VIDEO ENCODING (stable + widely compatible)
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # 🔥 AUDIO (FULL RE-ENCODE, NO GLITCHES)
        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-ac', '2',

        # 🔥 AUDIO FIX (this is the key you were missing)
        '-af', 'aresample=async=1:first_pts=0',

        # 🔥 SYNC SAFETY (prevents drift / freeze audio issues)
        '-async', '1',

        # 🔥 FINAL MP4 FIX
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


    
        
        

