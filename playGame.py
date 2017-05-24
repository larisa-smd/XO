import random as r
import Tkinter
from Tkinter  import *
from Tkconstants import *
from Tkinter import Message


class Game(Frame):
    # set all the variables, prepare the board
    def __init__(self, master):
        self.root = Tkinter.Frame(master, borderwidth=5, bd=3)

        self.player = {'wins': 0, 'ties': 0, 'loses': 0}
        self.statusFrame = Frame(master, borderwidth=5, bd=3)
        self.status = Label(self.statusFrame, text=">>>Welcome player, you are 'X'", bg="light green", bd=1, font=15, \
                            anchor=SW)
        self.board = []
        self.boardPaper = []
        self.availableSpaces = []
        self.photoPlayer = PhotoImage(file='x.png')
        self.photoComputer = PhotoImage(file='o.png')
        self.photoEmpty = PhotoImage(file='empty.png')
        self.hard = False
        for i in range(0, 3):
            for j in range(0, 3):
                t = tuple((i, j))
                self.availableSpaces.append(t)

        self.startGame()

        self.root.pack()
        self.statusFrame.pack(side=BOTTOM)
        self.status.pack()

    # returns the number of empty spaces left on the board
    def noSpacesLeft(self):
        return len(self.availableSpaces)

    def refreshBoard(self):
        self.resetBoard()
        self.showScore()

    def checkSpace(self, c, s):
        winnerSpace = False
        x, y = s
        self.boardPaper[x][y] = c
        if self.playerWin(c):
            winnerSpace = True
        self.boardPaper[x][y] = ''
        return winnerSpace

    def computerClick(self, s):
        x, y = s
        self.board[x][y].config(text='O', state='disabled', image=self.photoComputer)
        self.boardPaper[x][y] = 'O'
        self.availableSpaces.remove(s)
        if self.playerWin('O'):
            self.status.config(text="Sorry!! You lost!!!")
            messagebox.showinfo("LOST", " Sorry!! You lost!!")
            self.player['loses'] += 1
            self.refreshBoard()

    def itIsaTie(self):
        self.resetBoard()
        self.player['ties'] += 1
        messagebox.showinfo("TIE", " It's a tie. No one wins this game!!!")
        self.showScore()

    def playerClicked(self, i, j):
        # the player clicked so the space is filled with 'X'
        self.board[i][j].config(text='X', state='disabled', image=self.photoPlayer)
        self.boardPaper[i][j] = 'X'
        t = tuple((i, j))
        self.availableSpaces.remove(t)
        # check to see if the player is a winner
        if self.playerWin('X'):
            self.status.config(text="Congratulation!!   YOU WIN  THE GAME!!")
            messagebox.showinfo("WIN", " Congratulation!!!   You won!!")
            self.player['wins'] += 1
            self.refreshBoard()
        # the player is not a winner, so we check for empty spaces on the board
        elif self.noSpacesLeft() > 0:
            if self.hard:
                ComputerClicked = False

                for space in self.availableSpaces:
                    if self.checkSpace('O', space):
                        self.computerClick(space)
                        ComputerClicked = True
                        break

                if not ComputerClicked:
                    for space in self.availableSpaces:
                        if self.checkSpace('X', space):
                            self.computerClick(space)
                            ComputerClicked = True
                            break

                if not ComputerClicked:
                    computerChoice = r.randint(0, self.noSpacesLeft() - 1)
                    computer = self.availableSpaces[computerChoice]
                    self.computerClick(computer)

            else:
                computerChoice = r.randint(0, self.noSpacesLeft() - 1)
                computer = self.availableSpaces[computerChoice]
                self.computerClick(computer)

        else:
            self.itIsaTie()

    def showScore(self):
        score = " The score is: \nYou win %d games, \nYou lost %d games and \n tied %d games." \
                % (self.player['wins'], self.player['loses'], self.player['ties'])
        self.status.config(text=score)

    def playerWin(self, c):

        win = False
        #  ----  check the lines for winner
        for i in range(0, 3):
            if self.boardPaper[i][0] == self.boardPaper[i][1] and self.boardPaper[i][1] == self.boardPaper[i][2] and \
                            self.boardPaper[i][0] == c:
                win = True

        # ------ check  the columns for winner
        for j in range(0, 3):
            if self.boardPaper[0][j] == self.boardPaper[1][j] and self.boardPaper[1][j] == self.boardPaper[2][j] and \
                            self.boardPaper[0][j] == c:
                win = True

        # ------  check diagonally for the winner  -------
        if self.boardPaper[0][0] == self.boardPaper[1][1] and self.boardPaper[1][1] == self.boardPaper[2][2] and \
                        self.boardPaper[0][0] == c:
            win = True

        if self.boardPaper[2][0] == self.boardPaper[1][1] and self.boardPaper[1][1] == self.boardPaper[0][2] and \
                        self.boardPaper[2][0] == c:
            win = True

        return win

    def createButton(self, i, j):
        b = Button(self.root, padx=2, pady=2, text="", font=60, bd=5, \
                   command=lambda a=i, b=j: self.playerClicked(a, b), image=self.photoEmpty)
        b.grid(row=i, column=j)
        return b

    def resetBoard(self):
        self.availableSpaces = []
        for i in range(0, 3):
            for j in range(0, 3):
                self.boardPaper[i][j] = " "
                self.board[i][j] = self.createButton(i, j)
                t = tuple((i, j))
                self.availableSpaces.append(t)
        self.status.config(text="A new game has started. Have fun !!!")

    def startGame(self):
        for i in range(0, 3):
            line = []
            linePaper = []
            for j in range(0, 3):
                cell = self.createButton(i, j)
                line.append(cell)
                linePaper.append(' ')
            self.board.append(line)
            self.boardPaper.append(linePaper)

    def clickNewGame(self):
        self.player = {'wins': 0, 'ties': 0, 'loses': 0}
        self.resetBoard()

    def stopGame(self):
        messagebox.showwarning("Lost", "You lose!!   You can try again...")
        self.status.config(text=" You lost!!  Maybe play again...")
        self.player['loses'] += 1
        self.resetBoard()

    def quitGame(self):
        self.root.quit()

    def selectDifficulty(self):
        self.hard = not self.hard
        messagebox.showinfo('HARD', 'You selected to play for "real" versus the computer! ')

    def helpAbout(self):
        mess = "A game that the player plays against \nthe computer on which the \ngame is running!!"
        mess += "\nMy name is Larisa,  good luck!!!"
        self.status.config(text=mess)

    def showRules(self):
        message = '''The rules are simple:
   *  you have to chose a rectangle and
        click it
   *  you click in turns, you and your
        opponent
   *  the one that can put his symbol
        in a row, column or diagonal wins
   *  if the rectangles are all clicked,
        and there is not 3 symbols in a
        row, column or diagonal, the same
        symbol, than it's a tie'''

        self.status.config(text=message)


