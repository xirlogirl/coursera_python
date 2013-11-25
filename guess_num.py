# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math


# initialize global variables used in your code
num_range = 100
max_guesses = 7 

# helper function to start and restart the game
def new_game():
    global num_guesses, answer
    # start game   
    f.start()
    # pick the number based on the number range
    answer = random.randrange(0, num_range)
    # initialize guesses
    num_guesses = 0
    # Display information to player
    print "New game. Range is from 0 to", num_range
    print "Maximum number of guesses is", max_guesses
    print ""
    


# define event handlers for control panel
# guess range [1 to 100)
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range, max_guesses
    num_range = 100
    max_guesses = 7
    new_game()
  
    
# guess range [1 to 1000)
def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range, max_guesses
    num_range = 1000
    max_guesses = 10 
    new_game()
    
        
def input_guess(guess):    
    global num_guesses, max_guesses, answer
    # increment number of guesses with each entry
    num_guesses +=1

    # get and convert the player guess
    player_guess = int(guess)
    a = num_guesses < max_guesses
    
    # Check the player guess and if its less than no. of allowed guesses
    # set up to restart the game if needed
    if a and player_guess < answer:
        feedback  = "Higher!"
        restart = False
    elif a and player_guess > answer:
        feedback = "Lower!"
        restart = False
    elif player_guess == answer:
        feedback = "Correct!"
        restart = True
    elif not a:
        feedback = ("You ran out of guesses. The number was " + str(answer))
        restart = True
    
    # Display output
    print "You guessed", player_guess 
    print "Number of remaining guesses is:", max_guesses-num_guesses
    print feedback
    print ""
    
    # Start a new game if necessary
    if restart:
        new_game()
  
    
    
    
    

    
# create window
f = simplegui.create_frame("Guess the number", 200, 200)

# create the control elements for the window
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# register event handlers for control elements



# call new_game and start frame
new_game()


# always remember to check your completed program against the grading rubric
