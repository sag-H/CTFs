import socket ,re ,time ,my_TicTacToeAI 

def roundAndGameStatus(who_starts_screen):
    if "Game tied" in who_starts_screen:
        global round_is_on
        round_is_on = False
        s.send(str.encode("\n"))
        who_starts_screen = s.recv(1024).decode("utf-8")
        print(who_starts_screen)

        #Flag is given like so: CSA{Flag}
        if "{" in who_starts_screen:
            global game_is_on
            game_is_on = False
            print("\nGame over! Thanks for playing.")
    
        global i
        if i == 0:
            i = 1
        else:
            i = 0

def getServerMove(who_starts_screen):
    #Since the server always outputs the move with a period
    #after it (eg: 9.), we use 2 regexes to extract it
    server_move = re.search(r"\d\.",who_starts_screen).group()
    server_move = re.search(r"\d",server_move).group()
    return int(server_move)

def serverMove():
    print("SERVER MOVE")
    server_move = getServerMove(who_starts_screen)
    my_TicTacToeAI.humanMove(server_move)

def botMove():
    print("BOT MOVE")
    my_TicTacToeAI.botMove()
    with open("Bot_move.txt","r") as f:
        bestMove = f.read()
    s.send(str.encode(bestMove + "\n"))
    print(s.recv(1024).decode("utf-8"))
    global who_starts_screen
    who_starts_screen = s.recv(1024).decode("utf-8")

funcs = [serverMove,botMove]

first_round = True
game_is_on = True
round_is_on = True
turn = 0
global who_starts_screen 

s = socket.socket()  
try:
    s.connect(('18.198.234.32', 4444))

    #Passing the welcome screen
    print(s.recv(1024).decode("utf-8")) 
    s.send(str.encode("\n"))
    
    while game_is_on:
        #Without sleep who_starts_screen is inconsistent
        time.sleep(0.2)
        who_starts_screen = s.recv(1024).decode("utf-8")
        print(who_starts_screen)
        
        #Due to player alternation after each round, we
        #only check the starting player of the first round
        if first_round:
            if "I'll" in who_starts_screen:
                i = 0 #serverMove,botMove
            else:
                i = 1 #botMove,serverMove
            first_round = False

        round_is_on = True
        while round_is_on:
            funcs[0 + i]()
            if turn == 4:
                roundAndGameStatus(who_starts_screen)
                turn = 0
            if round_is_on:
                funcs[1 - i]()
            turn += 1       
except:
    raise 
finally:
    s.close()