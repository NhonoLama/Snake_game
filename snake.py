import pygame
from pygame.locals import *
import time
import random

SIZE = 48


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1500, 750))
        self.snake = Snake(self.surface, 1)
        self.frog = Food(self.surface)
        self.snake.draw_snake()
        self.frog.draw_frog()

    def collided(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.move_dir()
        self.frog.draw_frog()
        self.display_score()
        pygame.display.flip()

        # collides with frog
        if self.collided(self.snake.x[0], self.snake.y[0], self.frog.x, self.frog.y):
            self.snake.incre_snake()
            self.frog.move_frog()

        # collides with itself
        for i in range(3, self.snake.length):
            if self.collided(
                self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]
            ):
                raise "game over"

    def display_score(self):
        font = pygame.font.SysFont("arial", 25)
        score = font.render(f"SCORE: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 00))

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                if event.type == QUIT:
                    running = False

            try:
                self.play()
            except Exception as e:
                self.game_over()
            time.sleep(0.2)


class Food:
    def __init__(self, screen):
        self.screen = screen
        self.food = pygame.image.load("resources/frog.png").convert()
        self.x = SIZE * 2
        self.y = SIZE * 2

    def draw_frog(self):
        self.screen.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def move_frog(self):
        self.x = random.randint(0, 25) * SIZE
        self.y = random.randint(0, 13) * SIZE


class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.screen = screen
        self.snake = pygame.image.load("resources/snake.png").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def draw_snake(self):
        self.screen.fill((0, 0, 0))  # clearing the screen everytime
        for i in range(self.length):
            self.screen.blit(self.snake, (self.x[i], self.y[i]))
        pygame.display.flip()

    def incre_snake(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_dir(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw_snake()


if __name__ == "__main__":
    game = Game()
    game.run()
