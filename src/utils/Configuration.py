# imports
from pathlib import Path

# paths
DIRECTORY : Path = Path.cwd()
SOURCE : Path = DIRECTORY /'src'

DATA : Path = DIRECTORY /'data'
TEMPORARY : Path = DIRECTORY /'temp'
ASSETS : Path = DIRECTORY /'assets'
BIN : Path = DIRECTORY /'bin'

# ffmpeg executable paths
FFMPEG : Path = BIN /'video' /'bin' /'ffmpeg.exe'
FFPROBE : Path = BIN /'video' /'bin' /'ffprobe.exe'
FFPLAY : Path = BIN /'video' /'bin' /'ffplay.exe'