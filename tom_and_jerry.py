# import pygame pip
import io
import pygame
import random
from urllib.request import urlopen

# pygame initialization (Essential)
pygame.init()

# image url
background_str = urlopen(
    "http://photos1.blogger.com/blogger/6884/1394/1600/TeeForTwo-3.jpg").read()
background_file = io.BytesIO(background_str)
jerry_str = urlopen(
    "https://www.pinclipart.com/picdir/big/567-5672582_jerry-mouse-tom-cat-tom-and-jerry-cartoon.png").read()
jerry_file = io.BytesIO(jerry_str)
tom_str = urlopen(
    "https://www.pinclipart.com/picdir/big/20-205769_tom-and-jerry-public-domain-tao-clip-art.png").read()
tom_file = io.BytesIO(tom_str)

# screen
# resolution
screen_width = 480   # row
screen_height = 640  # column
screen = pygame.display.set_mode((screen_width, screen_height))

# game title
pygame.display.set_caption("Tom and Jerry")

# set frame per second (fps) using BIF Clock()
clock = pygame.time.Clock()

# background
background = pygame.image.load(background_file)
background = pygame.transform.scale(background, (screen_width, screen_height))

# jerry speed
jerry_speed = 0.5

# create jerry
jerry = pygame.image.load(jerry_file)
jerry = pygame.transform.scale(jerry, (70, 70))
# movement
jerry_size = jerry.get_rect().size  # get size of character
jerry_width = jerry_size[0]
jerry_height = jerry_size[1]
# position
jerry_x_pos = (screen_width / 2) - (jerry_width / 2)
jerry_y_pos = screen_height - jerry_height

# create tom image
tom = pygame.image.load(tom_file)
tom = pygame.transform.scale(tom, (70, 70))
# movement
tom_size = tom.get_rect().size  # get size of poop
tom_width = tom_size[0]
tom_height = tom_size[1]
# position (randomly assigned)
tom_x_pos = random.randint(0, screen_width - tom_width)
tom_y_pos = 0  # down vertically
# speed
tom_speed = 7

# coordinate
to_x = 0

# font
display_score = pygame.font.Font(None, 40)
start_score = pygame.time.get_ticks()

# event loop
game_running = True
while game_running:
    dt = clock.tick(60)  # fps

    # events
    for event in pygame.event.get():
        # when game is ended
        if event.type == pygame.QUIT:
            game_running = False
        # when key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= jerry_speed
            if event.key == pygame.K_RIGHT:
                to_x += jerry_speed
        # when key is not pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0    # stop moving

    # Jerry's speed
    jerry_x_pos += to_x * dt

    # Jerry's position limit
    # horizontal
    if jerry_x_pos < 0:
        jerry_x_pos = 0
    elif jerry_x_pos > screen_width - jerry_width:
        jerry_x_pos = screen_width - jerry_width

    tom_y_pos += tom_speed

    if tom_y_pos > screen_height:
        tom_y_pos = 0
        tom_x_pos = random.randint(0, screen_width - tom_width)

    # Tom catches Jerry (game over)
    jerry_rect = jerry.get_rect()
    jerry_rect.left = jerry_x_pos
    jerry_rect.top = jerry_y_pos

    tom_rect = tom.get_rect()
    tom_rect.left = tom_x_pos
    tom_rect.top = tom_y_pos

    # background settings
    # screen.blit(image, location)
    screen.blit(background, (0, 0))

    # character image
    screen.blit(jerry, (jerry_x_pos, jerry_y_pos))

    # enemy image
    screen.blit(tom, (tom_x_pos, tom_y_pos))

    # font setting
    # score
    calculate_score = (pygame.time.get_ticks() - start_score) / 500
    score = display_score.render(
        "Score: " + str(int(calculate_score)), True, (255, 255, 255))
    score_size = score.get_rect().size
    score_width = score_size[0]

    screen.blit(score, (((screen_width - score_width) / 2), 10))

    if jerry_rect.colliderect(tom_rect):
        print("Game Over!\nYour Score is " + str(int(calculate_score)))
        game_running = False

    pygame.display.update()

# delay to exit game
pygame.time.delay(5000)

# exit pygame
pygame.quit()
