# Missing Resources
## Value: 323
## Solve Count: 51
### Description
My flag is somewhere in this game, but I lost the source code and most of the resources! Can you retrieve it for me?

Hint 0: All of the error messages are part of the challenge! Use your internet-searching skills to find out what they mean!

Hint 1: You can find copies of the missing files on the internet. Be careful about where you download things from!

Hint 2: Is it opening and then instantly closing? Try using CMD to run the exe to get its output!
## Info
The player is given `game.exe`, which is missing its resources (two DLLs and a font file).
They must track down these items (which can be easily obtained from the internet)
and place them next to the exe. Once they have done this, the exe will display the flag
on-screen.

## For CTF event runners

### Description
I hid my flag in a game, but the CD got scratched and only the exe remains! Can you put it back together?

Hint 0: All of the error messages are part of the challenge! Use your internet-searching skills to find out what they mean!

Hint 1: You can find copies of the missing files on the internet. Be careful about where you download things from!

Hint 2: Is it opening and then instantly closing? Try using CMD to run the exe to get its output!

### Distribution
Upload [`CD.zip`](distrib/CD.zip) to the server for players to download. The flag is in `flag.txt`.

### Building (only required if changing the flag is desired)
1. You must have the following:
    -  Microsoft Visual Studio 2022 with the Desktop Development in C++ module
	-  NuGet for Visual Studio 
3. To change the flag, open `flag.h` and set the `FLAG` define to the flag string. The string will be obfuscated during compile time. See `obfuscate.h` for details. To keep the default flag, skip this step. 
4. Open `game.sln` and create a Release x64 build. When running it from Visual Studio, you should see a window with the flag displayed inside it.
5. Upload `x64/Release/game.exe` to the server for players to download. Don't upload the font or any of the DLLs.

