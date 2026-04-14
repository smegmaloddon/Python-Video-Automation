# imports
from pathlib import Path
import random

# user imports
from src.utils import Configuration, Temporary, UUID, FFMPEG, Directory, Keywords, Hex
from src.helpers import Prompt

# constants
COLORS : list[str] = [

    # gold
    "\#FFDC51",

    # silver
    "\#F1F1F1",

    # bronze
    "\#FF9152"
]
DEFAULT_PIXEL_VERTICAL_GAP : int = 26
DEFAULT_PIXEL_HORIZONTAL_GAP : int = 24
TEXT_GAP_ACROSS_PIXELS : int = 24
START_PIXEL_GAP : int = 72
FONT : str = 'C\\:/Windows/Fonts/arial.ttf'
FONT_SIZE : int = 48
HOOKS_LIST: list[str] = [
    'Wait till #1',
    '#1 is insane',
    'Watch #1 carefully',
    '#1 will shock you',
    'Starting from #5',
    '#3 is crazy',
    '#2 gets worse',
    '#1 is next level',
    'Don’t skip #2',
    'Wait for #1',
    'Ending changes everything',
    'Stay till end',
    'It escalates fast',
    'Final one hits hard',
    'Only #1 matters',
    'Most miss #1',
    'Watch till end',
    'Last one wins',
    'This is insane',
    'You missed #1',
    'Ranking from worst',
    'Best saved for #1',
    'Keep watching #1',
    'Top one is wild',
    'Final is shocking',
    'You wont expect #1',
    'Wait for ending',
    'This is crazy',
    'Don’t miss last',
    'Last one best',
    'Number one hits',
    'Watch carefully #1',
    'Ending goes hard',
    'This gets intense',
    'Only legends reach #1',
    'Last one insane',
    'Wait until #1'
]

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

        # fetch pixels vertical
        pixels : int = Temporary.content['video']['rank-config'].get(
            'vertical-pixels', DEFAULT_PIXEL_VERTICAL_GAP
        )

        # fetch vertical
        vertical : str = (
            number *pixels
        ) +START_PIXEL_GAP

        # fetch horizontal
        horizontal : int = Temporary.content['video']['rank-config'].get(
            'horizontal-pixels', DEFAULT_PIXEL_HORIZONTAL_GAP
        )

        # fetch font size
        size : int = Temporary.content['video'].get(
            'font-size', FONT_SIZE
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{number})':"
            f"x={horizontal}:y={vertical}:"
            f"fontsize={size}:"
            f"fontcolor={color}:"
            f"borderw=2:"
            f"bordercolor=black:"
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
        vertical : int = Temporary.content['video']['rank-config'].get(
            'vertical-pixels', DEFAULT_PIXEL_VERTICAL_GAP
        )
        vertical = (
            rank *vertical
        ) +START_PIXEL_GAP # add start pixel position2

        # fetch horizontal
        horizontal : int = Temporary.content['video']['rank-config'].get(
            'horizontal-pixels', DEFAULT_PIXEL_HORIZONTAL_GAP
        )

        # fetch gap
        gap : int = Temporary.content['video']['rank-config'].get(
            'horizontal-pixel-gap', TEXT_GAP_ACROSS_PIXELS
        )

        # fetch length of video
        length : float = FFMPEG.Length(
            path=video
        )

        # custom font size
        __size : int = max(
            16, min(
                size, int(
                    1200 /len(keyword)
                )
            )
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{keyword.upper()}':"
            f"x={horizontal +gap} + 2*sin(10*(t-{duration})):"
            f"y={vertical} + 1*sin(12*(t-{duration})):" # wobble effect
            f"fontcolor={color}:"
            f"borderw=2:"
            f"bordercolor=black:"
            # f"box=1:" # overlaps too much & creates z-index issues
            # f"boxcolor=black@0.25:"
            # f"boxborderw=14:"

            # 🔥 animation block (0.4s pop)
            f"fontsize='if(lt(t,{duration}+0.4),"
            f"{__size}*pow((t-{duration})/0.4,0.35),"
            f"{__size})':"

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

def Title(
) -> None:
    
    # fetch random hook
    text : str = random.choice(
        seq=HOOKS_LIST
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

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # open & write to file --> bypass ffmpeg issues
    with open(
        file=Configuration.TEMPORARY /'title.txt',
        mode='w',
        encoding='utf-8'
    ) as file:
        
        file.write(
            text.upper()
        )
        file.close()

    # fetch path
    path : str = FFMPEG.ConvertPath(
        path=Configuration.TEMPORARY /'title.txt'
    )

    # init start & end
    start : float = 0.125
    end : float = 2

    # fetch font size 
    size : int = max(
        18, min(
            26, int(
                1200 /len(text)
            )
        )
    )

    # colors & fetch color
    colors : list[str] = [

        "#3CFF42", "#FF5050", "#5D68FF", "#FF4AF0", "#FFFB00"
    ]
    color : str = random.choice(
        seq=colors
    )

    # create accent
    accent : str = Hex.Darken(
        color=color
    )

    # create animation
    animation: str = (
        f"drawtext="
        f"fontfile='{font}':"
        f"textfile='{path}':"
        f"fontcolor='{color}':"
        f"fontsize={size}:"
        f"box=1:"
        f"boxcolor={color}@0.45:"
        f"boxborderw=14:"
        f"x=(w-text_w)/2:"
        f"y=(h*0.65)-th/2-20*sin(t*2):"
        f"borderw=5:bordercolor='{accent}':"
        f"alpha='if(lt(t,{end}-0.5),1,if(lt(t,{end}),({end}-t)/0.5,0))':"
        f"enable='between(t,{start},{end})'"
    )
        
    # fetch process
    process : list = [
        Configuration.FFMPEG,
        '-i', str(Configuration.TEMPORARY /'video.mp4'),
        '-vf',
        animation,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        str(
            output
        )
    ]

    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=Configuration.TEMPORARY /'video.mp4',
        new=output
    )


    