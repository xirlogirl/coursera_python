# Rock-paper-scissors-lizard-Spock
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random

def number_to_name(number):

    # convert a numeric value to its string equivalent
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name == "scissors"
    else:
        print "Invalid number."
    return(name)

    
def name_to_number(name):
    # convert a string to its numeric value
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1       
    elif name == "paper":
        number = 2        
    elif name == "lizard":
        number = 3 
    elif name == "scissors": 
        number = 4
    else:
        print "Invalid name."
    return(number)

def rpsls(name): 
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)

    # compute difference of player_number and comp_number modulo five
    # determine winner using if/elif
    difference = (player_number - comp_number) % 5
    if difference ==1 or difference == 2:
        winner = 'Player wins!'
    elif difference >= 3:
        winner = 'Computer wins!'
    else: 
        winner = 'Player and computer tie!'

    
    # print results
    print 'Player chooses', name
    print 'Computer chooses', number_to_name(comp_number)
    print winner
    print '\n'
    
    
# test of code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
