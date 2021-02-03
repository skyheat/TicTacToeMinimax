import numpy as np
from math import inf as infinity

#Plays the move in the current state by the player
def playMove(state, player, move):
    if state[int((move-1)/3)][(move-1)%3] == ' ':
        state[int((move-1)/3)][(move-1)%3] = player
    else:
        move = int(input(str(move) + " has already been chosen. Choose again: "))
        playMove(state, player, move)
    
def checkState(gameState):
    
    #Horizontal Check
    for i in range(3):
        if gameState[i][0] == gameState[i][1] and gameState[i][0] == gameState[i][2] and gameState[i][0] != ' ':
            return gameState[i][0], "Done"
    
    #Vertical Check
    for i in range(3):
        if gameState[0][i] == gameState[1][i] and gameState[1][i] == gameState[2][i] and gameState[0][i] != ' ':
            return gameState[0][i], "Done"
    
    #Diagonal Check
    if (gameState[0][0] == gameState[1][1] and gameState[1][1] == gameState[2][2] and gameState[0][0] != ' '):
        return gameState[1][1], "Done"
    if (gameState[2][0] == gameState[1][1] and gameState[1][1] == gameState[0][2] and gameState[2][0] != ' '):
        return gameState[1][1], "Done"

    #Draw Check, checks to see if every spot on the board has been chosen
    draw = False
    for i in range(3):
        for j in range(3):
            if gameState[i][j] == ' ':
                draw = True
    if draw == False:
        return None, "Draw"
    
    return None, "Not Done"

#Prints the board
def printBoard(gameState):
    print('----------------')
    for i in range(3):
        print('| ' + str(gameState[i][0]) + ' || ' + str(gameState[i][1]) + ' || ' + str(gameState[i][2]) + ' |')
        print('----------------')
    
#Copies and returns the current state
def copyState(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state

#Returns a list of valid moves from the current state    
def validMoves(state):
    moves = []
    empty_cells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                empty_cells.append(i*3 + (j+1))
    return empty_cells  

#Returns the best move to play from the state
#If moves are of equal value, will play the 1st move
def getNextMove(state):
    currentBestMove = 0
    currentBestScore = -infinity
    moves = validMoves(state)
    for move in moves:
        copy_state = copyState(state)
        playMove(copy_state, "O", move)
        score = getMoveScore(copy_state, 0)
        if score > currentBestScore:
            currentBestMove = move
            currentBestScore = score
    return currentBestMove

#Changes the player
def invertPlayer(player):
    return (player + 1)%2

#Minimax algorithm
#As depth in Tic Tac Toe is quite low, Alpha Beta pruning is not needed
def getMoveScore(state, playerTurn):
    winner_loser, done = checkState(state)
    if done == "Done":
        if winner_loser == "O":
            return 1
        elif winner_loser == "X":
            return -1
    elif done == "Draw":
        return 0

    if playerTurn == 1:
        maxv = -infinity
        for move in validMoves(state):
            copy_state = copyState(state)
            playMove(copy_state, players[playerTurn], move)
            maxscore = getMoveScore(copy_state, invertPlayer(playerTurn))
            if maxscore > maxv:
                maxv = maxscore
        return maxv
    else:
        minv = infinity
        for move in validMoves(state):
            copy_state = copyState(state)
            playMove(copy_state, players[playerTurn], move)
            minscore = getMoveScore(copy_state, invertPlayer(playerTurn))
            if minscore < minv:
                minv = minscore
        return minv

#Main
players = ['X','O']
play = input("Play?(y/n)")
while play == 'Y' or play == 'y':
    gameState = [[' ',' ',' '], [' ',' ',' '], [' ',' ',' ']]
    gameStatus = "Not Done"
    print('\n----------------')
    print("\nNew Game")
    printBoard(gameState)
    playerTurn = input("Input which player goes first - X (You) or O(AI): ")
    winner = None
    if playerTurn == "x" or playerTurn == "X":
        currentPlayer = 0
    else:
        currentPlayer = 1
    while gameStatus == "Not Done":
        if currentPlayer == 0: # Player's turn
            moveChoice = int(input("It is " + str(players[currentPlayer]) + "'s turn. Input move (1 - 9): "))
            playMove(gameState ,players[currentPlayer], moveChoice)
        else:   # Minimax's turn
            moveChoice = getNextMove(gameState)
            playMove(gameState ,players[currentPlayer], moveChoice)
            print("Minimax plays move: " + str(moveChoice))
        printBoard(gameState)
        winner, gameStatus = checkState(gameState)
        if winner != None:
            print(str(winner) + " is the winner")
        else:
            currentPlayer = invertPlayer(currentPlayer)
        
        if gameStatus == "Draw":
            print("Draw!")
            
    play = input('Play again?(Y/N): ')
    if play == 'N' or play == "n":
        print('Goodbye')
print('Goodbye')
