import socket ,re , my_TicTacToeAI

def whoStarts(screen):
    server_turn_reg = re.compile(r"I'll go first") 
    my_turn_reg = re.compile(r"You go first")

    if server_turn_reg.search(screen):
        return "server"
    elif my_turn_reg.search(screen):
        return "me"
    else:
        return "No match"

def serverMain():
    s = socket.socket()         
    
    #Since the server always outputs the move with a period
    #after it (eg: 9.), we use 2 regexes to extract it
    server_move_reg1 = re.compile(r"\d\.")
    server_move_reg2 = re.compile(r"\d")

    game_ended_reg = re.compile(r"Game tied")
    
    try:
        port = 4444              
        s.connect(('18.198.234.32', port))

        #Printing and passing welcome screen
        print(s.recv(1024).decode("utf-8")) 
        s.send(str.encode("\n"))  
        
        for i in range(my_TicTacToeAI.getGamesToPlay()):
            who_starts_screen = s.recv(1024).decode("utf-8")
            print(who_starts_screen)

            #If the server starts:
            if whoStarts(who_starts_screen) == "server":
                is_server_game = True
                while is_server_game == True:

                    server_move = re.search(server_move_reg1,who_starts_screen).group()
                    server_move = re.search(server_move_reg2,server_move).group()                   

                    #Playing the server move against the bot
                    my_TicTacToeAI.myMove(int(server_move))

                    if game_ended_reg.search(who_starts_screen):
                        is_server_game = False
                        s.send(str.encode("\n"))
                        who_starts_screen = s.recv(1024).decode("utf-8")
                        print(who_starts_screen)
                    
                    my_TicTacToeAI.botMove()      

                    #Sending the bot's response to the server
                    with open("Bot_move.txt","r") as f:
                        bestMove = f.read()
                    s.send(str.encode(bestMove + "\n"))
                    print(s.recv(1024).decode("utf-8"))
                    who_starts_screen = s.recv(1024).decode("utf-8")
                                         
            #I start:
            elif whoStarts(who_starts_screen) == "me":
                is_my_game = True
                while is_my_game == True:

                    print("@@@@@@@@@@ MY TURN @@@@@@@@@@")
                    break
    except:
        raise 
    finally:
        s.close()