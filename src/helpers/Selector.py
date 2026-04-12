# imports
from pathlib import Path
import numpy
import librosa
import random

# user imports
from src.utils import Configuration, Temporary, FFMPEG, Math

def __FetchAudio(
    path : Path,
    duration : float = 1.0
) -> list:
    
    # fetch y & sr
    y, sr = librosa.load(
        path=path
    )
    
    # fetch chunk size
    size : int = int(
        sr *duration
    )

    # init energies
    energies = []

    # loop
    for number in range(
        0, len(
            y
        ), size
    ):
        
        chunk = y[number:number +size]
        if len(chunk) == 0:
            continue
        
        # RMS == loudness
        calculation : float = numpy.sqrt(
            numpy.mean(
                chunk**2
            )
        )
        energies.append(
            calculation
        )

    return energies

# groups scores together, more easily finds payoffs
def __Peaks(energies, distance=75):
    peaks = []
    
    sorted_peaks = sorted(
        enumerate(energies),
        key=lambda x: x[1],
        reverse=True
    )

    used = set()

    for i, score in sorted_peaks:
        if any(abs(i - u) < distance for u in used):
            continue

        peaks.append((i, score))
        used.add(i)

    return peaks[0]

def __RankAudio(
    energies : list
) -> list:
    
    # rank energies
    ranked : list = sorted(
        enumerate(
            energies
        ),
        key=lambda value: value[1],
        reverse=True
    )[0] # fetch only the best

    return ranked

def __ExtractAudio(
    path : Path
) -> bool:
    
    # decide if video has audio & return False
    audio : bool = FFMPEG.Audio(
        path=path
    )
    if not audio:

        return False
    
    # build process
    process = [
        Configuration.FFMPEG,
        '-y',

        '-i', str(path),

        # 🔥 more tolerant decoding (important)
        '-fflags', '+discardcorrupt',
        '-err_detect', 'ignore_err',

        # no video
        '-vn',

        # 🔥 optional audio (won’t crash if missing)
        '-map', '0:a?',

        # 🔥 force proper decoding (more stable than copy)
        '-c:a', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',

        # 🔥 overwrite-safe + consistent output
        str(
            Configuration.TEMPORARY /'audio-extract.wav'
        )
    ]

    # run process with ffmpeg
    FFMPEG.Run(
        process=process
    )

    return True

def Run(
    videos : list = None,
    between : float = 4
) -> None:
    
    # verify 'videos'
    assert videos is not None and len(
        videos
    ) != 0

    # init placeholder
    placeholder : list = []

    # loop through video paths
    for path in videos:

        # fetch length of video
        length : float = FFMPEG.Length(
            path=path
        )

        boolean : bool = __ExtractAudio(
            path=path
        )
        if not boolean:

            # fetch requirements for truely random dictionary
            # audio not present -> fallback
            start : float = length -(
                between *2
            )
            start = random.uniform(
                0, start
            )

            end : float = start +(
                between *2
            )
            
            # add to placeholder
            placeholder.append(
                {
                    'Path': path,
                    'Start': start,
                    'End': end 
                }
            )

            # do not finish this loop iteration
            continue

        # fetch energies for specific video
        energies : list[float] = __FetchAudio(
            path=Configuration.TEMPORARY /'audio-extract.wav'
        )

        # fetch ranked audio & length of video
        selected : float = __Peaks(
            energies=energies
        )

        # fetch filtered start & end
        start : float = Math.Clamp(
            number=selected[0] -between,
            lowest=0.0, # lowest possible start time is 0
            highest=length # highest possible is video length
        )
        end : float = Math.Clamp(
            number=selected[0] +between,
            lowest=0.0, # lowest possible start time is 0
            highest=length # highest possible is video length
        )

        # build placeholder with dicts
        placeholder.append(
            {
                'Path': path,
                'Start': start,
                'End': end
            }
        )

    return placeholder
