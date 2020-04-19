# Global Variables
card_values = {"ACE":0,"TWO":2,"THREE":3,"FOUR":4,"FIVE":5,"SIX":6,"SEVEN":7,"EIGHT":8,"NINE":9,"TEN":10,"JACK":10,"QUEEN":10,"KING":10}
ace_values = {0:(0,0),1:(1,11),2:(2,12),3:(3,13),4:(4,14)}  #ace values based on count
card_suits = ("Hearts","Dimonds","Spades","Clubs")
deck_of_cards = []
black_jack_players = []
TOLERANCE = 50.0  # % of total eiarnings on the table that the dealer will keep on playng for 
num_players = 0

#packages
from random import shuffle
from random import randint
import time

def calculate_winnings():
    global black_jack_players
    dealer = black_jack_players[0]
    player_status = ""
    dealer_status = ""
    output_string = ""
    dealer_amount = 0

    for player in (item for item in black_jack_players[1:] if item.is_active()):
        if not(player.is_bust()):
            if dealer.get_black_jack_total() > player.get_black_jack_total() and not(dealer.is_bust()):
                player_status = "LOSS"
                dealer_status = "WIN"
                dealer_amount = player.get_current_bet()
            elif dealer.get_black_jack_total() == player.get_black_jack_total():
                player_status = "PUSH"
                dealer_Status = "PUSH"
                dealer_amount = 0
            else:
                player_status = "WIN"
                dealer_status = "LOSS"
                dealer_amount = -(player.get_current_bet())
        else:
            player_status = "LOSS"
            dealer_status = "WIN"
            dealer_amount = player.get_current_bet()

        if player_status == "WIN":
            if dealer.is_bust():
                output_string = "{} wins ${} dollars with {} points vs {} who busts with {} points.".format(player.name,player.get_current_bet(),player.get_black_jack_total(),dealer.name,dealer.get_black_jack_total())
            else:
                output_string = "{} wins ${} dollars with {} points vs {} with {} points.".format(player.name,player.get_current_bet(),player.get_black_jack_total(),dealer.name,dealer.get_black_jack_total())
        elif player_status == "PUSH":
            output_string = "For {} is a PUSH with the dealer with {} points".format(player.name,player.get_black_jack_total())
        else:
            if player.is_bust():
                output_string = "{} busts with {} points.".format(player.name,player.get_black_jack_total())
            else:
                output_string = "{} lost ${} dollars with {} points vs {} with {} points.".format(player.name,player.get_current_bet(), player.get_black_jack_total(),dealer.name,dealer.get_black_jack_total())
        print output_string
        player.update_moneys(player_status)
        dealer.update_money_earnings(dealer_amount)

def num_of_active_users():
    global black_jack_players
    total = 0
    for i in black_jack_players:
        if i.is_active():
            total+=1
    return total

def get_num_players():
    return num_players

def increase_num_players():
    global num_players
    num_players += 1

def build_deck():
    global card_values
    global deck_of_cards
    global deck_suits

    for suit in card_suits:
        for card in card_values.keys():
            deck_of_cards.append(Card(card,suit))

def deal_a_card(player = ""):
    global black_jack_players
    global deck_of_cards

    if player == "":
        for player in black_jack_players:
            if player.is_active():
                player.get_a_card(deck_of_cards.pop())
    else:
        if player.is_active():
            player.get_a_card(deck_of_cards.pop())

def get_percentage_win():
    global black_jack_players
    win_total = 0
    total_bet = 0
    for player in (item for item in black_jack_players[1:] if item.is_active()):
        if not(player.is_bust()):
            total_bet += player.get_current_bet()
            if black_jack_players[0].get_black_jack_total() >= player.get_black_jack_total():
                win_total += player.get_current_bet()
    if total_bet == 0:
        total_bet = 1
        win_total = 1
    return (float(win_total)/total_bet)*100

def place_bets():
    global black_jack_players
    for player in black_jack_players[1:]:
         if player.is_active():
             while True:
                 try:
                     mybet = int(raw_input("Welcome {} - Enter your bet : ".format(player.name)))
                 except:
                     print "That is not a valid number(integer)." 
                 else:
                     if player.bet(mybet) > 0:
                         break

def play_next_game():
    global black_jack_players
    keep_playing = ""

    for player in black_jack_players[1:]:
        if player.is_active():
            keep_playing = ""
            if player.get_money() > 0:
                while keep_playing not in ("Y","N"):
                    keep_playing = raw_input("{}: you have {} in the bank and your total earnings are {}. Would you like to play again: ".format(player.name,player.get_money(),player.get_earnings())).upper()
                if keep_playing == "N":
                    print "Thanks for playing today {}!".format(player.name)
                    player.inactivate()
                else:
                    print "Game ON {}".format(player.name)
                    player.reset_hand()
            else:
                print "{} You have no money left in the bank to play. Your final earings are {}".format(player.name, player.get_earnings())
                player.inactivate()

def reset_deck():
    global deck_of_cards
    global black_jack_players

    deck_of_cards = []
    build_deck()
    shuffle_deck()
    black_jack_players[0].reset_hand()

def set_up_players():
    global black_jack_players
    global num_players
    name  = ""
    result = ""

    black_jack_players.append(Player("Dealer",True))
    while result != "Q" and num_players < 5:
        result = raw_input("Press [Enter] to add a new player. Press [q] to quit: ").upper()
        if result != "Q":
            num_players += 1
            print "\n"*100
            name  =  raw_input("Enter a name for the player. Press [Enter] to keep the default as Player[{}]: ".format(num_players))
            black_jack_players.append(Player(name))
            print "\n"*100
    print "\n"*100

