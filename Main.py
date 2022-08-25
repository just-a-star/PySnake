import pygame
import sys
import random
from pygame.math import Vector2
from pygame.locals import *
from pygame import mixer
# class Snake():


class FOOD:
    def __init__(self):
        self.randomize()

    def draw_food(self):
        # create a rectangle
        # fruit_rect = pygame.Rect(x,y,w,h)
        fruit_rect = pygame.Rect(int(
            self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(food_mouse, fruit_rect)
        # screen.blit(surface, rectangle(position))
        # pygame.draw.rect(surface,color,rectangle)
        # pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        print("muck")


class SNAKE:
    def __init__(self):
        self.body = [Vector2(3, 10), Vector2(2, 10), Vector2(1, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load(
            "Snake Game\Resources\graphics\snake_head_up_32.png")
        self.head_down = pygame.image.load(
            "Snake Game\Resources\graphics\snake_head_down_32.png")
        self.head_left = pygame.image.load(
            "Snake Game\Resources\graphics\snake_head_left_32.png")
        self.head_right = pygame.image.load(
            "Snake Game\Resources\graphics\snake_head_right_32.png")

        self.body_horizontal = pygame.image.load(
            "Snake Game\Resources\graphics\snake_body_horizontal_32.png")
        self.body_vertical = pygame.image.load(
            "Snake Game\Resources\graphics\snake_body_vertical__32.png")

        self.rotation_upleft = pygame.image.load(
            "Snake Game\Resources\graphics\snake_rotation_upleft_32.png")
        self.rotation_upright = pygame.image.load(
            "Snake Game\Resources\graphics\snake_rotation_upright_32.png")
        self.rotation_rightdown = pygame.image.load(
            "Snake Game\Resources\graphics\snake_rotation_rightdown_32.png")
        self.rotation_leftdown = pygame.image.load(
            "Snake Game\Resources\graphics\snake_rotation_leftdown_32.png")

        self.tail_up = pygame.image.load(
            "Snake Game\Resources\graphics\snake_tail_up_32.png")
        self.tail_down = pygame.image.load(
            "Snake Game\Resources\graphics\snake_tail_down_32.png")
        self.tail_left = pygame.image.load(
            "Snake Game\Resources\graphics\snake_tail_left_32.png")
        self.tail_right = pygame.image.load(
            "Snake Game\Resources\graphics\snake_tail_right_32.png")
        self.munch_sound = pygame.mixer.Sound(
            'Snake Game\Resources\crunch.wav')

    def draw_snake(self):

        # create a rect
        # draw the snake
        # - we need to rect for the position of the snake
        self.update_head_direction()
        self.update_tail_direction()

        for index, block in enumerate(self.body):
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)

            snake_rect = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
        # - we also need the direction of the head heading
        # why == 0 because index is always gonna be the first element which means the head
            if index == 0:
                # we need to check the direction of the head

                screen.blit(self.head, snake_rect)
            elif index == len(self.body)-1:
                # we need to check the direction of the tail
                screen.blit(self.tail, snake_rect)
            # last one we need to add the body of the snake
            # we need to know the previous and the next block of the snake

            else:
                self.update_body_direction()

                # ended up separated the code to make it easier to read
                # we need to check the direction of the body using index and and block
                # index is our current element and then we add 1 to it to get the next element(block)
                # then we need to subtract it to get the relative position of the previous element(block) aka relation
                # again its the same as the opposite
                # this will create a new vector that can point to the direction of the body

                # if the previous block and the next block have the same x coordinate then we need to draw a vertical body
                # same for the opposite direction

    def move_snake(self):

        if self.new_block == True:
          # add a block to the snake when the snake eats the food
          # the last element of the index stays the same but we add a new element(head) to the list
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            # we only want to copy the first two elements this gives 3,10 and 4,10
            # so the last element of the index(list) will be deleted
            body_copy = self.body[:-1]
            # why body_copy[0] because its the head
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
      # add a block to the snake
        self.new_block = True

    def play_munch_sound(self):
        self.munch_sound.play()

    def update_head_direction(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1, 0):
            self.head = self.head_left
        elif head_direction == Vector2(-1, 0):
            self.head = self.head_right
        elif head_direction == Vector2(0, 1):
            self.head = self.head_up
        elif head_direction == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_direction(self):
        tail_direction = self.body[-2] - self.body[-1]
        if tail_direction == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_direction == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_direction == Vector2(0, -1):
            self.tail = self.tail_up
        elif tail_direction == Vector2(0, 1):
            self.tail = self.tail_down

    def update_body_direction(self):
        for index, block in enumerate(self.body):

            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)

            snake_rect = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
            if index == 0:
                continue
            elif index == len(self.body)-1:
                continue
            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    self.update_corner_direction()

    # decided to repeat this because it will be easier to read
    def update_corner_direction(self):
        for index, block in enumerate(self.body):

            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)

            snake_rect = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
            if index == 0:
                continue
            elif index == len(self.body)-1:
                continue
            else:
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                if previous_block.x == next_block.x:
                    continue
                elif previous_block.y == next_block.y:
                    continue
                else:
                    # top left corner
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.rotation_upright, snake_rect)

                    # bottom left corner
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.rotation_rightdown, snake_rect)

                    # top right corner
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.rotation_upleft, snake_rect)

                    # bottom right corner
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.rotation_leftdown, snake_rect)
                        # screen.blit(self.rotation_upright, snake_rect)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_dead()

    def draw_elements(self):
        self.snake.draw_snake()
        self.food.draw_food()

    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize()
            # self.snake.add_block()
            self.snake.add_block()
            self.snake.play_munch_sound()

    def check_dead(self):
      # check if snake hits the screen
      # we use the snake.body[0] because its the head
      # why self.snake.body[0].x because its the x position of the head (this is 2d vector) and not the x position of the head (this is a number)
        # if not 0 <= self.snake.body[0].x < cell_number:
        #     self.game_over()
        #     # check if snake hits it self
        # elif not 0 <= self.snake.body[0].y < cell_number:
        #     self.game_over()
        #     # check if snake hits the wall
        # cleaner code
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # check if snake eat/collide itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        print("modar")
        pygame.quit()
        sys.exit()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 32
cell_number = 20
clock = pygame.time.Clock()
#  this is display surface -> only 1, displayed by default, the canvas theentire game is drawn one
screen = pygame.display.set_mode(
    [cell_number * cell_size, cell_number * cell_size])
# screen.fill([255, 255, 255])
food_mouse = pygame.image.load(
    'Snake Game\Resources\mouse_food_32.png').convert_alpha()

mixer.music.load('Snake Game\Resources\Kevin MacLeod - Pixelland.mp3')
mixer.music.play(-1)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 300)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # if main_game.snake.direction != Vector2(0, 1):
                # much simplier way to do this
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

            # pygame.draw.rect(screen, pygame.Color("red"), test_rect)
    screen.fill([0, 0, 0])
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
