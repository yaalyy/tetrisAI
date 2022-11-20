# tetris
This project produced an AI to play Tetris.

## Rules
- You only have 400 tetronimos to land. This changes the gameplay significantly. Just staying alive to the end is not going to result in a really high score.
- The scoring is weighted heavily in favour of eliminating more rows at a time. The scores for eliminating 1-4 rows are 25, 100, 400, 1600, so there’s a big benefit from not eliminating one row at a time.
-  You can discard a tetronimo you don’t like. You only get to do this 10 times though. This makes play easier for a human, but it’s not necessarily easy for an AI to decide to do this.
-  You can substitute a bomb in place of the next tetronimo! When a bomb lands it destroys all the immediately surrounding blocks, and all the blocks above it or the neighbouring squares will fall to the ground. Blocks destroyed by bombs don’t score anything. You only get five bombs, so use them wisely. Bombs also make play easier for a human, but add a new element for an AI.

In manual play, the key bindings are:   
↑ - rotate clockwise  
→ - move right  
← - move left  
↓ - move down  
Space - drop the block  
z - rotate anticlockwise  
x - rotate clockwise  
b - switch next piece for bomb d - discard   current piece  
Esc - exit game  
If you don’t like the key bindings, feel free to change them. They’re in key to move in [visual-pygame.py](./visual-pygame.py "visual-pygame.py"), UserPlayer.key() in [visual.py](./visual.py "visual.py"), or UserPlayer.choose action() in [cmdline.py](./cmdline.py "cmdline.py").
## Requirement
Python3
## Usage
To **run** the program:   
please run following commands below in the terminal.
`python visual.py`  
To get a feeling for the game, you can also run any of the interfaces in manual mode by adding the flag -m:
`python visual.py -m`  

If that interface does not work, there are two alternative interfaces available:  
• A command-line interface; run `python cmdline.py` to use it. If you are using Windows, you may need to install the windows-curses package first; try running `pip --user install windows-curses`.  
• A Pygame-based interface; run `python visual-pygame.py` to use it. For this, you need to have a working copy of Pygame; run `pip --user install pygame` to install it.  
The pygame version is recommended as it works fastest when autoplaying.
## Reference
1. Islam El-Ashi (2016) El-Tetris – an improvement on Pierre Dellacherie's algorithm, imake. Available at: https://imake.ninja/el-tetris-an-improvement-on-pierre-dellacheries-algorithm/ (Accessed: November 13, 2022). 
2. Lee, Y. (2013) Tetris AI – the (near) perfect bot, Code My Road. Available at: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/ (Accessed: November 20, 2022). 
‌