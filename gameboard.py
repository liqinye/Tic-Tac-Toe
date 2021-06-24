'''
Name:Liqin Ye
Student ID:82829031
'''
import tkinter as tk
import tkinter.messagebox
from functools import partial
import threading

#Ceeate a gameboard class
class BoardClass:
    #Define the instance variables
    _playerUserName = ''
    _lastTurnUserName = ''
    _gameNumber = 0
    _winNumber = 0
    _tiesNumber = 0
    _loseNumber = 0
    #Draw the empty chest board
    _board1 = [' ',' ',' ']
    _board2 = [' ',' ',' ']
    _board3 = [' ',' ',' ']
    _moves = []
    _master = 0

    #Define the BoardClass constructor
    def __init__(self,playerUserName = '',lastTurnUserName = '',gameNumber = 0,\
                 winNumber = 0,tiesNumber = 0,loseNumber = 0,moves = _moves,\
                 board1 = _board1,board2 = _board2,board3 = _board3):
        self.playerUserName = playerUserName
        self.opponent = ''
        self.lastTurnUserName = lastTurnUserName
        self.gameNumber = gameNumber
        self.winNumber = winNumber
        self.tiesNumber = tiesNumber
        self.loseNumber = loseNumber
        self.board1 = board1
        self.board2 = board2
        self.board3 = board3
        self.moves = moves
        self.turn = 0
        self.buttons = []

        
    #Initalizes my tk variables
    def initTKVariables(self):
        self.mySyb = tk.StringVar()

    #Set up canvas
    def canvasSetup(self,mySyb,opSyb,conn):
        #initialize my tkinter canvas
        self.master = tk.Tk()
        if mySyb == 'X':
            self.master.title('Tic Tac Toe Game Board-Player 1')
        elif mySyb == 'O':
            self.master.title('Tic Tac Toe Game Board-Player 2')
        self.master.geometry('600x660')
        self.master.configure(bg='light blue')
        self.master.resizable(1,1)
        self.initTKVariables()
        self.boardSetup(mySyb,opSyb,conn)

    #Setup my game board
    def boardSetup(self,mySyb,opSyb,conn):
        #Update the game played time
        self.updateGamesPlayed()
        #Main chest board
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                self.chestButton = tk.Button(self.master,bg='light blue',text='   ')
                self.chestButton.grid(row=i,column=j,ipadx=90,ipady=60)
                self.chestButton.configure(command = partial(self.clickChestBoard,i,j,mySyb,opSyb,conn))
                self.buttons[-1].append(self.chestButton)

            
        #Game Statistic
        self.title = tk.Label(self.master,bg='light blue',text='Game Statistic').grid(row=4,column=1)
        self.nameT = tk.Label(self.master,bg='light blue',text='Player user name:').grid(row=5,column=0)
        self.lastTurnT = tk.Label(self.master,bg='light blue',text='Last turn player:').grid(row=6,column=0)
        self.gameT = tk.Label(self.master,bg='light blue',text='The number of games:').grid(row=7,column=0)
        self.winT = tk.Label(self.master,bg='light blue',text='The number of wins:').grid(row=8,column=0)
        self.loseT = tk.Label(self.master,bg='light blue',text='The number of losses:').grid(row=9,column=0)
        self.tieT = tk.Label(self.master,bg='light blue',text='The number of ties:').grid(row=10,column=0)

        #Game Status
        self.statusTitle = tk.Label(self.master,bg='light blue',text='Game Dialog').grid(row=4,column=2)

        #Quit button
        self.quitButton = tk.Button(self.master,bg='red',text='Quit',command = self.master.destroy).grid(row=12,column=1)

        if mySyb == 'X':
            self.turnLabel = tk.Label(self.master,bg='light blue',text=self.playerUserName+"'s turn")
            self.turnLabel.grid(row=5,column=2)

        if mySyb == 'O':
            turnText = self.opponent + "'s turn"
            self.turnLabel = tk.Label(self.master,bg='light blue',text=turnText)
            self.turnLabel.grid(row=5,column=2)
            self.master.after(1000,self.delayRecvMove,mySyb,opSyb,conn)
    
    #Click the chest board
    def clickChestBoard(self,i,j,mySyb,opSyb,conn):
        #When it is other's turn, do nothing
        if self.turn % 2 == 1 and mySyb == 'X':
            return
        if self.turn % 2 == 0 and mySyb == 'O':
            return

        MyThread(self.sendMove,i,j,mySyb,opSyb,conn)
        MyThread(self.recvMove,mySyb,opSyb,conn)
        
    #Get players move
    def recvInfo(self,conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    continue
                playerMove = data.decode('ascii')
                if playerMove == 'Play Again' or playerMove == 'Fun Times':
                    return playerMove
                    break
                playerMoveT = tuple(map(int,playerMove))
                return playerMoveT
            except ValueError:
                return playerMove
            
    #Send player Move when user click the chest board
    def sendMove(self,i,j,mySyb,opSyb,conn):
        self.turn += 1
        self.buttons[i][j].configure(text=mySyb)
        self.updateGameBoard(mySyb,opSyb,conn,(i+1,j+1))
        self.buttons[i][j]['state'] = 'disabled'
        conn.send(str.encode(str(i)+str(j)))
        self.turnLabel.destroy()
        turnText = self.opponent + "'s turn"
        self.turnLabel = tk.Label(self.master,bg='light blue',text=turnText)
        self.turnLabel.grid(row=5,column=2)
        self.endOrAgain(mySyb,opSyb,conn)
        
    #Receive another player's move
    def recvMove(self,mySyb,opSyb,conn):
        playerStep = self.recvInfo(conn)
        if playerStep == 'DONE':
            self.playerUserName = ''
            self.opponent = ''
            self.gameNumber = 0
            self.winNumber = 0
            self.loseNumber = 0
            self.tiesNumber = 0
            self.resetUI(mySyb,opSyb,conn)
            
        if playerStep == 'Fun Times':
            self.lastTurnUserName = self.playerUserName
            textSend1 = self.opponent + ':Fun Times'
            self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend1)
            self.statusLabel.grid(row=6,column=2)
            self.printStats()
            return
        elif playerStep == 'Play Again':
            textSend2 = self.opponent + ':Play Again'
            self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend2)
            self.statusLabel.grid(row=6,column=2)
            self.resetUI(mySyb,opSyb,conn)
            return
        else:
            row,col = playerStep
            self.turn += 1
            self.buttons[row][col].configure(text=opSyb)
            self.updateGameBoard(opSyb,mySyb,conn,(row+1,col+1))
            self.buttons[row][col]['state'] = 'disabled'
            self.turnLabel.destroy()
            self.turnLabel = tk.Label(self.master,bg='light blue',text=self.playerUserName+"'s turn")
            self.turnLabel.grid(row=5,column=2)
            self.endOrAgain(mySyb,opSyb,conn)

    #Delay receiving the move from opponent
    def delayRecvMove(self,mySyb,opSyb,conn):
        row,col = self.recvInfo(conn)
        self.turn += 1
        self.buttons[row][col].configure(text=opSyb)
        self.updateGameBoard(opSyb,mySyb,conn,(row+1,col+1))
        self.buttons[row][col]['state'] = 'disabled'
        self.turnLabel.destroy()
        self.turnLabel = tk.Label(self.master,bg='light blue',text=self.playerUserName+"'s turn")
        self.turnLabel.grid(row=5,column=2)
        if self.gameNumber > 1:
            self.statusLabel.destroy()

    #Decide End or restart
    def endOrAgain(self,mySyb,opSyb,conn):
        #Get the win or lose result
        winOrLose = self.isWinner(mySyb,opSyb)

        if winOrLose == 'True':
            #Disabled the button on the chest board
            for row in self.buttons:
                for eachButton in row:
                    if eachButton['state'] != 'disabled':
                        eachButton['state'] = 'disabled'
            self.turnLabel.destroy()
            #Inform user game over
            self.statusLabel1 = tk.Label(self.master,bg='light blue',text='Game over')
            self.statusLabel1.grid(row=5,column=2)
            if mySyb == 'X':
                self.informWin = tk.Label(self.master,bg='light blue',text='You win!') #Create the label to inform player win
                self.informWin.grid(row=6,column=2)
                self.lastTurnUserName = self.playerUserName #Update the last turn player
                self.statusLabel2 = tk.Label(self.master,bg='light blue',text='Do you want to play again?') #Ask if player want to play again
                self.statusLabel2.grid(row=7,column=2)
                #Create the yes or no button to answer play again question
                self.statusButton1 = tk.Button(self.master,bg='red',text='Yes',command=partial(self.resetUI,mySyb,opSyb,conn))
                self.statusButton1.grid(row=8,column=2)
                self.statusButton2 = tk.Button(self.master,bg='red',text='No',command=partial(self.endGame,conn))
                self.statusButton2.grid(row=9,column=2)
            if mySyb == 'O':
                self.informWin = tk.Label(self.master,bg='light blue',text='You win!')
                self.informWin.grid(row=6,column=2)

        elif winOrLose == 'False':
            #Disabled the button on the chest board
            for row in self.buttons:
                for eachButton in row:
                    if eachButton['state'] != 'disabled':
                        eachButton['state'] = 'disabled'
            #Destroy the turn label
            self.turnLabel.destroy()
            self.statusLabel1 = tk.Label(self.master,bg='light blue',text='Game over') #Inform game over
            self.statusLabel1.grid(row=5,column=2)
            if mySyb == 'X':
                self.informWin = tk.Label(self.master,bg='light blue',text='You lose.') #Inform lose
                self.informWin.grid(row=6,column=2)
                self.lastTurnUserName = self.opponent
                self.statusLabel2 = tk.Label(self.master,bg='light blue',text='Do you want to play again?') #Ask if player want to play again
                self.statusLabel2.grid(row=7,column=2)
                #Create the yes or no button to answer play again question
                self.statusButton1 = tk.Button(self.master,bg='red',text='Yes',command=partial(self.resetUI,mySyb,opSyb,conn))
                self.statusButton1.grid(row=8,column=2)
                self.statusButton2 = tk.Button(self.master,bg='red',text='No',command=partial(self.endGame,conn))
                self.statusButton2.grid(row=9,column=2)
            if mySyb == 'O':
                self.informWin = tk.Label(self.master,bg='light blue',text='You lose.') #Inform lose
                self.informWin.grid(row=6,column=2)
                #Receive player1 choice
                dataRecv = self.recvInfo(conn)
                if dataRecv == 'Fun Times':
                    self.lastTurnUserName = self.opponent #Update the last turn player name
                    textSend1 = self.opponent + ':Fun Times'
                    self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend1)
                    self.statusLabel.grid(row=6,column=2)
                    self.printStats() #Print the game statistic
                elif dataRecv == 'Play Again':
                    textSend2 = self.opponent + ':Play Again'
                    self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend2)
                    self.statusLabel.grid(row=6,column=2)
                    self.resetUI(mySyb,opSyb,conn) #Restart the game
                    
        elif self.boardIsFull() == 'True':
            self.turnLabel.destroy()
            #Inform user game over
            self.statusLabel1 = tk.Label(self.master,bg='light blue',text='Game over')
            self.statusLabel1.grid(row=5,column=2)
            
            if mySyb == 'X':
                self.informWin = tk.Label(self.master,bg='light blue',text='Ties.') #Inform ties
                self.informWin.grid(row=6,column=2)
                self.lastTurnUserName = self.playerUserName #Update the last turn player name
                self.statusLabel2 = tk.Label(self.master,bg='light blue',text='Do you want to play again?') #Ask if player want to play again
                self.statusLabel2.grid(row=7,column=2)
                #Create the yes or no button to answer play again question
                self.statusButton1 = tk.Button(self.master,bg='red',text='Yes',command=partial(self.resetUI,mySyb,opSyb,conn))
                self.statusButton1.grid(row=8,column=2)
                self.statusButton2 = tk.Button(self.master,bg='red',text='No',command=partial(self.endGame,conn))
                self.statusButton2.grid(row=9,column=2)
            if mySyb == 'O':
                self.informWin = tk.Label(self.master,bg='light blue',text='Ties.') #Inform ties
                self.informWin.grid(row=6,column=2)
                #Receive player1 choice
                dataRecv = self.recvInfo(conn)
                if dataRecv == 'Fun Times':
                    self.informWin.destroy()
                    self.lastTurnUserName = self.opponent #Update the last turn user name
                    textSend1 = self.opponent + ':Fun Times'
                    self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend1)
                    self.statusLabel.grid(row=6,column=2)
                    self.printStats()
                elif dataRecv == 'Play Again':
                    textSend2 = self.opponent + ':Play Again'
                    self.statusLabel = tk.Label(self.master,bg='light blue',text=textSend2)
                    self.statusLabel.grid(row=6,column=2)
                    self.resetUI(mySyb,opSyb,conn)
        
            
    #Reset the game board
    def resetUI(self,mySyb,opSyb,conn):
        #Destroy the dialog label
        self.statusLabel1.destroy()
        self.informWin.destroy()
        if mySyb == 'X':
            conn.sendall(str.encode('Play Again'))
            #Destroy the choice button
            self.statusLabel2.destroy()
            self.statusButton1.destroy()
            self.statusButton2.destroy()
            self.turnLabel = tk.Label(self.master,bg='light blue',text=self.playerUserName+"'s turn")
            self.turnLabel.grid(row=5,column=2)
        self.resetGameBoard() #Reset the game board
        self.updateGamesPlayed() #Update the game played time
        #Enabled the buttons
        for row in self.buttons:
            for eachButton in row:
                eachButton.configure(text='   ')
                eachButton['state'] = 'normal'
        if mySyb == 'O':
            turnText = self.opponent + "'s turn"
            self.turnLabel = tk.Label(self.master,bg='light blue',text=turnText)
            self.turnLabel.grid(row=5,column=2)
            self.master.after(1000,self.delayRecvMove,mySyb,opSyb,conn)
        
    #End the game
    def endGame(self,conn):
        #Destroy any other things
        self.informWin.destroy()
        self.statusLabel2.destroy()
        self.statusButton1.destroy()
        self.statusButton2.destroy()
        conn.sendall(str.encode('Fun Times'))
        #Print the game statistics
        self.printStats()
    
    #Update the change to UI
    def runUI(self):
        #Starts my UI - event handler
        self.master.mainloop()
            
    #Update the game played times
    def updateGamesPlayed(self):
        self.gameNumber += 1

    #Reset the game board
    def resetGameBoard(self):
        self.board1 = [' ',' ',' ']
        self.board2 = [' ',' ',' ']
        self.board3 = [' ',' ',' ']
        self.moves = []
        self.turn = 0
        
    #Check if there is a winner
    def isWinner(self,urSyb = '',opSyb = ''):
        allBoard = []
        allBoard.append(self.board1)
        allBoard.append(self.board2)
        allBoard.append(self.board3)
        urSybList = [urSyb,urSyb,urSyb]
        opSybList = [opSyb,opSyb,opSyb]
        #Check if the row is all the same symbol
        for eachBoard in allBoard:
            if eachBoard == urSybList:
                self.winNumber += 1
                return 'True'
            elif eachBoard == opSybList:
                self.loseNumber += 1
                return 'False'
        #Check if the column is all the same symbol 
        for i in range(3):
            if self.board1[i] == urSyb:
                if self.board1[i] == self.board2[i] == self.board3[i]:
                    self.winNumber += 1
                    return 'True'
            elif self.board1[i] == opSyb:
                if self.board1[i] == self.board2[i] == self.board3[i]:
                    self.loseNumber += 1
                    return 'False'
        #Check if the diagonal is all the same symbol
        if self.board1[0] == urSyb:
            if self.board1[0] == self.board2[1] == self.board3[2]:
                self.winNumber += 1
                return 'True'
        elif self.board1[0] == opSyb:
            if self.board1[0] == self.board2[1] == self.board3[2]:
                self.loseNumber += 1
                return 'False'
        if self.board1[2] == urSyb:
            if self.board1[2] == self.board2[1] == self.board3[0]:
                self.winNumber += 1
                return 'True'
        elif self.board1[2] == opSyb:
            if self.board1[2] == self.board2[1] == self.board3[0]:
                self.loseNumber += 1
                return 'False'

    #Check whether the board is full
    def boardIsFull(self):
        self.moves.sort()
        allPos = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
        if self.moves == allPos:
            self.tiesNumber += 1
            return 'True'
        
    #Update the move to the game board
    def updateGameBoard(self,urSyb,opSyb,conn,pos = (0,0)):
        #Record each move
        self.moves.append(pos)
        if pos[0] == 1:
            self.board1[(pos[1]-1)] = urSyb
        if pos[0] == 2:
            self.board2[(pos[1]-1)] = urSyb
        if pos[0] == 3:
            self.board3[(pos[1]-1)] = urSyb

    #Print Statistics to the game board        
    def printStats(self):
        self.nameStats = tk.Label(self.master,bg='light blue',text=self.playerUserName)
        self.nameStats.grid(row=5,column=1)
        self.lastTurnStats = tk.Label(self.master,bg='light blue',text=self.lastTurnUserName)
        self.lastTurnStats.grid(row=6,column=1)
        self.gameNum = tk.Label(self.master,bg='light blue',text=self.gameNumber)
        self.gameNum.grid(row=7,column=1)
        self.winNum = tk.Label(self.master,bg='light blue',text=self.winNumber)
        self.winNum.grid(row=8,column=1)
        self.loseNum = tk.Label(self.master,bg='light blue',text=self.loseNumber)
        self.loseNum.grid(row=9,column=1)
        self.tieNum = tk.Label(self.master,bg='light blue',text=self.tiesNumber)
        self.tieNum.grid(row=10,column=1)
        
#Define my threading class
class MyThread(threading.Thread):
    def __init__(self, function, *args):
        super().__init__()
        self.function = function
        self.args = args
        self.setDaemon(True)
        self.start()
        
    def run(self):
        self.function(*self.args)      


        
    

