import pygame
from pygame import transform
import PyParticles
import random
import os
import struct
import sys
from time import sleep
from math import pi
# Check for android module and does stuff
try:
    import android
except ImportError:
    android = None
# Check for PIL, not working on android yet
try:
    import Image
    import PyColorize
except ImportError:
    try:
        from PIL import Image
        import PyColorize
    except ImportError:
        Image = None
        print ("PIL not found, using preloaded colored balls/court.")
draw = pygame.draw

# Android stuff
TIMEREVENT = pygame.USEREVENT

if android:
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
    print ("Android device detexted. DPI:{0}".format(android.get_dpi()))
pygame.init()

# S E T T I N G S #
# (WIDTH, HEIGHT) = (800, 1280)
(WIDTH, HEIGHT) = (600, 1024)
# (WIDTH, HEIGHT) = (480, 800)
if android:
    if android.get_dpi() > 240:
        (WIDTH, HEIGHT) = (720, 1280)
    else:
        (WIDTH, HEIGHT) = (600, 1024)
# (WIDTH, HEIGHT) = (480, 800)"""
print ("Window dimensions: {0}px/{1}px".format(WIDTH, HEIGHT))
WINDOW_TITLE = "LOLOL, like OLO, but it's not OLO"
FPS = 60
NOISE = False  # Noise filter, destroys performance
L_SIZE = int(HEIGHT/30)
M_SIZE = int(HEIGHT/45)
S_SIZE = int(HEIGHT/80)
HL_SIZE = 4  # Ball in score field highlight width
LIVES = 7
BALL_HITPOINTS = 50
RANDOM_PLAYER_START = True
P_SIZE = HEIGHT/6  # Size of the player area in relation to the height
P1_CLR = "963640"  # Light red
# P2_CLR = "ff9743"
P2_CLR = "94B362"  # Bleak green
# P2_CLR = "c39783"
DARK_THEME, darkness = True, 15
VIBRATE = True
SOUND = True

