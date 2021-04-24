import pygame
import sys
import math
import time
import random

SIZE = 40


def check_collision(x1, y1, x2, y2):
    if x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE:
        return True
    return False


def update_score(score, hi_score):
    if score > hi_score:
        hi_score = score
    return hi_score


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert_alpha()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.WHITE = (255, 255, 255)
        self.MAGENTA = (142, 63, 255)
        self.direction = 'down'

    def increase_length(self):
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

    def draw(self):
        # self.parent_screen.fill(self.MAGENTA)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE

        self.draw()


class Assets:
    def __init__(self):
        self.background = pygame.image.load("resources/background.png")
        self.game_over = pygame.image.load("resources/game_over.png")
        self.game_over_rect = self.game_over.get_rect(center=(500, 400))


class Game:
    def __init__(self):
        pygame.init()

        # Game Constants
        self.MONITOR = pygame.display.Info()
        self.SCREEN_DIMENSIONS = (math.ceil(self.MONITOR.current_w * 0.5206), math.ceil(self.MONITOR.current_h * 0.74))
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.DUMMY_WINDOW = pygame.Surface((1000, 800))
        self.WIDTH, HEIGHT = self.SCREEN_DIMENSIONS
        self.WINDOW_WIDTH = self.WINDOW.get_width()
        self.WINDOW_HEIGHT = self.WINDOW.get_height()
        self.font = pygame.font.SysFont('arial', 30)
        self.WHITE = (255, 255, 255)

        # Game Variables
        self.running = True
        self.game_active = True
        self.high_score = 0

        # Class Imports
        self.snake = Snake(self.DUMMY_WINDOW, 1)
        self.apple = Apple(self.DUMMY_WINDOW)
        self.assets = Assets()

        # Onscreen Drawings
        self.snake.draw()
        self.apple.draw()

    def game_over(self):
        self.game_active = False
        while not self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    self.running = False
                    self.game_quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_active = True
            self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))
            self.DUMMY_WINDOW.blit(self.assets.game_over, self.assets.game_over_rect)
            self.display_score()
            self.scale_window()

    def play(self):
        self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))
        self.snake.walk()
        
        if check_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            
        for i in range(3, self.snake.length):
            if check_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.game_over()
    
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    @staticmethod
    def game_quit():
        pygame.quit()
        sys.exit()

    def display_score(self):
        score = self.font.render(f"Score: {self.snake.length}", True, self.WHITE)
        score_rect = score.get_rect(topright=(990, 10))

        hi_score = self.font.render(f"High Score: {self.high_score}", True, self.WHITE)
        hi_score_rect = hi_score.get_rect(center=(500, 700))
        
        self.high_score = update_score(self.snake.length, self.high_score)

        self.DUMMY_WINDOW.blit(score, score_rect)
        if not self.game_active:
            self.DUMMY_WINDOW.blit(hi_score, hi_score_rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.move_up()
                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()
                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_quit()

            if self.game_active:
                self.play()

                time.sleep(0.15)

            self.scale_window()


if __name__ == "__main__":
    game = Game()
    game.run()
