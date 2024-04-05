# Rev: Shredded
## Value: 50
## Solve Count: 66
## Description:
We encoded a flag, and to make sure that pesky interlopers couldn't reverse it, we shredded the encoding code.

**Note:** The encoder was written in C. The code is written with good style, but all indents have been removed.

# Provide
`shredder.py`, `output.txt` and `out.zip`

## Solution
Based on common C coding standards, we can order some of the lines. For example, the "#includes" statements can easily be reconstructed, after which the rest is also pretty easily retrievable.
The actual code is easy to recover. The string is reordered based on index 0:50, which can be reversed by re-reordering the string with the same function. Then, each character must be subtracted by 0x20 and XORed with 0x20. 
Again, there are 2 more rounds of shuffling the flag, which can be reversed in the same manner as above.
At this moment, there should only be a padding left, which can be removed trivially by cutting the string off after the "}".
