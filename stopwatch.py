# This is a simple game which displays a clock which starts 
# when the player hits the start button. Points are awarded if 
# the player stops the watch on any integer number of seconds,
# that is when the tenths digits is equal to zero
# The score is displayed as a fraction on the canvas.

import simplegui

# Define global variables (program state)
counter  = 0 
interval = 100
message = 0.0
timer_run = False
points = 0
stopcounter = 0
scoreboard = "SCORE : " + str(points) + "/" + str(stopcounter)

# define helper functions
def format(t):
    """ converts time in tenths of seconds into formatted string A:BC.D """
    t = t/100 				# conversion
    no_secs = t/10	 		# so units below are understandable 
    A = no_secs//60			# minutes
    B = (no_secs%60)//10	# tens of seconds
    C = (no_secs%60)%10		# seconds
    D = t%10				# fraction of second
    message = str(A)+":"+str(B)+ str(C)+"."+str(D)
    return message
            
# define event handler for timer with 0.1 sec interval    
def increment():
    """ Increment by interval specified """
    global counter 
    counter = counter + interval

# event handlers for buttons; "Start", "Stop", "Reset"
def tick():
    """ Increment the clock """
    increment()
     
def start():
    """ Begins timer from initial value """
    global timer_run
    timer.start()
    timer_run = timer.is_running()

def stop():
    """ Stops timer, updates score """
    global scoreboard, points, stopcounter, timer_run
    # Run the sequence of checking the score only if the timer is running   
    if timer.is_running():   
        score()
        timer.stop()
        stopcounter += 1
        # update the scoreboard
        scoreboard = "SCORE : " + str(points)+ "/" + str(stopcounter)       
            
def reset():
    """ make it reset counter and score to 0 """
    global points, stopcounter, counter, scoreboard
    counter = 0 
    stopcounter = 0
    points = 0
    timer.stop()
    scoreboard = "SCORE : " + str(points) + "/" + str(stopcounter)

def score():
    """ Determine if a point should be awarded """
    global points, timer_run 
    check = (counter/100)%10
    if timer_run and check == 0:
        points += 1    
    return points 
    
# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(format(counter), [110,160], 36, "White")
    canvas.draw_text(scoreboard, [190,50], 18, "Green")   

# Create a frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# Register event handlers
timer = simplegui.create_timer(interval, tick)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset) 
frame.set_draw_handler(draw)

# Start frame
frame.start()
