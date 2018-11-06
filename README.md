# Vapoursynth mingw library creator script
#### written in Python

Creates MinGW compatible library files of the Vapoursynth DLLs using gendef/dlltool, for people unable to cross compile it.

VS Source: https://github.com/vapoursynth/vapoursynth

### Supports:
 - VapourSynth R37,38,39,40,41,42,42.1,43,44,45+ - Win64 and 32 (Only tested the 64bit variant)

### Requires: 
 - gendef (part of MinGW)
 - dlltool (so is this)
 - Python 2(+)

### How to run:

    make PREFIX={INSTALL_FOLDER} GENDEF={FULL_PATH_TO_GENDEF} DLLTOOL={FULL_PATH_TO_DLLTOOL}
	
`INSTALL_FOLDER` should probably be your MinGW prefix (where lib/include folders are)
