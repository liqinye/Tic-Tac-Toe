'''
Name:Liqin Ye
Student ID:82829031
'''
import socket
from gameboard import *

player2Address = '127.0.0.1'
player2Port = 8000

#Make connection with player1
def makeConnection():
    #Start bind the fixed IP
    player2Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    player2Socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1024)
    player2Socket.bind((player2Address,player2Port))
    player2Socket.listen()
    connection,address = player2Socket.accept()
    #Constructor the board class
    gameBoard = BoardClass()
    #Receive player1 name and send player2 name to player1
    data = connection.recv(1024)
    dataRecv = data.decode('ascii')
    gameBoard.opponent = dataRecv
    connection.sendall(str.encode('player2'))
    gameBoard.playerUserName = 'player2'
    #If receive the name,start playing game
    if data:
        playGame(gameBoard,connection)
            
def playGame(board,serverInfo):
    board.canvasSetup('O','X',serverInfo)
    board.runUI()
    
if __name__ == '__main__':
    makeConnection()

    
        
    
    
