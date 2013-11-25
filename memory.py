# implementation of card game - Memory

import simplegui
import random

# initialize variables
CARDS = range(8) + range(8)
CARD_HEIGHT = 100
CARD_WIDTH = 50
exposed = []
matched = []
guessing = []
indexes = []
moves = 0
state = 0
# Load card back image
image = simplegui.load_image("http://farm4.staticflickr.com/3609/3426567435_7d9d476bbe.jpg")

# helper function to initialize globals
def new_game():
    """ reinitialize game """
    global state, exposed, matched, moves, guessing, indexes
    random.shuffle(CARDS)
    exposed = [False for i in range(16)]
    moves = 0
    state = 0
    guessing = []
    indexes = []
    label.set_text("Turns = " + str(moves))
    print "For debugging, cards are:\n", CARDS    
     
# define event handlers
def mouseclick(pos):
    """ Main game logic, determines if cards are shown """
    global state, exposed, moves, guessing, indexes   
    # Get card position
    card_no = pos[0]//50  
    if not exposed[card_no]:                      
        if state == 0: # for first click
            moves +=1 
            exposed[card_no] = True
            # Store the card value and its index
            guessing.append(CARDS[card_no])
            indexes.append(card_no)
            state = 1        
        elif state == 1: # for second click
            exposed[card_no] = True
            # Store the card value and its index
            guessing.append(CARDS[card_no])
            indexes.append(card_no)
            state = 2
        else:           
            # Upon 3rd card selection, check if previous two are a match
            moves +=1
            if guessing[0] == guessing[1]:
                # if a match is found                 
                # clear lists 
                guessing = []
                indexes = []
                # Continue game, populate with last card selected
                exposed[card_no] = True
                guessing.append(CARDS[card_no])
                indexes.append(card_no)              
            # if no match is found
            else:
                # Turn the unmatched cards back over
                exposed[indexes[0]] = False
                exposed[indexes[1]] = False
                indexes = []
                guessing =[]
                # Continue game, populate with last card selected
                exposed[card_no] = True
                guessing.append(CARDS[card_no])
                indexes.append(card_no)            
            state = 1
        label.set_text("Turns = " + str(moves))
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed
    #pos = 10;    
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(CARDS[i]), (10 + 50 * i, 75), 55, "White")            
        else:
            try: # to load the image
                IMG_SIZE_X = image.get_width()
                IMG_SIZE_Y = image.get_height()
                canvas.draw_image(image, (IMG_SIZE_X / 2, IMG_SIZE_Y / 2), (IMG_SIZE_X, IMG_SIZE_Y), (25 + 50 * i, 50), (48, 100))           
            except: # if it fails, draw green squares instead
                canvas.draw_polygon( [(i * 50, 0), (i * 50 + 49, 0), (i * 50 + 49, 99), (i * 50, 99)], 1, 'Green', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