def shuffle_deck():
    global deck_of_cards
    num = randint(1,10)
    i = 0
    while i < num:
        shuffle(deck_of_cards)
        i+=1

def welcome_display():
    print"\n"*100
    print "************************************"
    print "#                                  #"
    print "#     Welcome To Black Jack        #"
    print "#                                  #"
    print "************************************"
    print "\n"*5

class Card:
    value = ""
    suit = ""

    def __init__(self,value,suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return "{} of {}".format(self.value,self.suit)

class Hand(object):
    hand = []
    _BJ_total = 0;

    def __init__(self):
        self._BJ_total = 0
        self. hand = []

    def get_a_card(self,card):
        self.hand.append(card)

    def get_top_card(self):
        return self.hand[-1]

    def __str__(self):
        for card in self.hand:
            print card
        return ""

    def get_black_jack_total(self):
        self._BJ_total = 0
        list_of_values  = []
        for item in self.hand:
            self._BJ_total += card_values[item.value]
            list_of_values.append(item.value)

        ace1,ace2 = ace_values[list_of_values.count("ACE")]
        
        if (self._BJ_total + ace1) == 21 or (self._BJ_total + ace2) > 21:
            self._BJ_total += ace1
        else:
            self._BJ_total += ace2

        return self._BJ_total

    def reset_hand(self):
        self.hand = []

    def is_hand_complete(self):
        return len(self.hand) == 5
        
class Player(Hand):
    name = ""
    _money = 0
    _current_bet = 0
    _earnings = 0
    _active_status = ""

    def __init__(self,name = "", dealer = False, money = 100):
        super(Player,self).__init__()
        if name == "":
            self.name = "Player["+str(get_num_players())+"]"
        else:
            self.name = name
        if not(dealer) :
            self._money = money
        self._active_status = "A"

    def __str__(self):
        return "{} has {} left in the account. Earnings so far {}".format(self.name,self._money,self._earnings)

    def bet(self,bet_amount):
        if bet_amount > self._money:
            print "You can't bet {}. You only have {} in your account.".format(bet_amount,self._money)
            bet_amount = 0
        else:
            self._money -= bet_amount
            self._current_bet = bet_amount
        return bet_amount

    def update_money_earnings(self,amount):
        self._money += amount
        self._earnings += amount

    def update_moneys(self,result):
        if result == "WIN":
            self._money += (self._current_bet)*2
            self._earnings += self._current_bet
        elif result == 'PUSH':
            self._money += (self._current_bet)
        else:
            self._earnings -= self._current_bet
        self._current_bet = 0

    def get_current_bet(self):
        return self._current_bet

    def get_earnings(self):
        return self._earnings

    def get_money(self):
        return self._money

    def is_active(self):
        return self._active_status == "A"

    def inactivate(self):
        self._active_status = "I"

    def is_bust(self):
        return self.get_black_jack_total() > 21

    def show_hand(self):
        return super(Player,self).__str__()

def play_the_game():
    global black_jack_players
    global deck_of_cards
    more_cards = ""
    player = ""
    dealer = ""

    welcome_display()
    build_deck()
    shuffle_deck()
    set_up_players()
    place_bets()
    dealer =  black_jack_players[0]
    while num_of_active_users() > 1:
        print "\n"*100
        print "Dealing cards ..."
        time.sleep(3)
        deal_a_card()
        deal_a_card()
        for player in (item for item in black_jack_players[1:] if item.is_active()):
            while True:
                more_cards = ""
                print "\n"*100
                print "The dealer's top card is:"
                print  dealer.get_top_card()
                print "\n"
                print "{} : Your total is {} ".format(player.name,player.get_black_jack_total())
                print player.show_hand()
                if not(player.is_bust()): 
                    print "\n"*3
                    while more_cards not in ['N','Y'] and not(player.is_hand_complete()):
                        more_cards = raw_input("Would you like another card (y/n) : ").upper()
                    if more_cards == "Y":
                        deal_a_card(player)
                    else:
                        print "\n"*100
                        print "{} is staying with {} points.".format(player.name, player.get_black_jack_total()) 
                        print player.show_hand()
                        print "..."
                        time.sleep(3)
                        break
                else:
                    print "\n"*100
                    print "{} busts with {} points:".format(player.name,player.get_black_jack_total())
                    print player.show_hand()
                    print "..."
                    time.sleep(3)
                    break
        get_more_cards = True
        while True:
           print "\n"*100
           print "{}'s current hand with {} points:".format(dealer.name,dealer.get_black_jack_total())
           print dealer.show_hand()
           if not(dealer.is_bust()) and get_percentage_win() < TOLERANCE:
               print "Dealer is getting a card ..." 
               time.sleep(3)
               deal_a_card(dealer)
           elif dealer.is_bust():
               print "\n"*100
               print "Dealer busts with {} points !".format(dealer.get_black_jack_total())
               print dealer.show_hand()
               print "..."
               time.sleep(4)
               break
           else:
               print "\n"*100
               print "{} is staying with {} points.".format(dealer.name, dealer.get_black_jack_total())
               print dealer.show_hand()
               print "..."
               time.sleep(4)
               break
        print "\n"*100
        calculate_winnings()
        time.sleep(5)
        print "\n"*2
        play_next_game()
        reset_deck()
        place_bets()

    print "\n"*100
    print "***********************"
    print "* Game Statistics:"
    print "***********************"
    for player in black_jack_players[::-1]:
        print "* {} ended up with {} dollars: {} of total earnings".format(player.name,player.get_money(),player.get_earnings())
    print "***********************"
    print "\n"*5

play_the_game()
