# Software_Final_Project_Battleship
# The final project for Software Carpentry class.
This project is a game of battleship played by single player against the computer.  
Player (and computer) are going to set 5 ships in different sizes on a 10*10 grid.  
The size and number of different ships for both players are shown in Figure 1.  
Each player has a chance to choose a block to blast, the first player who blasts all the ships from
the opponent is the winner.  
![Image text](https://github.com/arthurzhang434/Software_Final_Project_Battleship/blob/master/ships.png)   
Figure 1: Each player has 5 ships.  
The Graphical User Interface (GUI) is made through Pygame.
In order to run this code, Pygame 1.9 or later has to be installed.  
The game interface of this battleship game is shown in Figure 2.
Once enter the game, player could place 5 ships one by one on the left grid which represents the player's sea.  
Player should first drag the ship to the desired position then click the mouse button to place down the ship.  
The default direction of ships are set to horizontal, player could change to vertical by clicking any key on the keyboard.  
If a player places the ships out of the player's sea or on the position overlapped with an already exist position. A remind will be shown in the console (or terminal).  
Once player and computer finishing the placement of the ships, the player could choose a block in computer's sea to blast by clicking that block. Then computer will response to player's sea after that.  
![Image text](https://github.com/arthurzhang434/Software_Final_Project_Battleship/blob/master/gamescreen.png)  
Figure 2: The example of the game interface. Grey blocks represent player's ships. Red blocks represent hitted ships. Green blocks represent missed shots.


