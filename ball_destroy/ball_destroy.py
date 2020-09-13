############ Ball Destroy ############
########## How to win this game ##########
###### Player has to hit the ball with the given weapon
###### The ball is divided into two small part when it is hit by bullet 
###### Game ends if player destroyes all balls 
###### Game ends if the ball hit player
###### Game ends if player fails to destroy all balls in 99 seconds (time limit)
import pygame
import os

pygame.init()

### display setting ###
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

### game title ###
pygame.display.set_caption("Ball Destroy")

### fps ###
clock = pygame.time.Clock()

### image setting ###
current_path = os.path.dirname(__file__)  # change file location
# change current path to image file location
image_path = os.path.join(current_path, "images")

# 1. background
background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.jpg"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 2. character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_height - character_height
character_speed = 0.05
# position (moves to left and right only)
character_to_x_LEFT = 0
character_to_x_RIGHT = 0

# 3. weapon
weapon = pygame.image.load(os.path.join(image_path, "bullet.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapons = []
weapon_speed = 5

# 4. balls
ball_images = [
  pygame.image.load(os.path.join(image_path, "ballon1.png")),
  pygame.image.load(os.path.join(image_path, "ballon2.png")),
  pygame.image.load(os.path.join(image_path, "ballon3.png")),
  pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# speed
ball_speed_y = [-18, -15, -12, -9]

# balls
balls = []
# initial set up
balls.append({
  "pos_x": 50,
  "pos_y": 50,
  "img_index": 0,
  "to_x": 2,
  "to_y": -6,
  "initial_speed": ball_speed_y[0]
})

# if weapon hit the ball, they both disappear
remove_ball = -1
remove_weapon = -1

### Game font ###
game_font = pygame.font.Font(None, 30)
game_end_msg = pygame.font.Font(None, 60)
game_result_msg = "Game Over"

### Time Limit ###
total_time = 100
start_time = pygame.time.get_ticks()

####################
#### start game ####
####################
game_running = True
while game_running:
  dt = clock.tick(30)

  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          game_running = False

  ### key setting ###
  if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_LEFT:
      character_to_x_LEFT -= character_speed
    elif event.key == pygame.K_RIGHT:
      character_to_x_RIGHT += character_speed
    elif event.key == pygame.K_SPACE:
      weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
      weapon_y_pos = character_y_pos
      weapons.append([weapon_x_pos, weapon_y_pos])

  if event.type == pygame.KEYUP:
    if event.key == pygame.K_LEFT:
      character_to_x_LEFT = 0
    elif event.key == pygame.K_RIGHT:
      character_to_x_RIGHT = 0
  # character speed
  character_x_pos += (character_to_x_LEFT + character_to_x_RIGHT) * dt

  # prevent to go out of the game screen
  if character_x_pos < 0:
    character_x_pos = 0
  elif character_x_pos > screen_width - character_width:
    character_x_pos = screen_width - character_width

  ### weapon setting ###
  # weapon position
  weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
  # if weapon hit the top of screen
  weapons = [[w[0], w[1] - weapon_speed] for w in weapons if w[1] > 0]

  ### ball setting ###
  for ball_index, ball_val in enumerate(balls):
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_index = ball_val["img_index"]

    # check if the ball goes out of the screen
    ball_size = ball_images[ball_img_index].get_rect().size
    ball_width = ball_size[0]
    ball_height = ball_size[1]

    # horizontal
    if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
      ball_val["to_x"] = ball_val["to_x"] * -1

    # vertical
    if ball_pos_y > screen_height - stage_height - ball_height:
      ball_val["to_y"] = ball_val["initial_speed"]
    else:
      ball_val["to_y"] += 0.5

    ball_val["pos_x"] += ball_val["to_x"]
    ball_val["pos_y"] += ball_val["to_y"]

  ### Collision setting ###
  # 1. character and ball
  character_rect = character.get_rect()
  character_rect.left = character_x_pos
  character_rect.top = character_y_pos

  for ball_idx, ball_val in enumerate(balls):
    ball_pos_x = ball_val["pos_x"]
    ball_pos_y = ball_val["pos_y"]
    ball_img_index = ball_val["img_index"]
    ball_rect = ball_images[ball_img_index].get_rect()
    ball_rect.left = ball_pos_x
    ball_rect.top = ball_pos_y
    
    if character_rect.colliderect(ball_rect):
      game_running = False
      break

    # 2. weapon and ball
    for weapon_idx, weapon_val in enumerate(weapons):
      weapon_pos_x = weapon_val[0]
      weapon_pos_y = weapon_val[1]
      weapon_rect = weapon.get_rect()
      weapon_rect.left = weapon_pos_x
      weapon_rect.top = weapon_pos_y

      if weapon_rect.colliderect(ball_rect):
        remove_weapon = weapon_idx
        remove_ball = ball_idx  # current ball index
        
        # divide a ball into two small balls
        if ball_img_index < 3:  # index of ball pictures (4 different size)
          # ball size
          ball_width = ball_rect.size[0]
          ball_height = ball_rect.size[1]

          # small ball size
          small_ball_rect = ball_images[ball_img_index + 1].get_rect()
          small_ball_width = small_ball_rect.size[0]
          small_ball_height = small_ball_rect.size[1]

          # left ball
          balls.append({
            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
            "img_index": ball_img_index + 1,
            "to_x": -2,
            "to_y": -6,
            "initial_speed": ball_speed_y[ball_img_index + 1]
          })

          # right ball
          balls.append({
            "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
            "pos_y": ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
            "img_index": ball_img_index + 1,
            "to_x": 2,
            "to_y": -6,
            "initial_speed": ball_speed_y[ball_img_index + 1]
          })
        break

    else:
      continue

    break

  # remove ball and weapon if they are crashed
  if remove_weapon > -1:
    del weapons[remove_weapon]
    remove_weapon = -1

  if remove_ball > -1:
    del balls[remove_ball]
    remove_ball = -1

  # if player destroys all balls, game is over
  if len(balls) == 0:
    game_result_msg = "Mission Completed!"
    game_running = False

  ### display setting ###
  screen.blit(background, (0, 0))

  for weapon_x_pos, weapon_y_pos in weapons:
    screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

  for index, val in enumerate(balls):
    ball_pos_x = val["pos_x"]
    ball_pos_y = val["pos_y"]
    ball_index = val["img_index"]
    screen.blit(ball_images[ball_index], (ball_pos_x, ball_pos_y))

  screen.blit(stage, (0, screen_height - stage_height))
  screen.blit(character, (character_x_pos, character_y_pos))

  # display timer
  time_elapsed = (pygame.time.get_ticks() - start_time) / 1000
  timer = game_font.render("Time: {}".format(int(total_time - time_elapsed)), True, (255, 255, 255))
  timer_rect = timer.get_rect(center=(int(screen_width / 2), 20))
  screen.blit(timer, (timer_rect))

  if total_time - time_elapsed <= 0:
    game_result_msg = "Time Over"
    game_running = False

  pygame.display.update()

### Game end message ###
game_result = game_end_msg.render(game_result_msg, True, (255, 255, 0))
game_result_rect = game_result.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(game_result, game_result_rect)
pygame.display.update()

#### exit game ####
pygame.time.delay(5000)
pygame.quit()