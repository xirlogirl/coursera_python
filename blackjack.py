# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object

    def __str__(self):
        return "Hand contains " + " ".join(str(card) for card in self.cards)
        
    def add_card(self, card):
        self.cards.append(card) # add a card object to a hand
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust        
        hand_value = 0
        has_ace = False
        for card in self.cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_ace = True

        if has_ace:          
            if hand_value + 10 <= 21:                  
                return hand_value + 10
            else:             
                return hand_value
        else:
            return hand_value

            
    def draw(self, canvas, pos):
        for card in self.cards:	# draw a hand on the canvas, use the draw method for card        
            card.draw(canvas, pos)
            # offset each card by 80
            pos[0] += 80
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(str(suit), str(rank))
                self.cards.append(card) 
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)  # use random.shuffle()

    def deal_card(self):
        deal = self.cards.pop()	# deal a card object from the deck
        return deal
    
    def __str__(self):
        return "Deck contains " + " ".join(str(card) for card in self.cards)	# return a string representing the deck


#define event handlers for buttons
def deal():
    global score, option, outcome, in_play, p1Hand, dHand, new_deck
    outcome = ''
    if in_play:
        # If player selects new deal partway through game a point is lost
        outcome = 'Player loses. New deal.'
        score -= 1
    new_deck = Deck()
    new_deck.shuffle()
    # Create hands for each 
    p1Hand = Hand()
    dHand = Hand()

    # Now deal cards from deck to hands
    p1Hand.add_card(new_deck.deal_card())
    p1Hand.add_card(new_deck.deal_card())
    #print 'P1', p1Hand.get_value()
 
    # Dealer   
    dHand.add_card(new_deck.deal_card())
    dHand.add_card(new_deck.deal_card())
    #print 'Dealer', dHand.get_value()
    
    # Prompt the player
    in_play = True
    option = ' Hit or stand?' #(' + str(p1Hand.get_value()) + ')'

def hit():
    global option, outcome, p1Hand, dHand, in_play, score
    # if the hand is in play, hit the player
    outcome = ''
    if in_play:
        p1Hand.add_card(new_deck.deal_card())
        option = 'Hit again or stand?' # (' + str(p1Hand.get_value()) + ')'
        #print 'Player hand is ', p1Hand.get_value()
    if in_play and p1Hand.get_value() > 21:
        outcome = 'Player goes bust and loses.' # with ' + str(p1Hand.get_value()) + '!'
        option = 'New Deal?'
        in_play = False
        score -= 1
       
def stand():
    # Main Blackjack game logic 
    global p1Hand, option, dHand, in_play, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        # First let the dealer obtain their score to 17 
        while dHand.get_value() < 17:
            dHand.add_card(new_deck.deal_card())
    
    # Now see who won
    # assign a message to outcome, update in_play and score
    # ask the player what they want to do
    if in_play and p1Hand.get_value() <= 21 and p1Hand.get_value() > dHand.get_value():
        outcome = 'Player wins with ' + str(p1Hand.get_value()) + '!'
        option = 'New Deal?'
        score += 1
        in_play = False
    elif in_play and dHand.get_value() >= p1Hand.get_value() and dHand.get_value() <= 21:
        outcome = 'Dealer wins with ' + str(dHand.get_value())
        option = 'New Deal?'
        score -= 1
        in_play = False
    elif in_play and dHand.get_value() > 21:
        outcome = 'Dealer busts with ' + str(dHand.get_value()) + '. Player wins!'
        option = 'New Deal?'
        score += 1
        in_play = False    
   
# draw handler    
def draw(canvas):
    global option, outcome, score
    # draw game logo, some fun background stuff
    canvas.draw_circle((300, -100), 300, 300, '#006400', '#006400')
    canvas.draw_circle((320, 80), 20, 20, 'White', 'White')
    canvas.draw_circle((310, 60), 20, 20, 'Blue', 'Blue')
    canvas.draw_text('BLACKJACK', [250, 60], 20, 'White', 'sans-serif')
    
    # test to make sure that card.draw works, replace with your code below
    p1Hand.draw(canvas, [50, 400])
    dHand.draw(canvas, [50, 170])
    if in_play:
        # cover up dealer's first card by drawing card back
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [85, 220], CARD_BACK_SIZE)
    else:
        # just draw the hand if not in play
        dHand.draw(canvas, [50, 170])

    
    # draw labels
    canvas.draw_text('Player', [50, 385], 20, 'White', 'sans-serif')
    canvas.draw_text('Dealer', [50, 155], 20, 'White', 'sans-serif')
    # draw messages to player
    canvas.draw_text(option, [225, 385], 20, 'White', 'sans-serif')
    canvas.draw_text(outcome, [225, 155], 20, 'Yellow', 'sans-serif')
    canvas.draw_text('Score: ' + str(score), [460, 50], 20, 'White', 'sans-serif')
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
