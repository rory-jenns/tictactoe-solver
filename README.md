# tictactoe-solver

I solve TicTacToe using the minimax algorithm. 

It looks through every game state and finds the best (or worst!) moves.

Play the AI in the terminal. Choose different AIs via the flags at the bottom.

## AI

## Random 

It looks through the valid moves and picks one with a uniform random distribution.

### Minimax

Searches through all possible states in the game tree (numbers below). It finds the best move at each state by analysing the moves available and seeing if any are forcing a win/draw on the AI's turn and taking those, or forcing a draw/loss on its opponents turn and avoiding those.

### MENACE

The Matchbox Educable Noughts and Crosses Engine (MENACE) was originally a set of 287 matchboxes representing 'essentially distinct' game states and a lot of beads inside them representing moves that can me made in Naughts and Crosses (TicTacToe). Through playing, beads are added and removed from the matchboxes and the result is the overall system 'learning' to play better.

I aimed to make an AI based off the original source. I based my design off the information in Donald Michie's 1963 paper (below) and a StandUpMaths video I saw many years ago that I felt like linking. However, I could not find the original 1961 paper which he references.

Donald Michie 1963 simulating MENACE - https://gwern.net/doc/reinforcement-learning/model-free/1963-michie.pdf
StandUpMaths MENACE Video - https://youtu.be/R9c-_neaxeU?si=XyUH6qdTKL-jTf3y


### Optimally Bad TicTacToe

Do you like winning? Then play against `optimallybad`! The TicTacToe bot that has searched through every possibility to make you win as often as possible :)

This works through Minimax. It searches through the game tree to find losing moves instead of winning moves.

## Numbers

### Game States
There are 5478 unique game states in tictactoe (which comes from 3^9). 

If you care about symmetry then the number is even fewer in both cases.

### Encoding
I index each game state by encoding the board as a number. For a turn (`t`), a blank is valued at 0, a Naught `O` valued at 1 and a Cross `X` valued at 2 and the positions (`p`) on the board are valued as below.  

0 | 1 | 2  
3 | 4 | 5  
6 | 7 | 8  

The value of a square is calculated as `t * (3 ^ p)`, and the sum of all the squares becomes the unique index.


## Options

If you pick multiple opponents then one will be chosen for you.

--buildgraph   
- this is used to build 'graph.txt' which is a DAG (graph) of all game states.
- You can use this to verify the code is correct, or take the graph for your own uses.
- the states are stored as an index. The states are encoded in base 3 (blank, naught, cross).      

--playcross   
- by Default the human player is playing Naughts (O). Use this flag to play Crosses.   

--twoplayer
-  If you want two human players, use this flag.   

--boteasy
-  This bot will play random moves.   

--bothard
-  This bot uses minimax to play the best moves it can.    

--optimallybad
-  This bot uses minimax to play the worst moves possible. It will try its hardest to lose.    

--menace
-   Play as Crosses against a simulation of the Matchbox Educable Naughts And Crosses Engine (MENACE)