window = Tk()
window.title(" X & O")
window.config(bg="light green")
window.resizable(width=False, height=False)
window.iconbitmap("resources/game.ico")


game = Game(window)



# ***********    MENU   **************

#  ------>  Menu
player_x = BooleanVar()
player_o = BooleanVar()

menu = Menu()

v=BooleanVar()
v.set(False)
menuGame = Menu(menu, tearoff=0)
menuGame.add_command(label="New game", command=game.clickNewGame)
menuGame.add_command(label="Stop game", command=game.stopGame)
menuGame.add_separator()
menuGame.add_command(label="Exit", command=game.quitGame)
menu.add_cascade(label="Game", menu=menuGame)

menuDifficulty = Menu(menu, tearoff=0)
menuDifficulty.add_radiobutton(label="Easy", font=20, value=False,variable=v,  selectcolor='blue',  command=game.selectDifficulty)
menuDifficulty.add_radiobutton(label="Hard", font=20, value=True, variable=v,  selectcolor='blue', command=game.selectDifficulty)
menu.add_cascade(label="Difficulty", menu=menuDifficulty)

menuHelp = Menu(menu, tearoff=0)
menuHelp.add_command(label="About", command=game.helpAbout)
menuHelp.add_command(label="Rules", command=game.showRules)
menu.add_cascade(label="Help", menu=menuHelp)

window.config(menu=menu)


window.mainloop()