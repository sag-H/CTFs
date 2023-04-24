import socket

def printBoard(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])
    print("\n")

def resetBoard(board):
    board[1] = ' '
    board[2] = ' '
    board[3] = ' '
    board[4] = ' '
    board[5] = ' '
    board[6] = ' '
    board[7] = ' '
    board[8] = ' '
    board[9] = ' '

def isSpaceFree(position):
    if board[position] == ' ':
        return True
    else:
        return False

def insertLetter(letter, position):
    if isSpaceFree(position):
        board[position] = letter
        if isDraw() or isWin():
            resetBoard(board) 
            print("Board Reset!")   
        return
    else:
        print(position,"Is taken, enter new one:")
        position = int(input())
        insertLetter(letter, position)
        return

def isWin():
    if (board[1] == board[2] and board[1] == board[3] and board[1] != ' '):
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] != ' '):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] != ' '):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] != ' '):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] != ' '):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] != ' '):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] != ' '):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] != ' '):
        return True
    else:
        return False

def thisPlayerWon(player):
    if board[1] == board[2] and board[1] == board[3] and board[1] == player:
        return True
    elif (board[4] == board[5] and board[4] == board[6] and board[4] == player):
        return True
    elif (board[7] == board[8] and board[7] == board[9] and board[7] == player):
        return True
    elif (board[1] == board[4] and board[1] == board[7] and board[1] == player):
        return True
    elif (board[2] == board[5] and board[2] == board[8] and board[2] == player):
        return True
    elif (board[3] == board[6] and board[3] == board[9] and board[3] == player):
        return True
    elif (board[1] == board[5] and board[1] == board[9] and board[1] == player):
        return True
    elif (board[7] == board[5] and board[7] == board[3] and board[7] == player):
        return True
    else:
        return False

def isDraw():
    for key in board.keys():
        if board[key] == ' ':
            return False
    return True

def minimax(board,isMaximizing):
    if (thisPlayerWon(bot)):
        return 1
    elif (thisPlayerWon(human)):
        return -1
    elif (isDraw()):
        return 0

    #If we are the bot this is our bot:
    if (isMaximizing):
        bestScore = -1000
        for key in board.keys():
            if (board[key] == ' '):
                board[key] = bot
                score = minimax(board,False)
                board[key] = ' '
                if (score > bestScore):
                    bestScore = score
        return bestScore

    #And this is the opponent's bot:
    #These two will play each other until 
    #someone wins or it's a draw
    else:
        bestScore = 1000
        for key in board.keys():
            if (board[key] == ' '):
                board[key] = human
                score = minimax(board,True)
                board[key] = ' '
                if (score < bestScore):
                    bestScore = score
        return bestScore

def humanMove(server_move):

    #This line converts the server's move to it's magic-square position.
    #Using server's move as a position(value) in the dict to get it's key. 
    server_move = list(magic_to_board.keys())[list(magic_to_board.values()).index(server_move)]

    insertLetter(human, server_move)
    printBoard(board)
    return

def botMove():
    #Bot is the maximizing player, so the lower
    #the move's score - the better it is
    bestScore = -1000
    #0 is placeholder. Our moves are 1-9
    bestMove = 0 
    for key in board.keys():

        #If the spot is empty we want to play it
        #so that we eventually play every variation
        if (board[key] == ' '):
            board[key] = bot

            score = minimax(board,False)
            
            #Reverting what we did so that we can
            #play the next move, while still remembering
            # the score of the pos before reverting
            board[key] = ' '

            #Updating the best score overall
            #and the best move(key)
            if (score > bestScore):
                bestScore = score
                bestMove = key
    insertLetter(bot, bestMove)

    print("Bot's move:",bestMove,"(",magic_to_board[bestMove],")")
    printBoard(board)

    #Outputting the bot's move to the server
    with open("Bot_move.txt","w") as f:
        f.write(str(magic_to_board[bestMove]))
    return 

board = {1: ' ', 2: ' ', 3: ' ',
         4: ' ', 5: ' ', 6: ' ',
         7: ' ', 8: ' ', 9: ' '}

magic_to_board = {1:8 , 2:1 , 3:6 ,
                  4:3 , 5:5 , 6:7 ,
                  7:4 , 8:9 , 9:2}

human = 'O'
bot = 'X'