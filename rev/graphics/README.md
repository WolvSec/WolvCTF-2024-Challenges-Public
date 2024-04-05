# Game Graphics Debugging
## Value: 428
## Solve Count: 33
## Description:
I put a flag in this game, but I can't see it! Can you find it for me?

## Info
The player is given a small "game" which when opened, displays a window containing some basic artwork and a colored box in the UI layer. 
Underneath that box is the flag, however, the flag cannot be viewed because it's being covered. 

# For CTF event runners


## Distribution
Upload all of the zip files inside [`distrib`](distrib). The flag is in `flag.txt`. The different platform versions are suffixed in the file names. 

### Building (only required if changing the flag is desired)
1. You must have the following
	- Microsoft Visual Studio with the Desktop Development in C++ module
2. Clone this repository _recursive_ (`--recurse-submodules` and `--depth=1`). This is because the game engine that this challenge uses is quite large so I didn't want to copy all 300MB of its source code into this repo.
3. To change the flag, paste the string into `flag.h`. It will be obfuscated during compilation via a library that I found, see `obfuscate.h` for details. To keep the current flag, skip this step. 
4. Open a Developer Powershell and `cd` to the `challenge` directory. (It must be a Developer Powershell)
4. Run `config.bat` 
5. Run `build.bat`
6. Go to `build/release/` and put `CTFGame.exe` and `CTFGame.rvedata` in a zip file
	- Both of these files are required for it to work. `CTFGame.rvedata` contains all of the game's assets (shaders, textures, models, etc). 
7. Upload that zip file to the server for players to download

