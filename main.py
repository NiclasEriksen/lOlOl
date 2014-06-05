import pygame
from pygame import transform
import PyParticles
import random, os, struct
from math import pi
# Check for android module and does stuff
try:
    import android
except ImportError:
    android = None
# Check for PIL, not working on android yet
try:
    from PIL import Image
    import PyColorize
except ImportError:
    try:
        import Image
        import PyColorize
    except ImportError:
        Image = None
        print ("PIL not found, not generating colored balls/court.")

# Android stuff
TIMEREVENT = pygame.USEREVENT

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    print ("DPI:{0}".format(android.get_dpi()))
pygame.init()

######### S E T T I N G S #########
#(WIDTH, HEIGHT) = (800, 1280)
(WIDTH, HEIGHT) = (720, 1280)
if android:
    if android.get_dpi() == 320:
        (WIDTH, HEIGHT) = (480, 800)

#(WIDTH, HEIGHT) = (480, 800)
WINDOW_TITLE = "LOLOL, like OLO, but it's not OLO"
FPS = 60
NOISE = False # Noise filter, destroys performance
L_BALLSIZE = int(HEIGHT/30)
M_BALLSIZE = int(HEIGHT/45)
S_BALLSIZE = int(HEIGHT/80)
LIVES = 8
BALL_HITPOINTS = 50
RANDOM_PLAYER_START = True
P_AREA_SIZE = HEIGHT/6 # Size of the player area in relation to the height
P1_COLOUR = "4f7ea9"
P2_COLOUR = "ff9743"
DARK_THEME = True

######### F I L E   L O A D I N G #########
FONT_FILE = "./font.ttf"
OSD_FONT_FILE = "./osd_font.ttf"
FONT = pygame.font.Font(FONT_FILE, 15)
OSD_FONT = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/15))
basePath = os.path.dirname(__file__)

if Image:
    ### HUE TESTING ###
    input_image_path = './img/new_ball_raw.png'
    # Colorizing P1
    result_image_path = './img/p1_ball.png'
    result = PyColorize.image_tint(input_image_path, '#%s' % P1_COLOUR)
    if os.path.exists(result_image_path):  # delete any previous result file
        result = PyColorize.image_tint(input_image_path, '#%s' % P1_COLOUR)
        os.remove(result_image_path)
    result.save(result_image_path)  # file name's extension determines format
    P1_BALL_IMG = pygame.image.load(result_image_path)

    # Colorizing P2
    result_image_path = './img/p2_ball.png'
    result = PyColorize.image_tint(input_image_path, '#%s' % P2_COLOUR)
    if os.path.exists(result_image_path):  # delete any previous result file
        os.remove(result_image_path)
    result.save(result_image_path)  # file name's extension determines format
    P2_BALL_IMG = pygame.image.load(result_image_path)
else:
    P1_BALL_IMG = pygame.image.load('./img/p1_ball.png')
    P2_BALL_IMG = pygame.image.load('./img/p2_ball.png')


#p1ballPath = os.path.join(basePath, "./img/red_ball.png") # P1 ball image
#P1_BALL_IMG = pygame.image.load(p1ballPath)
#p2ballPath = os.path.join(basePath, "./img/green_ball.png") # P2 ball image
#P2_BALL_IMG = pygame.image.load(p2ballPath)
DMG_BALL_IMG = pygame.image.load('./img/damaged_ball.png') # The damage indicator
SPLASH_IMG = pygame.image.load('./android-presplash.jpg') # The sweet splash logo
NEWROUND_IMG = pygame.image.load('./img/new_round.png')
QUIT_IMG = pygame.image.load('./img/quit.png')

if NOISE: # Aah, the things we do for grittyness
    noisescaledPath = './img/noise_scaled.png'
    NOISE_IMG = pygame.image.load('./img/noise.png')
    noise_img_scaled = pygame.transform.scale(NOISE_IMG, (WIDTH, HEIGHT))
    pygame.image.save(noise_img_scaled, noisescaledPath)
    NOISE_IMG = pygame.image.load(noisescaledPath)

P1_L_IMG = pygame.transform.scale(P1_BALL_IMG, (L_BALLSIZE*2, L_BALLSIZE*2))
P1_M_IMG = pygame.transform.scale(P1_BALL_IMG, (M_BALLSIZE*2, M_BALLSIZE*2))
P1_S_IMG = pygame.transform.scale(P1_BALL_IMG, (S_BALLSIZE*2, S_BALLSIZE*2))

