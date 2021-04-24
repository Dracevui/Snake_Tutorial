import pygame
import sys
import math
import time
import random

SIZE = 40


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
        self.parent_screen.fill(self.MAGENTA)
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


class Game:
    def __init__(self):
        pygame.init()
        self.MONITOR = pygame.display.Info()
        self.SCREEN_DIMENSIONS = (math.ceil(self.MONITOR.current_w * 0.5206), math.ceil(self.MONITOR.current_h * 0.74))
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.DUMMY_WINDOW = pygame.Surface((1000, 800))
        self.WIDTH, HEIGHT = self.SCREEN_DIMENSIONS
        self.WINDOW_WIDTH = self.WINDOW.get_width()
        self.WINDOW_HEIGHT = self.WINDOW.get_height()
        self.WHITE = (255, 255, 255)

        self.snake = Snake(self.DUMMY_WINDOW, 1)
        self.snake.draw()

        self.apple = Apple(self.DUMMY_WINDOW)
        self.apple.draw()

    def check_apple_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE:
            return True
        return False

    def play(self):
        self.snake.walk()
        if self.check_apple_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
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
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, self.WHITE)
        score_rect = score.get_rect(topright=(990, 10))
        self.DUMMY_WINDOW.blit(score, score_rect)
        pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
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
                    running = False
                    self.game_quit()

            self.play()

            time.sleep(0.15)

            self.scale_window()


if __name__ == "__main__":
    game = Game()
    game.run()
