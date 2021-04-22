import pygame
from pygame.locals import *
import sys
import math


def game_quit():
    pygame.quit()
    sys.exit()


def scale_window():  # Scales the game window and assets to fit the user's monitor dimensions
    frame = pygame.transform.scale(DUMMY_WINDOW, SCREEN_DIMENSIONS)
    WINDOW.blit(frame, frame.get_rect())
    pygame.display.flip()


if __name__ == "__main__":
    # Constants
    pygame.init()
    MONITOR = pygame.display.Info()
    SCREEN_DIMENSIONS = (math.ceil(MONITOR.current_w * 0.26), math.floor(MONITOR.current_h * 0.463))
    WINDOW = pygame.display.set_mode(SCREEN_DIMENSIONS)
    DUMMY_WINDOW = pygame.Surface((500, 500))
    WIDTH, HEIGHT = SCREEN_DIMENSIONS
    WINDOW_WIDTH = WINDOW.get_width()
    WINDOW_HEIGHT = WINDOW.get_height()

    # Colours
    WHITE = (255, 255, 255)
    MAGENTA = (142, 63, 255)

    DUMMY_WINDOW.fill(MAGENTA)
    scale_window()

    # Asset Files
    block = pygame.image.load("resources/block.jpg").convert()

    # Game Variables
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == QUIT:
                running = False
                game_quit()
