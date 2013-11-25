# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0
paddle1_pos = HEIGHT / 2 - 40
paddle2_pos = HEIGHT / 2 - 40
paddle1_vel = 0
paddle2_vel = 0
acc = 5

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(2, 4),random.randrange(1, 3)]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == RIGHT:
        ball_vel = [random.randrange(2,4),-random.randrange(1,3)]
    elif direction == LEFT:
        ball_vel = [-random.randrange(2,4),-random.randrange(1,3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)

def buttonreset_handler():
    """ resets the score, starts a new game """
    global score1, score2, ball_pos
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    score1 = 0
    score2 = 0
    new_game()
    

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # collide and reflect off of bottom side of canvas
    if ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS :
        ball_vel[1] = - ball_vel[1]
        
    # collide and reflect off of bottom side of canvas
    if ball_pos[1] <= BALL_RADIUS :
        ball_vel[1] = - ball_vel[1]
    
        
    # check what to do when ball reaches player 1 defensive zone
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
        # reflect off paddle
        if ball_pos[1]>= paddle1_pos and ball_pos[1]<=paddle1_pos + PAD_HEIGHT:
            ball_vel[0] = -1.1*ball_vel[0]
        else:
            # or score a point for player 2 and respawn ball
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            score2 += 1
            spawn_ball(RIGHT)
        
    
    # check what to do when the ball reaches player 2 defensive zone
    if ball_pos[0] > WIDTH -1 - BALL_RADIUS - PAD_WIDTH:
        # reflect off paddle
        if ball_pos[1]>= paddle2_pos and ball_pos[1]<=paddle2_pos + PAD_HEIGHT :
            ball_vel[0] = -1.1*ball_vel[0]
        else:
            # or score a point for player 1 and respawn ball
            ball_pos = [WIDTH / 2, HEIGHT / 2]
            score1 += 1
            spawn_ball(LEFT)               
            
    
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen    
    paddle1_pos = paddle1_pos + paddle1_vel 
    if paddle1_pos  >= HEIGHT - PAD_HEIGHT:
        paddle1_pos  = HEIGHT - PAD_HEIGHT
    if paddle1_pos  <= 0:
        paddle1_pos = 0
          
    # same for paddle 2
    paddle2_pos = paddle2_pos + paddle2_vel 
    if paddle2_pos  >= HEIGHT - PAD_HEIGHT:
        paddle2_pos  = HEIGHT - PAD_HEIGHT
    if paddle2_pos  <= 0:
        paddle2_pos = 0
    
    
    # draw paddles
    c.draw_line((PAD_WIDTH/2, paddle1_pos), (PAD_WIDTH/2, paddle1_pos + PAD_HEIGHT), PAD_WIDTH, 'White')
    c.draw_line((WIDTH - PAD_WIDTH/2, paddle2_pos), (WIDTH - PAD_WIDTH/2, paddle2_pos + PAD_HEIGHT), PAD_WIDTH, 'White')
    
    # draw scores
    c.draw_text(str(score1), (225, 100), 40, 'White')
    c.draw_text(str(score2), (350, 100), 40, 'White')            
    
def keydown(key):
    """ moves paddles up and down depending on keystroke """
    global paddle1_vel, paddle2_vel    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = paddle1_vel - acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle1_vel + acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = paddle2_vel - acc      
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle2_vel + acc 
   
def keyup(key):
    """ stops motion of paddle whren key is no longer pressed """
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0      
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button('Reset', buttonreset_handler)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
