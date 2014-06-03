import pygame
from pygame import transform
import PyParticles, PyButtons
import random, os
from math import pi
from timer import Timer
# Check for android module and does stuff
try:
    import android
except ImportError:
    android = None

# Android stuff
TIMEREVENT = pygame.USEREVENT

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
pygame.init()

######### S E T T I N G S #########
#(WIDTH, HEIGHT) = (800, 1280)
(WIDTH, HEIGHT) = (720, 1280)
#(WIDTH, HEIGHT) = (480, 800)
WINDOW_TITLE = "LOLOL, like OLO, but it's not OLO"
FPS = 60
NOISE = False # Noise filter, destroys performance
L_BALLSIZE = int(HEIGHT/30)
M_BALLSIZE = int(HEIGHT/50)
S_BALLSIZE = int(HEIGHT/90)
LIVES = 8
BALL_HITPOINTS = 50
RANDOM_PLAYER_START = True
P_AREA_SIZE = HEIGHT/6 # Size of the player area in relation to the height

######### F I L E   L O A D I N G #########
FONT_FILE = "./font.ttf"
OSD_FONT_FILE = "./osd_font.ttf"
FONT = pygame.font.Font(FONT_FILE, 15)
OSD_FONT = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/15))
basePath = os.path.dirname(__file__)
p1ballPath = os.path.join(basePath, "./img/red_ball.png") # P1 ball image
P1_BALL_IMG = pygame.image.load(p1ballPath)
p2ballPath = os.path.join(basePath, "./img/green_ball.png") # P2 ball image
P2_BALL_IMG = pygame.image.load(p2ballPath)
dmgballPath = os.path.join(basePath, "./img/damaged_ball.png") # The damage indicator
DMG_BALL_IMG = pygame.image.load(dmgballPath)
splashPath = os.path.join(basePath, "./android-presplash.jpg") # The sweet splash logo
SPLASH_IMG = pygame.image.load(splashPath)
if NOISE: # Aah, the things we do for grittyness
    noisePath = os.path.join(basePath, "./img/noise.png")
    noisescaledPath = os.path.join(basePath, "./img/noise_scaled.png")
    NOISE_IMG = pygame.image.load(noisePath)
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
P1_BALL_COLOUR = (220,40,40)
P2_BALL_COLOUR = (40,220,40)
P1_WEAK_COLOUR = (220,110,110)
P2_WEAK_COLOUR = (110,220,110)
P1_AREA_COLOUR = (40,30,30)
P2_AREA_COLOUR = (30,40,30)
ACTIVE_AREA_COLOUR = (50,50,50)
TEXT_COLOUR = (100,200,100)
COURT_COLOUR = (200,200,200) # Lines and stuff
PAUSE_COLOUR = (160,160,160)

######### P H Y S I C S #########
universe = PyParticles.Environment((WIDTH, HEIGHT))
universe.colour = (30,30,30)
universe.addFunctions(['move','bounce','collide','drag'])
universe.mass_of_air = 0.04
universe.acceleration = (pi, 0.15)
universe.global_elasticity = False
MOTION_TRESHOLD = 0.05

# CLUTTER
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
        colour = P1_BALL_COLOUR
        y = int(P_AREA_SIZE/2)
        if universe.p1_lives == 0:
            spawn = False
        else:
            universe.p1_lives -= 1
    elif p == 2:
        player = 2
        colour = P2_BALL_COLOUR
        y = int(HEIGHT - P_AREA_SIZE/2)
        if universe.p2_lives == 0:
            spawn = False
        else:
            universe.p2_lives -= 1

    if spawn:
        universe.addParticles(mass=mass, player=player, hp=BALL_HITPOINTS, size=size, speed=0, colour=colour, x=WIDTH/2, y=y, elasticity=elasticity)