P2_L_IMG = pygame.transform.scale(P2_BALL_IMG, (L_BALLSIZE*2, L_BALLSIZE*2))
P2_M_IMG = pygame.transform.scale(P2_BALL_IMG, (M_BALLSIZE*2, M_BALLSIZE*2))
P2_S_IMG = pygame.transform.scale(P2_BALL_IMG, (S_BALLSIZE*2, S_BALLSIZE*2))

######### C O L O U R S #########
#P1_BALL_COLOUR = (220,40,40)
#P2_BALL_COLOUR = (40,220,40)
#P1_WEAK_COLOUR = (220,110,110)
#P2_WEAK_COLOUR = (110,220,110)
P1_COLOUR_RGB = struct.unpack('BBB',P1_COLOUR.decode('hex'))
P2_COLOUR_RGB = struct.unpack('BBB',P2_COLOUR.decode('hex'))
darkness = 10
if DARK_THEME:
    P1_AREA_COLOUR = (int(P1_COLOUR_RGB[0]/darkness),int(P1_COLOUR_RGB[1]/darkness),int(P1_COLOUR_RGB[2]/darkness))
    P2_AREA_COLOUR = (int(P2_COLOUR_RGB[0]/darkness),int(P2_COLOUR_RGB[1]/darkness),int(P2_COLOUR_RGB[2]/darkness))
else:
    P1_AREA_COLOUR = P1_COLOUR_RGB
    P2_AREA_COLOUR = P2_COLOUR_RGB
ACTIVE_AREA_COLOUR = (50,50,50)
TEXT_COLOUR = (100,200,100)
COURT_COLOUR = (200,200,200) # Lines and stuff
PAUSE_COLOUR = (160,160,160)
if Image:
    p1_score_colour = P1_COLOUR_RGB
    p2_score_colour = P2_COLOUR_RGB
else:
    p1_score_colour, p2_score_colour = COURT_COLOUR, COURT_COLOUR

###################

######### P H Y S I C S #########
universe = PyParticles.Environment((WIDTH, HEIGHT))
universe.colour = (30,30,30)
universe.addFunctions(['move','bounce','collide','drag'])
universe.mass_of_air = 0.04
universe.acceleration = (pi, 0.15)
universe.global_elasticity = False
MOTION_TRESHOLD = 0.05

# CLUTTER
def Quit():
    print ("Exiting cleanly...")
    return False
def spawnBall(p, s):
    spawn = True
    if s == "s":
        size = S_BALLSIZE
        mass = 20
        elasticity = 1
    elif s == "m":
        size = M_BALLSIZE
        mass = 40
        elasticity = 0.9
    else:
        size = L_BALLSIZE
        mass = 70
        elasticity = 0.8
    if p == 1:
        player = 1
        y = int(P_AREA_SIZE/2)
        if universe.p1_lives == 0:
            spawn = False
        else:
            universe.p1_lives -= 1
    elif p == 2:
        player = 2
        y = int(HEIGHT - P_AREA_SIZE/2)
        if universe.p2_lives == 0:
            spawn = False
        else:
            universe.p2_lives -= 1

    if spawn:
        universe.addParticles(mass=mass, player=player, hp=BALL_HITPOINTS, size=size, speed=0, x=WIDTH/2, y=y, elasticity=elasticity)

def restartRound():
    p1, p2 = False, False
    p1_b, p2_b = [], []
    universe.p1_lives, universe.p2_lives = LIVES, LIVES
    del universe.particles[:]
    if RANDOM_PLAYER_START:
        coinflip = random.randrange(1,3)
        if coinflip == 1:
            p1 = True
        else:
            p2 = True
    else:
        p1 = True
    if p1:
        spawnBall(1, random.choice(BALL_SIZES))
    else:
        spawnBall(2, random.choice(BALL_SIZES))
    for p in universe.particles:
        if p.player == 1:
            p1_b.append(p)
        if p.player == 2:
            p2_b.append(p)

    p1_s, p2_s, b_i_m = [], [], []

    return p1, p2, p1_b, p2_b, p1_s, p2_s, b_i_m

