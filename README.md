# tictactoe-solver

I solve TicTacToe using the minimax algorithm. 

It looks through every game state and finds the best (or worst!) moves.

Play the AI in the terminal <br> (By default you play as Naughts against the best AI).

## Optimally Bad TicTacToe

Do you like winning? Then play against `optimallybad`! The TicTacToe bot that has searched through every possibility to make you win as often as possible :)

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
