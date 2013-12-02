# program template for Rice Rocks
# Final assignment for Coursera course An Introduction to Interactive Programming in Python
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
missile_group = set()
rock_group = set()
explosion_group = set()
num_lives = 3
num_collisions = 0
game_started = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions 
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Helper function to draw group
def process_sprite_group(group, canvas):
    remove = set()
    for sprite in group:
        # Check if sprite still needs to be drawn
        if sprite.update():
            sprite.draw(canvas)
        else:
            remove.add(sprite)
    group.difference_update(remove)
           
            
# helper function for single object collision with group            
def group_collide(group, another_object):
    global num_lives, explosion_group, score 
    num_collisions = 0
    collided = set()
    for sprite in group:
        if sprite.collide(another_object):
            num_collisions += 1
            collided.add(sprite)
            an_explosion = Sprite([sprite.pos[0], sprite.pos[1]], [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            #num_lives -= 1
            #if num_lives == 0:
            #    game_over()
            #    print 'Game over'
            
    group.difference_update(collided) 
    return num_collisions

# helper function for group-group collisions
def group_group_collide(group1, group2):
    global score
    collided = set()
    for sprite in group1:
        if group_collide(group2, sprite) and game_started: 
            collided.add(sprite)
            score += 10
    group1.difference_update(collided)     
    return score

def game_over():
    global game_started, score
    score = 0
    reset_game()
    game_started = False
    soundtrack.rewind()
    
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    # draw appropriate image depending on whether thrust applied    
    def draw(self,canvas):
        if not self.thrust: 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size , self.angle)
            ship_thrust_sound.rewind()
        else:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), self.image_size, self.pos, self.image_size , self.angle)
            ship_thrust_sound.play()
        
    def update(self):   
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
        # apply forward acceleration along with friction
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] / 5 
            self.vel[1] += forward[1] / 5
            self.vel[0] *= 0.97 #friction
            self.vel[1] *= 0.97                     
                    
        # apply only friction if ship not accelerating    
        elif not self.thrust:
            self.vel[0] = self.vel[0]*0.99
            self.vel[1] = self.vel[1]*0.99 
        
        #run helper to wrap the ship on screen
        self.pos = keep_onscreen(self.pos)
        
        
    # instantiate missile sprites here
    def shoot(self):
        #global missile_group
        forward = angle_to_vector(self.angle)        
        a_missile = Sprite([self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]], [self.vel[0] + 5*forward[0],self.vel[1] + 5*forward[1]], self.angle, self.angle_vel, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:            
            canvas.draw_image(self.image, [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size , self.angle)
        else:	
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size , self.angle)

    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < (self.radius + other_object.radius):
            return True
                
    def update(self):
        if self.angle > 0:
            self.angle += 0.05        
        else:
            self.angle -= 0.05
        # Update position    
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]    
        self.pos = keep_onscreen(self.pos)
        
        #Update age
        self.age += 1
        
        # return true or false depending on if the object is still alive
        if self.age >= self.lifespan:
            return False
        else:
            return True
        
          
           
def draw(canvas):
    global time, score, game_started, num_lives   
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Always draw ship
    my_ship.draw(canvas) 
    
    # draw game interactable sprites
    if game_started:               
        process_sprite_group(rock_group, canvas)       
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        group_group_collide(rock_group, missile_group)
        if group_collide(rock_group, my_ship) > 0:
            num_lives -= 1
        if num_lives == 0:
            game_started = False
            game_over()    

    else:
        # Display splash screen        
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
       
    # update ship and sprites
    my_ship.update()
    

    
    # Draw User info
    canvas.draw_text('Lives: ', (20, 40), 25, 'White', 'sans-serif')
    canvas.draw_text('Score: ' + str(score), (WIDTH - 150 , 40), 25, 'White', 'sans-serif')

    # Draws ships instead of number for lives
    for i in range(num_lives):
        canvas.draw_image(ship_image,ship_info.center, ship_info.size, [110 + i * 40, 35],[40, 40], (-1) * math.pi / 2)
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group # game_started
    if game_started:
        while len(rock_group) < 10:
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            #rock_vel = 
            if dist(my_ship.pos, rock_pos) > my_ship.radius + asteroid_info.radius + 100:
                difficulty = (0.5 + 0.5 * score // 100)
                a_rock = Sprite(rock_pos, [difficulty * random.randrange(-1, 2), difficulty * random.randrange(-1, 2)], random.randrange(-1, 2), random.randrange(-1, 2), asteroid_image, asteroid_info)
                rock_group.add(a_rock)

        
# key down handler
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= 0.05
        my_ship.thrust = False
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += 0.05
        my_ship.thrust = False
    elif key == simplegui.KEY_MAP['down']:
        my_ship.thrust = False        
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
       

        
        
# keyup handler        
# slow down ship with friction, stop ship rotation
def keyup(key):
    my_ship.thrust = False
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0

        
# helper function for staying on screen
def keep_onscreen(pos):
    if pos[0] > WIDTH:
        pos[0] = pos[0] % WIDTH
    elif pos[0] < 0:
        pos[0] = pos[0] + WIDTH
    if pos[1] > HEIGHT:
        pos[1] = pos[1] % HEIGHT
    elif pos[1] < 0:
        pos[1] = pos[1] + HEIGHT
    return pos        

def reset_game():
    global num_lives, score, rock_group, missile_group, explosion_group
    explosion_group = set()
    rock_group = set()
    missile_group = set()
    num_lives = 3
    score = 0
    soundtrack.play()
    
# Begin game on mouse click
def click(pos):
    global game_started
    game_started = True
    reset_game()
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and rocks
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 1, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()

