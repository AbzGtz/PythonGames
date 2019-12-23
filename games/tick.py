########################################################################
# Global Variables
########################################################################

player_setup = {'PL1':['token','turn'],'PL2':['token','turn']}  # Keeps track of a player's token - player_setup['PL1'][0] - and wheather is its turn - player_setup['PL1'][1]
standings = {'PL1':0,'PL2':0,'TIE':0}
win_combinations = ((1,2,3),(4,5,6),(7,8,9),(7,5,1),(9,5,3),(7,4,3),(8,5,2),(9,6,1))
board = list([' ']*10)
box_number = tuple(list('123456789'))
tokens = ('X','O')
game_count = 0
winner = ""

########################################################################
# TOP-Level functions
########################################################################

def check_game_status():
    """
    Checks if the game is over by examining the board entries and checking
    them against the known winning combinations.
    If the game is over, it will set the winner to X, O, or TIE.
    """
    global player_setup
    global win_combinations
    global board
    global winner

    for box1,box2,box3 in win_combinations:
        if board[box1] == board[box2] and board[box2] == board[box3] and board[box2] != " ":
             winner = board[box1]
             break
    else:
        if (board.count('X') + board.count('O')) == 9:
            winner = 'TIE'

def display_board():
    """
    Displays the Tick-Tack-Toe board and also a numbered pad so the user can remeber which
    tick-tack-toe box is mapped to which number in their keyboard.
    """
    global board
    global box_number

    print"\n"*100
    print"   |   |   " + " "*20 + "   |   |   "
    print " " + board[7] +" | "+ board[8] +" | " + board[9] + " "*20 + "  " + box_number[6] +" | "+ box_number[7] +" | " + box_number[8]
    print"   |   |   "  + " "*20 + "   |   |   "
    print "---|---|---" +  " "*20 +  "---|---|---"
    print"   |   |   " + " "*20 +  "   |   |   "
    print " " + board[4] +" | "+ board[5] +" | " + board[6] + " "*20 + "  " + box_number[3] +" | "+ box_number[4] +" | " + box_number[5]
    print"   |   |   " + " "*20 + "   |   |   "
    print "---|---|---" + " "*20 + "---|---|---"
    print"   |   |   " +  " "*20 + "   |   |   "
    print " " + board[3] +" | "+ board[2] +" | " + board[1] + " "*20 + "  " + box_number[2] +" | "+ box_number[1] +" | " + box_number[0]
    print"   |   |   "  +  " "*20 + "   |   |   "
    print"\n"*5

def make_a_move(player_token, box_selected = "none"):
    """
    Recursive function to ask users to make a move and select a numbered-box to take. This function
    also ensures the integraty of the input by the user with the below:
    1) If the player enter anything order than a valid number (e.g. 1-9), it will ask again for input.
    2) If the player enters a box already taken, it will tell so to teh user and reqeust for another entry
    After a successful move by a player, it calls check_game_status and gives turn to the game player
    """
    global board
    global player_setup

    display_board()
    if box_selected != "none":
        print "Square {} already has a {}.".format( box_selected, board[int(box_selected)])

    if player_token == player_setup['PL1'][0]:
        player = "Player 1"
        player_setup['PL1'][1] = ""
        player_setup['PL2'][1] = "GO"
    else:
        player = "Player 2"
        player_setup['PL1'][1] = "GO"
        player_setup['PL2'][1] = ""

    move = raw_input( "{} ({}). Enter the number of the box you want to take :".format(player, player_token))
    while move not in box_number:
        move = raw_input( "{} ({}). {} is not a valid entry. Enter the number of the box you want to take :".format(player, player_token, move))
    if board[int(move)] in tokens:
        make_a_move(player_token, move)
    else:
        board[int(move)] = player_token
    check_game_status()

def quit_game():

    print"\n"*100
    print "Thank you for playing !"
    print "Here are the final Stats:"
    print "************************************"
    print "#                                  #"
    print "#  Games Played: {}                 #".format(game_count)
    print "#  Player 1: {} wins                #".format(standings['PL1'])
    print "#  Player 2: {} wins                #".format(standings['PL2'])
    print "#  Ties :    {}                     #".format(standings['TIE'])
    print "#                                  #"
    print "************************************"
    print "\n"
    quit()

def reset_game ():
    global player_setup
    global board
    global winner

    player_setup = {'PL1':['token','turn'],'PL2':['token','turn']}
    board = list([' ']*10)
    winner = ""

def select_player():
    global player_setup

    token1 = " "

    while token1 not in ['X','O','Q']:
        token1 = raw_input( "Player 1: select your token ( O, X or q to quit): " ).upper()
    if token1 == 'Q':
        quit_game()
    elif token1 == 'X':
        player_setup['PL1'] = [token1,'GO']
        player_setup['PL2'] = ['O','']
    else:
        player_setup['PL1'] = [token1,'GO']
        player_setup['PL2'] = ['X','']

def welcome_display():
    global game_count
    global standings

    print"\n"*100
    print "************************************"
    print "#                                  #"

    if game_count == 0:
        print "#  Welcome to Tic Tac Toe Game !   #"
        print "#                                  #"
    else:
        print "#  Welcome to Game # {}             #".format((game_count+1))
        print "#  Standings:                      #"
        print "#  Player 1: {} wins                #".format(standings['PL1'])
        print "#  Player 2: {} wins                #".format(standings['PL2'])
        print "#  Ties :    {}                     #".format(standings['TIE'])

    print "#                                  #"
    print "************************************"
    print "\n"*5

########################################################################
# main_game_fuction controls the flow of the game
########################################################################

def main_game_fuction ():
    global winner
    global player_setup
    global game_count

    welcome_display()
    select_player()
    while winner == "":
        if player_setup['PL1'][1] == 'GO':
            make_a_move(player_setup['PL1'][0])
        else:
             make_a_move(player_setup['PL2'][0])
    display_board()
    if winner == 'TIE':
        print " WE HAVE A TIE GAME !!! "
        standings['TIE']+=1
    elif winner == player_setup['PL1'][0]:
        print " PLAYER 1 WINS !!!\n"
        standings['PL1']+=1
    else:
        print " PLAYER 2 WINS !!!\n"
        standings['PL2']+=1
    game_count += 1

    result = raw_input('Would you like to play again: [y] for YES: ')
    if result.upper() == 'Y':
        reset_game ()
        main_game_fuction ()
    else:
        quit_game()

########################################################################
# main_game_fuction call
########################################################################
main_game_fuction()
