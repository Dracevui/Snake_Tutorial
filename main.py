import pygame
import sys
import math


class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = 100
        self.y = 100
        self.WHITE = (255, 255, 255)
        self.MAGENTA = (142, 63, 255)

    def move_left(self):
        self.x -= 10
        self.draw()

    def move_right(self):
        self.x += 10
        self.draw()

    def move_up(self):
        self.y -= 10
        self.draw()

    def move_down(self):
        self.y += 10
        self.draw()

    def draw(self):
        self.parent_screen.fill(self.MAGENTA)
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.MONITOR = pygame.display.Info()
        self.SCREEN_DIMENSIONS = (math.ceil(self.MONITOR.current_w * 0.26), math.floor(self.MONITOR.current_h * 0.463))
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.DUMMY_WINDOW = pygame.Surface((500, 500))
        self.WIDTH, HEIGHT = self.SCREEN_DIMENSIONS
        self.WINDOW_WIDTH = self.WINDOW.get_width()
        self.WINDOW_HEIGHT = self.WINDOW.get_height()

        self.snake = Snake(self.DUMMY_WINDOW)
        self.snake.draw()

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    @staticmethod
    def game_quit():
        pygame.quit()
        sys.exit()

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
            self.scale_window()


if __name__ == "__main__":
    game = Game()
    game.run()
