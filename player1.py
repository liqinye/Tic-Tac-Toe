'''
Name:Liqin Ye
Student ID:82829031
'''
import socket
import tkinter as tk
from tkinter import messagebox
from gameboard import *
from functools import partial

#Make GUI to ask player1 to input IP/Port
def makeConnection():
    #initialize the connection board
    global GUI
    GUI = tk.Tk()
    GUI.title('Tic Tac Toe')
    GUI.configure(bg='light blue')
    GUI.geometry('300x170')
    #Create entry for player to input IP
    global IPLabel
    global IPEntry
    IPLabel = tk.Label(GUI,text='IP Address:',bg='light blue').pack()
    IPEntry = tk.Entry(GUI,width=15)
    IPEntry.pack()
    #Create entry for player to input Port
    global portLabel
    global portEntry
    portLabel = tk.Label(GUI,bg='light blue',text='Port:').pack()
    portEntry = tk.Entry(GUI,width=15)
    portEntry.pack()
    #Create connect button
    global connectButton
    connectButton = tk.Button(GUI,bg='red',text='Connect',command=askForAddress)
    connectButton.pack()
    GUI.mainloop()

#Get player input IP/Port and user name to start game
def askForAddress():
    #initialize the port number
    port = 0
    try:
        #Get player1 input IP/Port
        port = int(portEntry.get())
        IP = IPEntry.get()
        #Check if it matches player2
        if (IP,port) == ('127.0.0.1',8000):
            GUI.destroy()
            player1Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            player1Socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1024)
            player1Socket.connect((IP,port))
            gameBoard = BoardClass() #Constructor my board class
            getUserName(gameBoard,player1Socket) #create another gui for user name
        #If it doesn't matches, ask for them if they want to connect again
        elif (IP,port) != ('127.0.0.1',8000):
            global connectAgain
            connectAgain = tk.messagebox.askquestion(title='Ask for Connection',message='Your connectino failed. Do you want to connect again?')
            if connectAgain == 'yes':
                GUI.destroy()
                makeConnection()
            elif connectAgain == 'no':
                GUI.destroy()
    #Except the value error of non-int input
    except ValueError:
        connectAgain = tk.messagebox.askquestion(title='Ask for Connection',message='Your connectino failed. Do you want to connect again?')
        if connectAgain == 'yes':
            GUI.destroy()
            makeConnection() #Loop the IP/Port input
        elif connectAgain == 'no':
            GUI.destroy()

#Ask player for user name
def getUserName(board,conn):
    #initialize the user interface
    global gui
    gui = tk.Tk()
    gui.configure(bg='light blue')
    gui.title('Tic Tac Toe')
    gui.geometry('300x170')
    #Create name label,entry,button
    global nameLabel
    global nameEntry
    global nameButton
    nameLabel = tk.Label(gui,bg='light blue',text='Please Enter Your User Name:').pack()
    nameEntry = tk.Entry(gui,width=14)
    nameEntry.pack()
    nameButton = tk.Button(gui,bg='red',text='Start',command=partial(startGame,board,conn))
    nameButton.pack()
    gui.mainloop()

#Start game
def startGame(board,conn):
    board.playerUserName = nameEntry.get() #Update the player1 user name
    conn.sendall(str.encode(board.playerUserName)) #Send it to player2
    data = conn.recv(1024) #Recv player2 User name
    dataRecv = data.decode('ascii')
    board.opponent = dataRecv #Update the opponent name
    gui.destroy()
    #Start playing game
    playGame(board,conn)
        
#Send the information to player2
def playGame(board,userInfo):
    board.canvasSetup('X','O',userInfo)
    board.runUI()
                
if __name__ == '__main__':
    makeConnection()
            
    