# Defining variables for later
pygame.display.set_caption(WINDOW_TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

p1_score, p2_score, p1_balls, p2_balls, balls_in_motion = [], [], [], [], []
BALL_SIZES = ["s", "m", "l"]
clock = pygame.time.Clock()
real_fps = FPS
delay, delay_max = 0, 5 # Another attempt to fix game end/round change bug when balls of equal mass collide
paused = True
debug_mode = False
selected_particle = None
running = True
p1_turn, p2_turn = False, False

######### MAIN LOOP #########
while running:

    # Android-specific:
    if android:
        if android.check_pause():
            android.wait_for_resume()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = Quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = universe.findParticle(mouseX, mouseY)
            if paused:
                # Button that starts new round
                if mouseX < NEWROUND_IMG.get_size()[0] and mouseY > HEIGHT/2-NEWROUND_IMG.get_size()[1]/2 and mouseY < HEIGHT/2+NEWROUND_IMG.get_size()[1]/2:
                    p1_turn, p2_turn, p1_balls, p2_balls, p1_score, p2_score, balls_in_motion = restartRound()
                    paused = False
                # Button that quits the game
                elif mouseX > WIDTH-QUIT_IMG.get_size()[0] and mouseY > HEIGHT/2-QUIT_IMG.get_size()[1]/2 and mouseY < HEIGHT/2+QUIT_IMG.get_size()[1]/2:
                    running = Quit()
                # Area that unpauses the game
                elif mouseY > (HEIGHT/5)*2 and mouseY < (HEIGHT/5)*3:
                    if p1_turn or p2_turn:
                        paused = False
            else:
                if mouseY > (HEIGHT/5)*2 and mouseY < (HEIGHT/5)*3:
                    paused = True
        elif event.type == pygame.MOUSEBUTTONUP:
            real_fps = FPS
            selected_particle = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                p1_turn, p2_turn, p1_balls, p2_balls, p1_score, p2_score, balls_in_motion = restartRound()
            elif event.key == pygame.K_d:
                debug_mode = (True, False)[debug_mode]
            elif event.key == pygame.K_t:
                p1_turn = (True, False)[p1_turn]
                p2_turn = (True, False)[p2_turn]
                paused = (True, False)[paused]
                selected_particle = None
            elif event.key == pygame.K_ESCAPE:
                running = Quit()
            elif event.key == pygame.K_1:
                spawnBall(1, random.choice(BALL_SIZES))
            elif event.key == pygame.K_2:
                spawnBall(2, random.choice(BALL_SIZES))

    # Checks if balls are inside players area, and allows for them to be moved.

    if not paused:
        if selected_particle:
            if selected_particle.y < P_AREA_SIZE and p1_turn:
                selected_particle.mouseMove(pygame.mouse.get_pos())
            elif selected_particle.y > HEIGHT-P_AREA_SIZE and p2_turn:
                selected_particle.mouseMove(pygame.mouse.get_pos())

    for p in balls_in_motion: # Fix to avoid balls "lingering" when dead
        if not p in universe.particles:
            balls_in_motion.remove(p)
            echo ("DOING IT")

    universe.update()

    screen.fill(universe.colour)

    # Drawing colors for areas where players score
    pygame.draw.rect(screen, P2_AREA_COLOUR, (0, P_AREA_SIZE, WIDTH, HEIGHT/2-P_AREA_SIZE), 0)
    pygame.draw.rect(screen, P1_AREA_COLOUR, (0, HEIGHT/2, WIDTH, HEIGHT/2-P_AREA_SIZE), 0)

    # Drawing the play area:
    pygame.draw.line(screen, COURT_COLOUR, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
    # These are the player areas on both sides:
    pygame.draw.line(screen, COURT_COLOUR, (0, HEIGHT-(P_AREA_SIZE+1)), (WIDTH, HEIGHT-(P_AREA_SIZE+1)))
    pygame.draw.line(screen, COURT_COLOUR, (0, P_AREA_SIZE+1), (WIDTH, P_AREA_SIZE+1))
    # Highlighting active player's area
    if p1_turn:
        pygame.draw.rect(screen, ACTIVE_AREA_COLOUR, (0, 0, WIDTH, P_AREA_SIZE), 0)
    elif p2_turn:
        pygame.draw.rect(screen, ACTIVE_AREA_COLOUR, (0, HEIGHT-(P_AREA_SIZE-1), WIDTH, P_AREA_SIZE), 0)

    # PARTICLE LOGIC AND DRAWING
    for p in universe.particles:
        if p.player == 1: # Set corresponding scaled ball image to the right size
            if p.size == L_BALLSIZE:
                scaled_ball_img = P1_L_IMG
            if p.size == M_BALLSIZE:
                scaled_ball_img = P1_M_IMG
            if p.size == S_BALLSIZE:
                scaled_ball_img = P1_S_IMG
        elif p.player == 2:
            if p.size == L_BALLSIZE:
                scaled_ball_img = P2_L_IMG
            if p.size == M_BALLSIZE:
                scaled_ball_img = P2_M_IMG
            if p.size == S_BALLSIZE:
                scaled_ball_img = P2_S_IMG

        # Determines the radius of the white circle, indicating damage
        scaled_by_hp = int(p.size-(p.size/(BALL_HITPOINTS/p.hitpoints)))
        scaled_dmg_ball_img = pygame.transform.scale(DMG_BALL_IMG, (scaled_by_hp*2, scaled_by_hp*2))

        ###############################
        # B A L L   R E N D E R I N G #
        ###############################
        screen.blit(scaled_ball_img,(int(p.x)-p.size, int(p.y)-p.size))
        screen.blit(scaled_dmg_ball_img, (int(p.x)-scaled_by_hp, int(p.y)-scaled_by_hp))
        ###############################

        # Score and turn
        if p.player == 1:
            if p.y < HEIGHT-P_AREA_SIZE and p.y > HEIGHT/2:    # Player 1
                if not p in p1_score:
                    p1_score.append(p)
                    p1_score_len = len(p1_score)
            else:
                if p in p1_score:
                    p1_score.remove(p)
                    p1_score_len = len(p1_score)

        if p.player == 2:
            if p.y > P_AREA_SIZE and p.y < HEIGHT/2:    # Player 2
                if not p in p2_score:
                    p2_score.append(p)
            else:
                if p in p2_score:
                    p2_score.remove(p)

        # CHECK FOR BALLS WITHIN PLAYER AREAS
        if p.y < P_AREA_SIZE:   # Player 1
            if not p in p1_balls:
                p1_balls.append(p) # Adds to the list of usable balls
        else:
            if p in p1_balls:
                p1_balls.remove(p) # Removes it if it's not in the area
        if p.y > HEIGHT-P_AREA_SIZE:   # Player 2
            if not p in p2_balls:
                p2_balls.append(p)
        else:
            if p in p2_balls:
                p2_balls.remove(p)


        # Removes the ball from all lists if it dies
        if p.hitpoints <= 0:
            if p in p1_score:
                p1_score.remove(p)
            if p in p1_balls:
                p1_balls.remove(p)
            if p in p2_score:
                p2_score.remove(p)
            if p in p2_balls:
                p2_balls.remove(p)
            if p in balls_in_motion:
                balls_in_motion.remove(p)
            p.speed = 0
            universe.particles.remove(p)

        # Changes turn and spawns ball if no balls are moving and none is available
        if not paused:
            if p1_turn:
                if not len(balls_in_motion) > 0 and len(p1_balls) == 0:
                    delay += 1
                    if delay == delay_max:
                        p1_turn = False
                        p2_turn = True
                        if universe.p2_lives > 0:
                            spawnBall(2, random.choice(BALL_SIZES))
                            p2_balls.append(p)
                        delay = 0
            elif p2_turn:
                if not len(balls_in_motion) > 0 and len(p2_balls) == 0:
                    delay += 1
                    if delay == delay_max:
                        p1_turn = True
                        p2_turn = False
                        if universe.p1_lives > 0:
                            spawnBall(1, random.choice(BALL_SIZES))
                            p1_balls.append(p)
                        delay = 0

        # Ends the round if no lives, no balls available and no ball is moving:
        if not len(balls_in_motion) > 0 and len(p1_balls) == 0 and len(p2_balls) == 0 and universe.p1_lives == 0 and universe.p2_lives == 0:
            delay += 1
            if delay == delay_max:# Waits 5 frames to restart
                p1_turn, p2_turn = False, False
                paused = True
                delay = 0

        # Make a list of balls that are in motion
        if p.speed > MOTION_TRESHOLD:
            if not p in balls_in_motion:
                balls_in_motion.append(p)
        else:
            if p in balls_in_motion:
                balls_in_motion.remove(p)

    try:
        p1_score_len
    except NameError:
        p1_score_len = 0
        p1_score_rotate = 0
        score_label1 = OSD_FONT.render("{0}".format(len(p1_score)), 1, p1_score_colour)
        score_label1 = pygame.transform.rotozoom(score_label1, 180, 1)

    clock.tick(real_fps)
    score_label2 = OSD_FONT.render("{1}".format(len(p1_score), len(p2_score)), 1, p2_score_colour)

    if not paused: # Shows score on both sides, the top one rotated
        if len(p1_score) != p1_score_rotate:
            score_label1 = OSD_FONT.render("{0}".format(len(p1_score)), 1, p1_score_colour)
            score_label1 = pygame.transform.rotozoom(score_label1, 180, 1) # rotate only on score update
            p1_score_rotate = len(p1_score)
        screen.blit(score_label1, (WIDTH-WIDTH/9, 0))
        screen.blit(score_label2, (20, int(HEIGHT-HEIGHT/15)))


    # PAUSE MENU, INCLUDING ANIMATION
    if paused:
        try: # Checks if it's the first time (aka when you run the app) and avoids the animation
            pause_rect1
        except NameError:
            pause_rect1 = HEIGHT/2
        try:
            pause_rect2
        except NameError:
            pause_rect2 = HEIGHT/2
        # Draws and animates the rectangles that makes up the pause screen background
        pygame.draw.rect(screen, PAUSE_COLOUR, (0, 0, WIDTH, HEIGHT-(HEIGHT-pause_rect1)), 0)
        if pause_rect1 < HEIGHT/2:
            pause_rect1 += int(HEIGHT/30)
        pygame.draw.rect(screen, PAUSE_COLOUR, (0, HEIGHT-pause_rect2, WIDTH, HEIGHT-(HEIGHT-pause_rect2)), 0)
        if pause_rect2 < HEIGHT/2:
            pause_rect2 += int(HEIGHT/30)

        # BUTTON TRIANGLES
        button_width = NEWROUND_IMG.get_size()[0]
        button_height = NEWROUND_IMG.get_size()[1]
        try:
            pause_anim
        except NameError:
            pause_anim = button_width
        try:
            quit_anim
        except NameError:
            quit_anim = button_width

        screen.blit(NEWROUND_IMG, ((0-button_width)+pause_anim, int(HEIGHT/2-button_height/2)))
        newround_label = FONT.render("NEW", 1, (220,220,220))
        screen.blit(newround_label, ((30-button_width)+pause_anim, HEIGHT/2-8))
        
        screen.blit(QUIT_IMG, (WIDTH-pause_anim, int(HEIGHT/2-button_height/2)))
        quit_label = FONT.render("QUIT", 1, (220,220,220))
        screen.blit(quit_label, ((WIDTH+button_width)-67-pause_anim, HEIGHT/2-8))
        
        if pause_anim < button_width:
            pause_anim += int(button_width/15)
        elif pause_anim > button_width:
            pause_anim = button_width



        # Shows the score in the middle of the screen instead
        score_label1_normal = OSD_FONT.render("{0}".format(len(p1_score)), 1, p1_score_colour)
        score_label1_shadow = OSD_FONT.render("{0}".format(len(p1_score)), 1, (60,60,60))
        score_label2_shadow = OSD_FONT.render("{0}".format(len(p2_score)), 1, (60,60,60))
        screen.blit(score_label1_shadow, ((WIDTH/2-15)+1, (HEIGHT/2-HEIGHT/15)+1))
        screen.blit(score_label1_normal, (WIDTH/2-15, HEIGHT/2-HEIGHT/15))
        screen.blit(score_label2_shadow, ((WIDTH/2-15)+1, (HEIGHT/2)+1))
        screen.blit(score_label2, (WIDTH/2-15, HEIGHT/2))

    elif not paused:
        if pause_rect1 > 0:
            pygame.draw.rect(screen, PAUSE_COLOUR, (0, 0, WIDTH, HEIGHT-(HEIGHT-pause_rect1)), 0)
            pause_rect1 -= int(HEIGHT/30)
        if pause_rect2 > 0:
            pygame.draw.rect(screen, PAUSE_COLOUR, (0, HEIGHT-pause_rect2, WIDTH, HEIGHT-(HEIGHT-pause_rect2)), 0)
            pause_rect2 -= int(HEIGHT/30)
    
        if pause_anim > 0:
            screen.blit(NEWROUND_IMG, ((0-button_width)+pause_anim, int(HEIGHT/2-(NEWROUND_IMG.get_size()[1]/2))))
            screen.blit(QUIT_IMG, (WIDTH-pause_anim, int(HEIGHT/2-button_height/2)))
            screen.blit(newround_label, ((30-button_width)+pause_anim, HEIGHT/2-8))
            screen.blit(quit_label, ((WIDTH+button_width)-67-pause_anim, HEIGHT/2-8))
            pause_anim -= int(WIDTH/30)

    # Renders the sweet ass splash img
    if pause_rect1 > 0:
            screen.blit(SPLASH_IMG, (WIDTH/2-128, (-368+pause_rect1)))

    if debug_mode: # DEBUG MODE PSD TEXT
        fps_label = FONT.render("FPS: %i" % round(clock.get_fps()), 1, TEXT_COLOUR)
        particles_on_screen = FONT.render("Particles: %i" % len(universe.particles), 1, TEXT_COLOUR)
        p1_balls_label = FONT.render("P1 balls: %i" % len(p1_balls), 1, TEXT_COLOUR)
        p2_balls_label = FONT.render("P2 balls: %i" % len(p2_balls), 1, TEXT_COLOUR)
        p1_lives_label = FONT.render("P1 lives: %i" % universe.p1_lives, 1, TEXT_COLOUR)
        p2_lives_label = FONT.render("P2 lives: %i" % universe.p2_lives, 1, TEXT_COLOUR)
        screen.blit(fps_label, (10, 10))
        screen.blit(particles_on_screen, (10, 35))
        screen.blit(p1_balls_label, (10, 60))
        screen.blit(p2_balls_label, (10, 85))
        screen.blit(p1_lives_label, (10, 110))
        screen.blit(p2_lives_label, (10, 135))

        # COLOR CHOOSER
        bar_h = 40
        bar_w = WIDTH/5
        bar_p1_x = WIDTH/2+WIDTH/5
        bar_p1_y = HEIGHT-HEIGHT/5
        bar_p2_x = WIDTH/2-(WIDTH/5)*2
        bar_p2_y = HEIGHT/5
        #P1
        r_p1_rect = (bar_p1_x, bar_p1_y, bar_w, bar_h)
        g_p1_rect = (bar_p1_x, bar_p1_y+bar_h, bar_w, bar_h)
        b_p1_rect = (bar_p1_x, bar_p1_y+bar_h*2, bar_w, bar_h)
        rgb_p1_rect = (bar_p1_x-bar_w/2, bar_p1_y, bar_w/2, bar_h*3)
        pygame.draw.rect(screen, (P1_COLOUR_RGB[0], 0, 0), r_p1_rect, 0)
        pygame.draw.rect(screen, (0, P1_COLOUR_RGB[1], 0), g_p1_rect, 0)
        pygame.draw.rect(screen, (0, 0, P1_COLOUR_RGB[2]), b_p1_rect, 0)
        pygame.draw.rect(screen, P1_COLOUR_RGB, rgb_p1_rect, 0)
        #P2
        r_p2_rect = (bar_p2_x, bar_p2_y-bar_h, bar_w, bar_h)
        g_p2_rect = (bar_p2_x, bar_p2_y-bar_h*2, bar_w, bar_h)
        b_p2_rect = (bar_p2_x, bar_p2_y-bar_h*3, bar_w, bar_h)
        rgb_p2_rect = (bar_p2_x+bar_w, bar_p2_y-bar_h*3, bar_w/2, bar_h*3)
        pygame.draw.rect(screen, (P2_COLOUR_RGB[0], 0, 0), r_p2_rect, 0)
        pygame.draw.rect(screen, (0, P2_COLOUR_RGB[1], 0), g_p2_rect, 0)
        pygame.draw.rect(screen, (0, 0, P2_COLOUR_RGB[2]), b_p2_rect, 0)
        pygame.draw.rect(screen, P2_COLOUR_RGB, rgb_p2_rect, 0)

    # LAST OF ALL, THE GRITTY NOISE FILTER WEEEE
    if NOISE:
        screen.blit(NOISE_IMG, (0, 0))

    pygame.display.flip()