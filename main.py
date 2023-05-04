import pygame
import random
import sys
from pygame.math import Vector2
import random


# CONSTANTS
CELL_SIZE = 40
CELL_NUMBER = 20
GREEN = (175,215,70)
RED = (200, 50, 50)
BLACK = (0, 0, 0)
BACKGROUND = (153,204,235)
WINDOW = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)
pygame.init()


class Fruit:
    def __init__(self):
        self.pos = Vector2()
        self.randomize()

    def draw_fruit(self):
        apple = pygame.image.load('graphics/apple.png').convert_alpha()
        fruit_rect = (int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        WINDOW.blit(apple, fruit_rect)

    # Place apple in a random place on the screen
    def randomize(self):
        x = random.randint(0, CELL_NUMBER - 1)
        y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(x, y)


class Snake():
    def __init__(self):
        # Start the snake with 3 squares moving towards the right.
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.score = -1

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(WINDOW, GREEN, block_rect)

    def move_snake(self):
        # If the snake has eaten an apple.
        if self.new_block:
            # Copy the snake and insert the head to the beginning of the list in the direction
            # The snake is moving
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
            self.score += 10
        # Else the snake hasn't eaten an apple, remove the last item in the list and insert the
        # head at the start in the direction the snake is moving.
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    # If the snake collides with an apple, set new_block to True.
    def add_block(self):
        self.new_block = True

    def add_score(self):
        self.score += 10


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.state = self.title_screen

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def game_over_check(self):
        # If the snake touches any of the walls, end the game
        if self.snake.body[0].y >= CELL_NUMBER or self.snake.body[0].y <= -1:
            self.state = self.title_screen
        if self.snake.body[0].x >= CELL_NUMBER or self.snake.body[0].x <= -1:
            self.state = self.title_screen
        # If the snake touches part of its own body, end the game.
        for pos in self.snake.body[1:]:
            if self.snake.body[0] == pos:
                self.state = self.title_screen

    # Checks if the fruit position is being place inside the snakes body
    def fruit_position(self):
        for block in self.snake.body:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def title_screen(self, event):
        WINDOW.fill(BACKGROUND)
        font = pygame.font.Font('fonts/SamuraiBlast-YznGj.ttf', 50)
        score = font.render(f'Your Score is {self.snake.score}', False, "Red")
        score_rect = score.get_rect(center=(CELL_NUMBER * CELL_SIZE // 2, CELL_NUMBER * CELL_SIZE // 4))
        play_game = pygame.image.load('graphics/play_1.png').convert_alpha()
        play_game_2 = pygame.image.load('graphics/play_2.png').convert_alpha()
        play_game_rect = play_game.get_rect(center=(CELL_NUMBER * CELL_SIZE // 2, CELL_NUMBER * CELL_SIZE // 2))
        if self.snake.score > 0:
            WINDOW.blit(score, score_rect)

        mouse_point = pygame.mouse.get_pos()
        play_game_rect.collidepoint(mouse_point)

        if play_game_rect.collidepoint(mouse_point):
            WINDOW.blit(play_game_2, play_game_rect)
        else:
            WINDOW.blit(play_game, play_game_rect)

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = pygame.mouse.get_pos()
            if play_game_rect.collidepoint(mouse_click):
                self.snake.score = 0
                self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
                self.snake.direction = Vector2(1,0)
                self.fruit.randomize()
                self.state = self.main_game

    def main_game(self, event):
        if event.type == SCREEN_UPDATE:
            self.snake.move_snake()
            self.check_collision()
            self.game_over_check()
            self.fruit_position()

            WINDOW.fill(BACKGROUND)
            self.draw_elements()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)


def main():
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.state(event)
        game.fruit_position()
        pygame.display.set_caption(f'Snake Score: {game.snake.score}!')
        pygame.display.update()
        CLOCK.tick(60)


if __name__ == '__main__':
    main()
