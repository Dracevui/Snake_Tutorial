import pygame
from pygame.locals import *
import sys
import math


def game_quit():
    pygame.quit()
    sys.exit()


def scale_window():  # Scales the game window and assets to fit the user's monitor dimensions
    DUMMY_WINDOW.fill(MAGENTA)
    DUMMY_WINDOW.blit(block, (block_x, block_y))
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

    # Asset Files
    block = pygame.image.load("resources/block.jpg").convert()
    block_x = 100
    block_y = 100

    # Game Variables
    running = True

    while running:
        scale_window()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    block_y -= 10
                if event.key == K_DOWN:
                    block_y += 10
                if event.key == K_LEFT:
                    block_x -= 10
                if event.key == K_RIGHT:
                    block_x += 10
                scale_window()
            if event.type == QUIT:
                running = False
                game_quit()