def restartRound():
    p1, p2 = False, False
    if not len(universe.particles) == 0:
        del universe.particles[:]
    if RANDOM_PLAYER_START:
        coinflip = random.randrange(1,3)
        #print ("Player %i begins!" % coinflip)
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

    return p1, p2

# Defining variables for later
pygame.display.set_caption(WINDOW_TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

restart_button = PyButtons.Button()
quit_button = PyButtons.Button()
p1_score, p2_score, p1_balls, p2_balls, balls_in_motion = [], [], [], [], []
BALL_SIZES = ["s", "m", "l"]
clock = pygame.time.Clock()
real_fps = FPS
paused = True
debug_mode = False
selected_particle = None
running = True
p1_turn, p2_turn = restartRound()

######### MAIN LOOP #########
while running:

    # Android-specific:
    if android:
        if android.check_pause():
            android.wait_for_resume()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if not selected_particle == None:
            #    real_fps = FPS / 3
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = universe.findParticle(mouseX, mouseY)
            if paused:
                if restart_button.pressed(pygame.mouse.get_pos()):
                    del p1_balls[:]
                    del p2_balls[:]
                    p1_turn, p2_turn = restartRound()
                    del p1_score[:]
                    del p2_score[:]
                    del balls_in_motion[:]
                    universe.p1_lives, universe.p2_lives = LIVES, LIVES
                    paused = False
                elif quit_button.pressed(pygame.mouse.get_pos()):
                    running = False
                elif mouseY > (HEIGHT/5)*2 and mouseY < (HEIGHT/5)*3:
                    paused = False
            else:
                if mouseY > (HEIGHT/5)*2 and mouseY < (HEIGHT/5)*3:
                    paused = True
        elif event.type == pygame.MOUSEBUTTONUP:
            real_fps = FPS
            selected_particle = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                del p1_balls[:]
                del p2_balls[:]
                p1_turn, p2_turn = restartRound()
                del p1_score[:]
                del p2_score[:]
                del balls_in_motion[:]
                universe.p1_lives, universe.p2_lives = LIVES, LIVES
            elif event.key == pygame.K_d:
                debug_mode = (True, False)[debug_mode]
            elif event.key == pygame.K_t:
                p1_turn = (True, False)[p1_turn]
                p2_turn = (True, False)[p2_turn]
            elif event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
                selected_particle = None
            elif event.key == pygame.K_ESCAPE:
                running = False
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
        #if p.player == 1: ##### OLD OBSOLETE?
        #    p.colour = (P1_BALL_COLOUR[0], P1_BALL_COLOUR[1]+(BALL_HITPOINTS-p.hitpoints)*2, P1_BALL_COLOUR[2]+(BALL_HITPOINTS-p.hitpoints)*2)
        #elif p.player == 2:
        #    p.colour = (P2_BALL_COLOUR[0]+(BALL_HITPOINTS-p.hitpoints)*2, P2_BALL_COLOUR[1], P2_BALL_COLOUR[2]+(BALL_HITPOINTS-p.hitpoints)*2)

        ###### Draws the balls ######
        #pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, 0)
        if p.player == 1:
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

        scaled_by_hp = int(p.size-(p.size/(BALL_HITPOINTS/p.hitpoints)))
        scaled_dmg_ball_img = pygame.transform.scale(DMG_BALL_IMG, (scaled_by_hp*2, scaled_by_hp*2))

        screen.blit(scaled_ball_img,(int(p.x)-p.size, int(p.y)-p.size))
        screen.blit(scaled_dmg_ball_img, (int(p.x)-scaled_by_hp, int(p.y)-scaled_by_hp))
        #############################

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
                p1_balls.append(p)
        else:
            if p in p1_balls:
                p1_balls.remove(p)
        if p.y > HEIGHT-P_AREA_SIZE:   # Player 2
            if not p in p2_balls:
                p2_balls.append(p)
        else:
            if p in p2_balls:
                p2_balls.remove(p)


        # Removes the ball if it dies
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
                    p1_turn = False
                    p2_turn = True
                    if universe.p2_lives > 0:
                        spawnBall(2, random.choice(BALL_SIZES))
                        p2_balls.append(p)
            elif p2_turn:
                if not len(balls_in_motion) > 0 and len(p2_balls) == 0:
                    p1_turn = True
                    p2_turn = False
                    if universe.p1_lives > 0:
                        spawnBall(1, random.choice(BALL_SIZES))
                        p1_balls.append(p)

        # Ends the round if no lives, no balls available and no ball is moving:
        if not len(balls_in_motion) > 0 and len(p1_balls) == 0 and len(p2_balls) == 0 and universe.p1_lives == 0 and universe.p2_lives == 0:
            p1_turn, p2_turn = False, False
            paused = True

        # Make a list of balls that are in motion
        if p.speed > MOTION_TRESHOLD:
            if not p in balls_in_motion:
                balls_in_motion.append(p)
        else:
            if p in balls_in_motion:
                balls_in_motion.remove(p)

    clock.tick(real_fps)

    score_label1 = OSD_FONT.render("{0}".format(len(p1_score), len(p2_score)), 1, COURT_COLOUR)
    score_label2 = OSD_FONT.render("{1}".format(len(p1_score), len(p2_score)), 1, COURT_COLOUR)

    if not paused: # Shows score on both sides, the top one rotated
        try:
            p1_score_len
        except NameError:
            p1_score_len = 0
        if not len(p1_score) == p1_score_len:
            score_label1 = pygame.transform.rotozoom(score_label1, 180, 1) # rotate only on score update
            p1_score_len = len(p1_score)
        screen.blit(score_label1, (WIDTH-WIDTH/8, 0))
        screen.blit(score_label2, (20, int(HEIGHT-HEIGHT/15)))


    # PAUSE MENU, INCLUDING ANIMATION
    if paused:
        try:
            pause_rect1
        except NameError:
            pause_rect1 = 0
        try:
            pause_rect2
        except NameError:
            pause_rect2 = 0
        pygame.draw.rect(screen, PAUSE_COLOUR, (0, 0, WIDTH, HEIGHT-(HEIGHT-pause_rect1)), 0)
        if pause_rect1 < HEIGHT/2:
            pause_rect1 += int(HEIGHT/30)
        pygame.draw.rect(screen, PAUSE_COLOUR, (0, HEIGHT-pause_rect2, WIDTH, HEIGHT-(HEIGHT-pause_rect2)), 0)
        if pause_rect2 < HEIGHT/2:
            pause_rect2 += int(HEIGHT/30)

        restart_button.create_button(screen, (107,142,35), WIDTH/2-155, HEIGHT/2-30, 150, 60, 0, "New Round", (255,255,255))
        quit_button.create_button(screen, (142,35,35), WIDTH/2+5, HEIGHT/2-30, 150, 60, 0, "Quit LOLOL", (255,255,255))
        # Shows the score in the middle of the screen instead
        screen.blit(score_label1, (WIDTH/15, HEIGHT/2-HEIGHT/15))
        screen.blit(score_label2, (WIDTH/15, HEIGHT/2))

    elif not paused:
        if pause_rect1 > 0:
            pygame.draw.rect(screen, PAUSE_COLOUR, (0, 0, WIDTH, HEIGHT-(HEIGHT-pause_rect1)), 0)
            pause_rect1 -= int(HEIGHT/30)
        if pause_rect2 > 0:
            pygame.draw.rect(screen, PAUSE_COLOUR, (0, HEIGHT-pause_rect2, WIDTH, HEIGHT-(HEIGHT-pause_rect2)), 0)
            pause_rect2 -= int(HEIGHT/30)
    
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

    # LAST OF ALL, THE GRITTY NOISE FILTER WEEEE
    if NOISE:
        screen.blit(NOISE_IMG, (0, 0))

    pygame.display.flip()