# F I L E   L O A D I N G #
SETTINGS_PATH = 'settings.db'
try:  # Checking if any files won't load
    FONT_FILE = "./font.ttf"
    OSD_FONT_FILE = "./osd_font.ttf"
    FONT = pygame.font.Font(FONT_FILE, 15)
    OSD_FONT = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/14))
    OSD_FONT_L = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/10))
    OSD_FONT_S = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/20))
    BTN_FONT = pygame.font.Font(OSD_FONT_FILE, int(HEIGHT/24))

    DMG_IMG = pygame.image.load('./img/damaged_ball.png')  # Dmg indicator
    SPLASH_IMG = pygame.image.load('./img/splash.png')  # The sweet splash logo
    NR_IMG = pygame.image.load('./img/new_round.png')
    QUIT_IMG = pygame.image.load('./img/quit.png')
    SOUND_IMG = pygame.image.load('./img/sound.png')
    VIBRATE_IMG = pygame.image.load('./img/vibrate.png')
    SOUND_OFF_IMG = pygame.image.load('./img/sound_off.png')
    VIBRATE_OFF_IMG = pygame.image.load('./img/vibrate_off.png')

    input_image_l = './img/new_ball_raw.png'
    input_image_m = './img/new_ball_raw_m.png'
    input_image_s = './img/new_ball_raw_s.png'
    if Image:
        # Colorizing P1
        result_image_path = './img/p1_ball_l.png'
        result = PyColorize.image_tint(input_image_l, '#%s' % P1_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P1_BALL_IMG_L = pygame.image.load(result_image_path)
        result_image_path = './img/p1_ball_m.png'
        result = PyColorize.image_tint(input_image_m, '#%s' % P1_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P1_BALL_IMG_M = pygame.image.load(result_image_path)
        result_image_path = './img/p1_ball_s.png'
        result = PyColorize.image_tint(input_image_s, '#%s' % P1_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P1_BALL_IMG_S = pygame.image.load(result_image_path)

        # Colorizing P2
        result_image_path = './img/p2_ball_l.png'
        result = PyColorize.image_tint(input_image_l, '#%s' % P2_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P2_BALL_IMG_L = pygame.image.load(result_image_path)
        result_image_path = './img/p2_ball_m.png'
        result = PyColorize.image_tint(input_image_m, '#%s' % P2_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P2_BALL_IMG_M = pygame.image.load(result_image_path)
        result_image_path = './img/p2_ball_s.png'
        result = PyColorize.image_tint(input_image_s, '#%s' % P2_CLR)
        if os.path.exists(result_image_path):  # delete previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name extension determines format
        P2_BALL_IMG_S = pygame.image.load(result_image_path)
        # HIGHLIGHT
        HIGHLIGHT_BALL = './img/damaged_ball.png'
        result_image_path = './img/p1_highlight.png'
        result = PyColorize.image_tint(HIGHLIGHT_BALL, '#%s' % P1_CLR)
        if os.path.exists(result_image_path):
            os.remove(result_image_path)
        result.save(result_image_path)
        P1_HL_IMG = pygame.image.load(result_image_path)
        result_image_path = './img/p2_highlight.png'
        result = PyColorize.image_tint(HIGHLIGHT_BALL, '#%s' % P2_CLR)
        if os.path.exists(result_image_path):
            os.remove(result_image_path)
        result.save(result_image_path)
        P2_HL_IMG = pygame.image.load(result_image_path)

    else:  # Loads default balls if PIL isn't available
        P1_BALL_IMG_L = pygame.image.load('./img/p1_ball_l.png')
        P1_BALL_IMG_M = pygame.image.load('./img/p1_ball_m.png')
        P1_BALL_IMG_S = pygame.image.load('./img/p1_ball_s.png')
        P2_BALL_IMG_L = pygame.image.load('./img/p2_ball_l.png')
        P2_BALL_IMG_M = pygame.image.load('./img/p2_ball_m.png')
        P2_BALL_IMG_S = pygame.image.load('./img/p2_ball_s.png')
        P1_HL_IMG = pygame.image.load('./img/p1_highlight.png')
        P2_HL_IMG = pygame.image.load('./img/p2_highlight.png')

    # For the animation at the end of the round, with balls falling
    ER_BALL_L_IMG = pygame.image.load(input_image_l)
    ER_BALL_M_IMG = pygame.image.load(input_image_m)
    ER_BALL_S_IMG = pygame.image.load(input_image_s)

    scale = transform.scale
    P1_L_IMG = scale(P1_BALL_IMG_L, (L_SIZE*2, L_SIZE*2))
    P1_M_IMG = scale(P1_BALL_IMG_M, (M_SIZE*2, M_SIZE*2))
    P1_S_IMG = scale(P1_BALL_IMG_S, (S_SIZE*2, S_SIZE*2))

    P2_L_IMG = scale(P2_BALL_IMG_L, (L_SIZE*2, L_SIZE*2))
    P2_M_IMG = scale(P2_BALL_IMG_M, (M_SIZE*2, M_SIZE*2))
    P2_S_IMG = scale(P2_BALL_IMG_S, (S_SIZE*2, S_SIZE*2))

    ER_L_IMG = scale(ER_BALL_L_IMG, (L_SIZE*2, L_SIZE*2))
    ER_M_IMG = scale(ER_BALL_M_IMG, (M_SIZE*2, M_SIZE*2))
    ER_S_IMG = scale(ER_BALL_S_IMG, (S_SIZE*2, S_SIZE*2))

    P1_HL_L_IMG = scale(P1_HL_IMG, (L_SIZE*2+HL_SIZE*2, L_SIZE*2+HL_SIZE*2))
    P1_HL_M_IMG = scale(P1_HL_IMG, (M_SIZE*2+HL_SIZE*2, M_SIZE*2+HL_SIZE*2))
    P1_HL_S_IMG = scale(P1_HL_IMG, (S_SIZE*2+HL_SIZE*2, S_SIZE*2+HL_SIZE*2))

    P2_HL_L_IMG = scale(P2_HL_IMG, (L_SIZE*2+HL_SIZE*2, L_SIZE*2+HL_SIZE*2))
    P2_HL_M_IMG = scale(P2_HL_IMG, (M_SIZE*2+HL_SIZE*2, M_SIZE*2+HL_SIZE*2))
    P2_HL_S_IMG = scale(P2_HL_IMG, (S_SIZE*2+HL_SIZE*2, S_SIZE*2+HL_SIZE*2))

    print ("Loaded all files successfully.")
except IOError:
    print ("There are missing files, exiting...")
    sys.exit()

# C O L O U R S #
p1_clr_rgb = struct.unpack('BBB', P1_CLR.decode('hex'))
p2_clr_rgb = struct.unpack('BBB', P2_CLR.decode('hex'))
BG_CLR = (40, 40, 40)
L_GREY = (220, 220, 220)
GREY = (150, 150, 150)
bg_r = int(BG_CLR[0])
bg_g = int(BG_CLR[1])
bg_b = int(BG_CLR[2])
if DARK_THEME:
    r1 = bg_r+p1_clr_rgb[0]/darkness
    g1 = bg_g+p1_clr_rgb[1]/darkness
    b1 = bg_b+p1_clr_rgb[2]/darkness
    r2 = bg_r+p2_clr_rgb[0]/darkness
    g2 = bg_g+p2_clr_rgb[1]/darkness
    b2 = bg_b+p2_clr_rgb[2]/darkness
    P1_AREA_CLR = (r1, g1, b1)
    P2_AREA_CLR = (r2, g2, b2)
else:
    P1_AREA_CLR = p1_clr_rgb
    P2_AREA_CLR = p2_clr_rgb
ACTIVE_CLR = (60, 60, 60)
TEXT_CLR = (100, 200, 100)
COURT_CLR = (160, 160, 160)  # Lines and stuff

PAUSE_CLR = (160, 160, 160)
p1_scr_clr = p1_clr_rgb
p2_scr_clr = p2_clr_rgb

###################

# P H Y S I C S #
universe = PyParticles.Environment((WIDTH, HEIGHT))
universe.colour = (BG_CLR)
# What attributes should the physics simulator have?
universe.addFunctions(['move', 'bounce', 'collide', 'drag'])
if HEIGHT > 1000:
    universe.mass_of_air = 0.04
else:
    universe.mass_of_air = 0.06
universe.acceleration = (pi, 0.15)
universe.global_elasticity = False
universe.p1_lives, universe.p2_lives = LIVES, LIVES
MOTION_TRESHOLD = 0.06

endroundballs = PyParticles.Environment((WIDTH, HEIGHT))
endroundballs.addFunctions(['move', 'bounce', 'collide', 'drag', 'accelerate'])
endroundballs.mass_of_air = 0.03
endroundballs.acceleration = universe.acceleration
endroundballs.global_elasticity = universe.global_elasticity


# CLUTTER
def Quit():
    # Write settings to file
    settings_file = open(SETTINGS_PATH, 'w')
    settings_file.write('SOUND = {0}\nVIBRATE = {1}'.format(SOUND, VIBRATE))
    settings_file.close()
    print ("Exiting cleanly...")
    return False


def spawnBall(p, s):
    spawn = True
    # Sets size on balls
    if s == "s":
        size = S_SIZE
        mass = 30
        elasticity = 1  # How bouncy they are
    elif s == "m":
        size = M_SIZE
        mass = 60
        elasticity = 0.9  # How bouncy they are
    else:
        size = L_SIZE
        mass = 120
        elasticity = 0.8  # How bouncy they are
    if p == 1:  # Checks if the player has any lives and if so, retracts one
        player = 1
        y = int(P_SIZE/2)
        if universe.p1_lives == 0:
            spawn = False
        else:
            universe.p1_lives -= 1
    elif p == 2:
        player = 2
        y = int(HEIGHT - P_SIZE/2)
        if universe.p2_lives == 0:
            spawn = False
        else:
            universe.p2_lives -= 1

    if spawn:
        universe.addParticles(
            mass=mass,
            player=player,
            hp=BALL_HITPOINTS,
            size=size, speed=0,
            x=WIDTH/2,
            y=y,
            elasticity=elasticity,
            vibrate=VIBRATE,
            sound=SOUND)


def scoreCalc(p, p1_s, p2_s):
    if p.player == 1:
        if p.y < HEIGHT-P_SIZE and p.y > HEIGHT/2:    # Player 1
            if p not in p1_s:
                p1_s.append(p)
        else:
            if p in p1_s:
                p1_s.remove(p)

    if p.player == 2:
        if p.y > P_SIZE and p.y < HEIGHT/2:    # Player 2
            if p not in p2_s:
                p2_s.append(p)
        else:
            if p in p2_s:
                p2_s.remove(p)
    return p1_s, p2_s


def drawLives(p1, p2):
    _offset = int(HEIGHT/100)
    _x_offset = _offset
    _y_offset = _offset
    _size = int(HEIGHT/150)
    for l in range(p1):
        draw.circle(screen, p1_clr_rgb, (_x_offset, _y_offset), _size)
        if _y_offset > P_SIZE-_offset*2:
            _x_offset += _size + _offset
            _y_offset = _offset
        else:
            _y_offset += _size + _offset
    _y_offset = _offset
    _x_offset = _offset
    for l in range(p2):
        draw.circle(screen, p2_clr_rgb, (WIDTH-_x_offset,
                                         HEIGHT-_y_offset), _size)
        if _y_offset > P_SIZE-_offset*2:
            _x_offset += _size + _offset
            _y_offset = _offset
        else:
            _y_offset += _size + _offset


def restartRound():
    p1, p2 = False, False
    p1_b, p2_b = [], []
    universe.p1_lives, universe.p2_lives = LIVES, LIVES
    del universe.particles[:]
    if RANDOM_PLAYER_START:
        coinflip = random.randrange(1, 3)
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

    print ("Starting new round!")

    return p1, p2, p1_b, p2_b, p1_s, p2_s, b_i_m


# Defining variables for later
pygame.display.set_caption(WINDOW_TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

if os.path.exists(SETTINGS_PATH):  # Loads settings from settings file
    import imp
    f = open(SETTINGS_PATH)
    settings = imp.load_source('settings', '', f)
    SOUND = settings.SOUND
    VIBRATE = settings.VIBRATE
    f.close()

PyParticles.SOUND, PyParticles.VIBRATE = SOUND, VIBRATE
p1_scr_lst, p2_scr_lst, p1_balls, p2_balls, in_motion = [], [], [], [], []
p1_scr, p2_scr = 0, 0
BALL_SIZES = ["s", "m", "l"]
clock = pygame.time.Clock()
real_fps = FPS
delay, delay_max = 0, 5  # Another attempt to fix game end/round change bug
paused = True            # when balls of equal mass collide
debug_mode = False
selected_particle = None
running = True
firstrun = True
roundstarted = False
p1_turn, p2_turn = False, False

# MAIN LOOP #
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
                if (mouseX < NR_IMG.get_size()[0] and
                        mouseY > HEIGHT/2-NR_IMG.get_size()[1]/2 and
                        mouseY < HEIGHT/2+NR_IMG.get_size()[1]/2):
                    (p1_turn, p2_turn, p1_balls, p2_balls,
                        p1_scr_lst, p2_scr_lst, in_motion) = restartRound()
                    p1_scr, p2_scr = 0, 0
                    firstrun = False
                    paused = False
                # Button that quits the game
                elif (mouseX > WIDTH-QUIT_IMG.get_size()[0] and
                        mouseY > HEIGHT/2-QUIT_IMG.get_size()[1]/2 and
                        mouseY < HEIGHT/2+QUIT_IMG.get_size()[1]/2):
                    running = Quit()
                # Buttons that toggles sound and vibration
                elif (mouseX > 10 and mouseX < 10 + SOUND_IMG.get_size()[0] and
                        mouseY > (HEIGHT-SOUND_IMG.get_size()[1])-10 and
                        mouseY < HEIGHT+10):
                    PyParticles.SOUND = (True, False)[PyParticles.SOUND]
                    SOUND = PyParticles.SOUND
                elif (mouseX > WIDTH-SOUND_IMG.get_size()[0]-10 and
                        mouseX < WIDTH-10 and
                        mouseY > (HEIGHT-SOUND_IMG.get_size()[1])-10 and
                        mouseY < HEIGHT+10):
                    PyParticles.VIBRATE = (True, False)[PyParticles.VIBRATE]
                    VIBRATE = PyParticles.VIBRATE
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
                (p1_turn, p2_turn, p1_balls, p2_balls,
                    p1_scr_lst, p2_scr_lst, in_motion) = restartRound()
                p1_scr, p2_scr = 0, 0
                firstrun = False
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
            if selected_particle.y < P_SIZE and p1_turn:
                selected_particle.mouseMove(pygame.mouse.get_pos())
            elif selected_particle.y > HEIGHT-P_SIZE and p2_turn:
                selected_particle.mouseMove(pygame.mouse.get_pos())

        for p in in_motion:  # Fix to avoid balls "lingering" when dead
            if p not in universe.particles:
                in_motion.remove(p)
                print ("DOING IT")

        universe.update()

    screen.fill(universe.colour)

    # Drawing colors for areas where players score
    draw.rect(screen, P2_AREA_CLR, (0, P_SIZE, WIDTH, HEIGHT/2-P_SIZE), 0)
    draw.rect(screen, P1_AREA_CLR, (0, HEIGHT/2, WIDTH, HEIGHT/2-P_SIZE), 0)

    # Drawing the play area:
    draw.line(screen, COURT_CLR, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
    # These are the player areas on both sides:
    draw.line(screen, COURT_CLR, (0, HEIGHT-(P_SIZE+1)),
              (WIDTH, HEIGHT-(P_SIZE+1)))
    draw.line(screen, COURT_CLR, (0, P_SIZE+1), (WIDTH, P_SIZE+1))
    # Highlighting active player's area
    if p1_turn:
        draw.rect(screen, ACTIVE_CLR, (0, 0, WIDTH, P_SIZE), 0)
    elif p2_turn:
        draw.rect(screen, ACTIVE_CLR, (0, HEIGHT-(P_SIZE-1), WIDTH, P_SIZE), 0)
    # Drawing circles that represents the players remaining lives.
    # Put it here to go behind the balls, as not to block them
    drawLives(universe.p1_lives, universe.p2_lives)

    # PARTICLE LOGIC AND DRAWING
    if not paused:
        for p in universe.particles:
            if p.player == 1:  # Set corresponding scaled ball image
                if p.size == L_SIZE:  # to the right size
                    scaled_ball_img = P1_L_IMG
                elif p.size == M_SIZE:
                    scaled_ball_img = P1_M_IMG
                elif p.size == S_SIZE:
                    scaled_ball_img = P1_S_IMG
            elif p.player == 2:
                if p.size == L_SIZE:
                    scaled_ball_img = P2_L_IMG
                elif p.size == M_SIZE:
                    scaled_ball_img = P2_M_IMG
                elif p.size == S_SIZE:
                    scaled_ball_img = P2_S_IMG

            # Determines the radius of the white circle, indicating damage
            if p.hitpoints > 1:  # Ball has to be alive in order to render it
                scaled_hp = int(p.size-(p.size/(BALL_HITPOINTS/p.hitpoints)))
                scaled_dmg_img = scale(DMG_IMG, (scaled_hp*2, scaled_hp*2))
                p_x = int(p.x)
                p_y = int(p.y)
                ###############################
                # B A L L   R E N D E R I N G #
                ###############################
                if p in p1_scr_lst or p in p2_scr_lst:
                    if p.player == 1:
                        if p.size == L_SIZE:
                            hl_img = P1_HL_L_IMG
                        elif p.size == M_SIZE:
                            hl_img = P1_HL_M_IMG
                        elif p.size == S_SIZE:
                            hl_img = P1_HL_S_IMG
                    if p.player == 2:
                        if p.size == L_SIZE:
                            hl_img = P2_HL_L_IMG
                        elif p.size == M_SIZE:
                            hl_img = P2_HL_M_IMG
                        elif p.size == S_SIZE:
                            hl_img = P2_HL_S_IMG
                    screen.blit(hl_img, ((p_x-p.size)-HL_SIZE,
                                (p_y-p.size)-HL_SIZE))
                screen.blit(scaled_ball_img, (p_x-p.size, p_y-p.size))
                screen.blit(scaled_dmg_img, (p_x-scaled_hp, p_y-scaled_hp))
                ###############################

            # Score and turn
            p1_scr_lst, p2_scr_lst = scoreCalc(p, p1_scr_lst, p2_scr_lst)
            p1_scr = len(p1_scr_lst)
            p2_scr = len(p2_scr_lst)

            # CHECK FOR BALLS WITHIN PLAYER AREAS
            if p.y < P_SIZE:   # Player 1
                if p not in p1_balls:
                    p1_balls.append(p)  # Adds to the list of usable balls
            else:
                if p in p1_balls:
                    p1_balls.remove(p)  # Removes it if it's not in the area
            if p.y > HEIGHT-P_SIZE:   # Player 2
                if p not in p2_balls:
                    p2_balls.append(p)
            else:
                if p in p2_balls:
                    p2_balls.remove(p)

            # Removes the ball from all lists if it dies
            if p.hitpoints <= 0:
                if p in p1_scr_lst:
                    p1_scr_lst.remove(p)
                if p in p1_balls:
                    p1_balls.remove(p)
                if p in p2_scr_lst:
                    p2_scr_lst.remove(p)
                if p in p2_balls:
                    p2_balls.remove(p)
                if p in in_motion:
                    in_motion.remove(p)
                p.speed = 0
                universe.particles.remove(p)

            # Changes turn and spawns ball if no balls are moving and
            if not paused:  # none is available
                if p1_turn:
                    if not len(in_motion) > 0 and len(p1_balls) == 0:
                        delay += 1
                        if delay == delay_max:  # End P1 turn, spawns P2 ball
                            p1_turn = False
                            p2_turn = True
                            if universe.p2_lives > 0:
                                spawnBall(2, random.choice(BALL_SIZES))
                                p2_balls.append(p)
                            delay = 0
                elif p2_turn:
                    if not len(in_motion) > 0 and len(p2_balls) == 0:
                        delay += 1
                        if delay == delay_max:  # End P2 turn, spawns P1 ball
                            p1_turn = True
                            p2_turn = False
                            if universe.p1_lives > 0:
                                spawnBall(1, random.choice(BALL_SIZES))
                                p1_balls.append(p)
                            delay = 0

            # Ends the round if no lives, no balls available, no balls moving:
            if (not len(in_motion) > 0 and
                    len(p1_balls) == 0 and
                    len(p2_balls) == 0 and
                    universe.p1_lives == 0 and
                    universe.p2_lives == 0):
                delay += 1
                if delay == delay_max:  # Waits 5 frames to end
                    p1_turn, p2_turn = False, False
                    sleep(0.5)
                    paused = True
                    delay = 0
                    del endroundballs.particles[:]
                    for p in universe.particles:  # Adds a copy of all
                        endroundballs.addParticles(mass=100,  # remaining
                                                   player=p.player,  # balls to
                                                   hp=BALL_HITPOINTS,
                                                   size=p.size,  # another set
                                                   speed=0,  # of particles
                                                   x=p.x,
                                                   y=p.y,
                                                   elasticity=p.elasticity,
                                                   vibrate=False,
                                                   sound=False)
                    if p1_scr > p2_scr:
                        endroundballs.acceleration = (pi, -0.20)
                    elif p2_scr > p1_scr:
                        endroundballs.acceleration = (pi, 0.20)
                    else:
                        endroundballs.acceleration = (pi, 0)
                    if p1_scr > p2_scr:
                        print ("Top wins!")
                    elif p1_scr < p2_scr:
                        print ("Bottom wins!")
                    else:
                        print ("It's a tie!")

            # Make a list of balls that are in motion
            if p.speed > MOTION_TRESHOLD:
                if p not in in_motion:
                    in_motion.append(p)
            else:
                if p in in_motion:
                    in_motion.remove(p)

        for p in p1_balls:
            if p not in universe.particles:
                p1_balls.remove(p)
        for p in p2_balls:
            if p not in universe.particles:
                p2_balls.remove(p)

        try:
            p1_scr_rotate
        except NameError:
            p1_scr_rotate = 0
            scr_lbl1 = OSD_FONT.render("{0}".format(p1_scr), 1, p1_scr_clr)
            scr_lbl1 = transform.rotozoom(scr_lbl1, 180, 1)

        if not paused:  # Shows score on both sides, the top one rotated
            if p1_scr != p1_scr_rotate:  # rotate only on score update
                scr_lbl1 = OSD_FONT.render("{0}".format(p1_scr), 1, p1_scr_clr)
                scr_lbl1 = transform.rotozoom(scr_lbl1, 180, 1)
                p1_scr_rotate = p1_scr
            scr_lbl2 = OSD_FONT.render("{0}".format(p2_scr), 1, p2_scr_clr)
            screen.blit(scr_lbl1, (WIDTH-WIDTH/9, 0))
            screen.blit(scr_lbl2, (20, int(HEIGHT-HEIGHT/15)))

    clock.tick(real_fps)

    # PAUSE MENU, INCLUDING ANIMATION
    if paused:
        try:  # Checks if it's the first time and avoids the animation
            rect1
        except NameError:
            rect1 = HEIGHT/2
        try:
            rect2
        except NameError:
            rect2 = HEIGHT/2
        # Draws and animates the rectangles that makes up the
        # pause screen background
        draw.rect(screen, PAUSE_CLR, (0, 0, WIDTH, HEIGHT-(HEIGHT-rect1)), 0)
        if rect1 < HEIGHT/2:
            rect1 += int(HEIGHT/30)
        draw.rect(screen, PAUSE_CLR, (0, HEIGHT-rect2, WIDTH,
                                      HEIGHT-(HEIGHT-rect2)), 0)
        if rect2 < HEIGHT/2:
            rect2 += int(HEIGHT/30)

        if not p1_turn and not p2_turn:  # Animates the balls that show
            for p in endroundballs.particles:  # up when round ends
                p.sound = False
                p.vibrate = False
                p.hitpoints -= 0.1
                if p.hitpoints <= 1:
                    endroundballs.particles.remove(p)

                if p.size == L_SIZE:
                    scaled_er_img = ER_L_IMG
                if p.size == M_SIZE:
                    scaled_er_img = ER_M_IMG
                if p.size == S_SIZE:
                    scaled_er_img = ER_S_IMG

                screen.blit(scaled_er_img, (int(p.x)-p.size, int(p.y)-p.size))
            endroundballs.update()

        # SOUND AND VIBRATE TOGGLE
        if SOUND:
            cur_snd_img = SOUND_IMG
        else:
            cur_snd_img = SOUND_OFF_IMG
        if VIBRATE:
            cur_vib_img = VIBRATE_IMG
        else:
            cur_vib_img = VIBRATE_OFF_IMG
        screen.blit(cur_snd_img, (10, HEIGHT-cur_snd_img.get_size()[1]-10))
        screen.blit(cur_vib_img, (WIDTH-(cur_vib_img.get_size()[0]+10),
                                  HEIGHT-cur_vib_img.get_size()[1]-10))

        # BUTTON TRIANGLES
        btn_width = NR_IMG.get_size()[0]
        anim_max = btn_width
        btn_height = NR_IMG.get_size()[1]
        try:
            anim
        except NameError:
            anim = anim_max
        try:
            quit_anim
        except NameError:
            quit_anim = anim_max

        screen.blit(NR_IMG, ((0-btn_width)+anim, int(HEIGHT/2-btn_height/2)))
        nr_lbl = BTN_FONT.render("NEW", 1, L_GREY)
        nr_lbl_shadow = BTN_FONT.render("NEW", 1, (30, 30, 30))
        nr_x = ((btn_width/2-nr_lbl.get_width()/2)-btn_width)+anim
        nr_y = HEIGHT/2-nr_lbl.get_height()/2
        screen.blit(nr_lbl_shadow, (nr_x+1, nr_y+1))
        screen.blit(nr_lbl, (nr_x, nr_y))

        screen.blit(QUIT_IMG, (WIDTH-anim, int(HEIGHT/2-btn_height/2)))
        quit_lbl = BTN_FONT.render("QUIT", 1, L_GREY)
        quit_lbl_shadow = BTN_FONT.render("QUIT", 1, (30, 30, 30))
        quit_x = (WIDTH+btn_width)-(btn_width/2+quit_lbl.get_width()/2)-anim
        quit_y = (HEIGHT/2-quit_lbl.get_height()/2)
        screen.blit(quit_lbl_shadow, (quit_x+1, quit_y+1))
        screen.blit(quit_lbl, (quit_x, quit_y))

        if anim < anim_max:
            anim += int(anim_max/15)
            if anim > anim_max:
                anim = anim_max
        elif anim > anim_max:
            anim = anim_max

        # Shows the score in the middle of the screen instead
        if not firstrun:
            scr_fnt1, scr_fnt2 = OSD_FONT, OSD_FONT
            if p1_scr == p2_scr:  # These are for enlarging the score of
                scr_fnt1 = OSD_FONT  # the leader/winner
                scr_fnt2 = OSD_FONT
                pol_wt_t = int((HEIGHT/10)*(float(anim)/float(anim_max)))
                pol_wt_b = int((HEIGHT/10)*(float(anim)/float(anim_max)))
            elif p1_scr > p2_scr:
                scr_fnt1 = OSD_FONT_L
                scr_fnt2 = OSD_FONT_S
                pol_wt_b = int((HEIGHT/12)*(float(anim)/float(anim_max)))
                pol_wt_t = int((HEIGHT/8)*(float(anim)/float(anim_max)))
            else:
                scr_fnt1 = OSD_FONT_S
                scr_fnt2 = OSD_FONT_L
                pol_wt_t = int((HEIGHT/12)*(float(anim)/float(anim_max)))
                pol_wt_b = int((HEIGHT/8)*(float(anim)/float(anim_max)))
            scr_lbl1_normal = scr_fnt1.render("{0}".format(p1_scr),
                                              1, p1_scr_clr)
            scr_lbl2_normal = scr_fnt2.render("{0}".format(p2_scr),
                                              1, p2_scr_clr)
            scr_lbl1_shadow = scr_fnt1.render("{0}".format(p1_scr),
                                              1, (100, 100, 100))
            scr_lbl2_shadow = scr_fnt2.render("{0}".format(p2_scr),
                                              1, (100, 100, 100))
            scr_lbl1_highlight = scr_fnt1.render("{0}".format(p1_scr),
                                                 1, (200, 200, 200))
            scr_lbl2_highlight = scr_fnt2.render("{0}".format(p2_scr),
                                                 1, (200, 200, 200))
            score1_width = scr_lbl1_normal.get_width()  # For centering
            score1_height = scr_lbl1_normal.get_height()
            score2_width = scr_lbl2_normal.get_width()

            pol_l = (anim, HEIGHT/2)
            pol_t = (WIDTH/2, HEIGHT/2-pol_wt_t)
            pol_r = (WIDTH-anim, HEIGHT/2)
            pol_b = (WIDTH/2, HEIGHT/2+pol_wt_b)
            pol_brdr = ()

            draw.polygon(screen, GREY, (pol_l, pol_t, pol_r, pol_b), 0)
            draw.polygon(screen, L_GREY, (pol_l, pol_t, pol_r, pol_b), 2)

            if anim >= btn_width:
                draw.line(screen, L_GREY, (int(WIDTH/2-15), int(HEIGHT/2)),
                          (int(WIDTH/2+15), int(HEIGHT/2)), 2)
                scr1_x = WIDTH/2-score1_width/2
                scr1_y = HEIGHT/2-score1_height
                scr2_x = WIDTH/2-score2_width/2
                screen.blit(scr_lbl1_highlight, (scr1_x-1, scr1_y-1))
                screen.blit(scr_lbl1_shadow, (scr1_x+1, scr1_y+1))
                screen.blit(scr_lbl1_normal, (scr1_x, scr1_y))
                screen.blit(scr_lbl2_highlight, (scr2_x-1, (HEIGHT/2)-1))
                screen.blit(scr_lbl2_shadow, (scr2_x+1, (HEIGHT/2)+1))
                screen.blit(scr_lbl2_normal, (scr2_x, HEIGHT/2))

            roundstarted = True

    elif not paused:
        if rect1 > 0:
            draw.rect(screen, PAUSE_CLR,
                      (0, 0, WIDTH, HEIGHT-(HEIGHT-rect1)), 0)
            rect1 -= int(HEIGHT/30)
        if rect2 > 0:
            draw.rect(screen, PAUSE_CLR,
                      (0, HEIGHT-rect2, WIDTH, HEIGHT-(HEIGHT-rect2)), 0)
            rect2 -= int(HEIGHT/30)

        if anim > 0:
            screen.blit(NR_IMG, ((0-btn_width)+anim,
                        int(HEIGHT/2-(NR_IMG.get_size()[1]/2))))
            screen.blit(QUIT_IMG, (WIDTH-anim, int(HEIGHT/2-btn_height/2)))
            nr_x = ((btn_width/2-nr_lbl.get_width()/2)-btn_width)+anim
            nr_y = HEIGHT/2-nr_lbl.get_height()/2
            screen.blit(nr_lbl_shadow, (nr_x+1, nr_y+1))
            screen.blit(nr_lbl, (nr_x, nr_y))
            q_x = (WIDTH+btn_width)-(btn_width/2+quit_lbl.get_width()/2)-anim
            q_y = HEIGHT/2-quit_lbl.get_height()/2
            screen.blit(quit_lbl_shadow, (q_x+1, q_y+1))
            screen.blit(quit_lbl, (q_x, q_y))

            if not firstrun and roundstarted:  # These are for enlarging the
                if p1_scr == p2_scr:  # score of the leader/winner
                    pol_wt_t = int((HEIGHT/10)*(float(anim)/float(anim_max)))
                    pol_wt_b = int((HEIGHT/10)*(float(anim)/float(anim_max)))
                elif p1_scr > p2_scr:
                    pol_wt_b = int((HEIGHT/12)*(float(anim)/float(anim_max)))
                    pol_wt_t = int((HEIGHT/8)*(float(anim)/float(anim_max)))
                else:
                    pol_wt_t = int((HEIGHT/12)*(float(anim)/float(anim_max)))
                    pol_wt_b = int((HEIGHT/8)*(float(anim)/float(anim_max)))
                pol_l = (anim, HEIGHT/2)
                pol_t = (WIDTH/2, HEIGHT/2-pol_wt_t)
                pol_r = (WIDTH-anim, HEIGHT/2)
                pol_b = (WIDTH/2, HEIGHT/2+pol_wt_b)
                draw.polygon(screen, GREY, (pol_l, pol_t, pol_r, pol_b), 0)
                draw.polygon(screen, L_GREY, (pol_l, pol_t, pol_r, pol_b), 2)

            anim -= int(WIDTH/30)

    # Renders the sweet ass splash img
    if rect1 > 0:
            screen.blit(SPLASH_IMG, (WIDTH/2-128, (-(HEIGHT/2.2)+rect1)))

    if debug_mode:  # DEBUG MODE PSD TEXT
        fps_lbl = FONT.render("FPS: %i" % round(clock.get_fps()), 1, TEXT_CLR)
        on_scr = FONT.render("BALL: %i" % len(universe.particles), 1, TEXT_CLR)
        p1_b_lbl = FONT.render("P1 balls: %i" % len(p1_balls), 1, TEXT_CLR)
        p2_b_lbl = FONT.render("P2 balls: %i" % len(p2_balls), 1, TEXT_CLR)
        p1_l_lbl = FONT.render("P1 lives: %i" % universe.p1_lives, 1, TEXT_CLR)
        p2_l_lbl = FONT.render("P2 lives: %i" % universe.p2_lives, 1, TEXT_CLR)
        bim_lbl = FONT.render("In motion: %i" % len(in_motion), 1, TEXT_CLR)
        screen.blit(fps_lbl, (10, 10))
        screen.blit(on_scr, (10, 35))
        screen.blit(p1_b_lbl, (10, 60))
        screen.blit(p2_b_lbl, (10, 85))
        screen.blit(p1_l_lbl, (10, 110))
        screen.blit(p2_l_lbl, (10, 135))
        screen.blit(bim_lbl, (10, 160))

        # COLOR CHOOSER
        """bar_h = 40
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
        draw.rect(screen, (p1_clr_rgb[0], 0, 0), r_p1_rect, 0)
        draw.rect(screen, (0, p1_clr_rgb[1], 0), g_p1_rect, 0)
        draw.rect(screen, (0, 0, p1_clr_rgb[2]), b_p1_rect, 0)
        draw.rect(screen, p1_clr_rgb, rgb_p1_rect, 0)
        #P2
        r_p2_rect = (bar_p2_x, bar_p2_y-bar_h, bar_w, bar_h)
        g_p2_rect = (bar_p2_x, bar_p2_y-bar_h*2, bar_w, bar_h)
        b_p2_rect = (bar_p2_x, bar_p2_y-bar_h*3, bar_w, bar_h)
        rgb_p2_rect = (bar_p2_x+bar_w, bar_p2_y-bar_h*3, bar_w/2, bar_h*3)
        draw.rect(screen, (p2_clr_rgb[0], 0, 0), r_p2_rect, 0)
        draw.rect(screen, (0, p2_clr_rgb[1], 0), g_p2_rect, 0)
        draw.rect(screen, (0, 0, p2_clr_rgb[2]), b_p2_rect, 0)
        draw.rect(screen, p2_clr_rgb, rgb_p2_rect, 0)"""

    # LAST OF ALL, THE GRITTY NOISE FILTER WEEEE
    if NOISE:
        screen.blit(NOISE_IMG, (0, 0))

    pygame.display.flip()
