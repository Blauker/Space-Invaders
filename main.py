# CREATED BY:
# ▀█████████▄   ▄█          ▄████████ ███    █▄     ▄█   ▄█▄    ▄████████    ▄████████ 
#   ███    ███ ███         ███    ███ ███    ███   ███ ▄███▀   ███    ███   ███    ███ 
#   ███    ███ ███         ███    ███ ███    ███   ███▐██▀     ███    █▀    ███    ███ 
#  ▄███▄▄▄██▀  ███         ███    ███ ███    ███  ▄█████▀     ▄███▄▄▄      ▄███▄▄▄▄██▀ 
# ▀▀███▀▀▀██▄  ███       ▀███████████ ███    ███ ▀▀█████▄    ▀▀███▀▀▀     ▀▀█████▀▀▀   
#   ███    ██▄ ███         ███    ███ ███    ███   ███▐██▄     ███    █▄  ▀█████████▄ 
#   ███    ███ ███▌    ▄   ███    ███ ███    ███   ███ ▀███▄   ███    ███   ███    ███ 
# ▄█████████▀  █████▄▄██   ███    █▀  ████████▀    ███   ▀█▀   ██████████   ███    ███ 
#              ▀                                   ▀                        ███    ███ 2024

import os, random, time
import SmoothPrint as SP
from pynput import keyboard
from enum import Enum

ALIEN = "👾"
PLAYER = "🚀"
SPACE = "  "
BULLET = "||"
EXPLOSION = "💥"
BOARD = [19, 12]
BOARD_COLOR = "⬜"
ENEMYROWS = 4

class Movement(Enum):
    RIGHT = 1
    LEFT = 2

class Game:
    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.data =  [[0] * size_x for _ in range(size_y)]
        self.board = [[0] * size_x for _ in range(size_y)]
        self.score = 0
        self.numOfEnemies = self.InitEnemies()
        self.player_pos = [self.size_y - 2, (int)(self.size_x / 2)]

    def InitGame(self):
        self.data[self.player_pos[0]][self.player_pos[1]] = 2

        while True:
            self.Print()
            win = False
            mov = input("Move (A - D) or Shoot (W): ")
            if mov.lower() == "a":
                self.MovePlayer(Movement.LEFT)
            elif mov.lower() == "d":
                self.MovePlayer(Movement.RIGHT)
            elif mov.lower() == "w":
                win = self.Shoot()
            elif mov.lower() == "q":
                exit()
            
            if win:
                break
        
        os.system("clear")
        self.WinPannel()

    def CheckIfWin(self) -> bool:
        if self.numOfEnemies <= 0:
            return True
        return False

    def WinPannel(self):
        SP.slowPrint("Congratulations! You win!")
        SP.slowPrint(f"Your score: {self.score}", 0.1)

    def Shoot(self) -> bool:
        lastAlien = []
        for i in range(self.size_y - 2):
            if self.data[i][self.player_pos[1]] != 1:
                self.board[i][self.player_pos[1]] = 1
            else:
                lastAlien = [i, self.player_pos[1]]
        
        if lastAlien != []:
            self.data[lastAlien[0]][lastAlien[1]] = 0
            self.board[lastAlien[0]][lastAlien[1]] = 2
            self.score += 10
            self.numOfEnemies -= 1
        
        return self.CheckIfWin()

    def MovePlayer(self, movement: Movement):
        self.ClearBoard()
        for i in range(self.size_x):
            self.data[self.player_pos[0]][i] = 0
        match movement:
            case Movement.RIGHT:
                if self.player_pos[1] < self.size_x - 1:
                    self.player_pos[1] += 1
            case Movement.LEFT:
                if self.player_pos[1] > 0:
                    self.player_pos[1] -= 1
        self.data[self.player_pos[0]][self.player_pos[1]] = 2
    
    def ClearBoard(self):
        self.board = [[0] * self.size_x for _ in range(self.size_y)]

    def InitEnemies(self) -> int:
        numOfEnemies = 0
        if ENEMYROWS > self.size_y / 2:
            print("ERROR")
            exit()
        for i in range(ENEMYROWS):
            for j in range(self.size_x):
                if j <= 1 or j >= self.size_x - 2: continue
                if j % 2 == 0:
                    self.data[i][j] = 1
                    numOfEnemies += 1
        return numOfEnemies
    
    def Print(self):
        os.system("clear")
        print("╔═", end=""); print("══" * self.size_x, end=""); print("═╗")
        for i in range(self.size_y):
            print("║ ", end="")
            for j in range(self.size_x):
                if self.board[i][j] == 1:
                    print(BULLET, end="")
                elif self.board[i][j] == 2:
                    print(EXPLOSION, end="")

                elif self.data[i][j] == 0:
                    print(SPACE, end="")
                elif self.data[i][j] == 1:
                    print(ALIEN, end="")
                elif self.data[i][j] == 2:
                    print(PLAYER, end="")
            print(" ║", end="")
            
            # Printing SCORE
            if (i == self.size_y/2 - 1):
                print("   SCORE:", end="")
            if (i == self.size_y/2):
                print(f"   {self.score}, {self.numOfEnemies}", end="")
            print("\n", end="")
        print("╚═", end=""); print("══" * self.size_x, end=""); print("═╝")


# ----- START OF THE GAME ----- #
game = Game(BOARD[0], BOARD[1])

# INFINITE GAME LOOP generating pieces
game.InitGame()
