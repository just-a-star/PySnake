import pygame
import sys
import random
from pygame.math import Vector2
from pygame.locals import *

# class Snake():


class FOOD:
    def __init__(self):
        self.randomize()

    def draw_food(self):
        # create a rectangle
        # fruit_rect = pygame.Rect(x,y,w,h)
        fruit_rect = pygame.Rect(int(
            self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        # pygame.draw.rect(surface,color,rectangle)
        pygame.draw.rect(screen, (255, 0, 0), fruit_rect)

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

    def draw_snake(self):
        # create a rect
        # draw the snake
        for block in self.body:
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            snake_rect = pygame.Rect(
                x_position, y_position, cell_size, cell_size)
            pygame.draw.rect(screen, (0, 255, 0), snake_rect)

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
        pygame.quit()
        sys.exit()


pygame.init()
cell_size = 25
cell_number = 20
clock = pygame.time.Clock()
#  this is display surface -> only 1, displayed by default, the canvas theentire game is drawn one
screen = pygame.display.set_mode(
    [cell_number * cell_size, cell_number * cell_size])
# screen.fill([255, 255, 255])


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

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
    screen.fill([255, 255, 255])
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
