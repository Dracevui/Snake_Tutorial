import pygame
import sys
import math
import random

SIZE = 40


def screen_dimensions(x, y):
    monitor = pygame.display.Info()
    base_x, base_y = 1920, 1080
    target_x = x / base_x
    target_y = y / base_y
    final_x, final_y = math.ceil(monitor.current_w * target_x), math.ceil(monitor.current_h * target_y)
    return final_x, final_y


def update_score(score, hi_score):
    if score > hi_score:
        hi_score = score
    return hi_score


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.transform.scale((pygame.image.load("resources/pizza_bubble.png").convert_alpha()), (40, 40))
        self.crunch = pygame.mixer.Sound("resources/crunch.wav")
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE

    def play_sound(self):
        pygame.mixer.Channel(1).play(self.crunch)


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert_alpha()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.WHITE = (255, 255, 255)
        self.MAGENTA = (142, 63, 255)
        self.direction = ""
        self.north = False
        self.south = True
        self.east = False
        self.west = False

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if not self.east:
            self.direction = "left"
            self.north = False
            self.south = False
            self.east = False
            self.west = True

    def move_right(self):
        if not self.west:
            self.direction = "right"
            self.north = False
            self.south = False
            self.east = True
            self.west = False

    def move_up(self):
        if not self.south:
            self.direction = "up"
            self.north = True
            self.south = False
            self.east = False
            self.west = False

    def move_down(self):
        if not self.north:
            self.direction = "down"
            self.north = False
            self.south = True
            self.east = False
            self.west = False

    def draw(self):
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
        self.background = pygame.transform.scale((pygame.image.load("resources/water_background.png")), (1000, 800))
        self.game_over = pygame.image.load("resources/game_over.png")
        self.press_spacebar_surface = pygame.image.load("resources/press_spacebar2.png")
        self.icon = pygame.image.load("resources/icon.png")
        self.bgm = pygame.mixer.Sound("resources/bgm.wav")

    def play_bgm(self):
        self.bgm.play(-1)


class Game:
    def __init__(self):
        # Game Initialisation
        pygame.init()
        pygame.display.set_caption("Blockey Snakey")

        # Game Constants
        self.MONITOR = pygame.display.Info()
        self.SCREEN_DIMENSIONS = screen_dimensions(1000, 800)
        self.WINDOW = pygame.display.set_mode(self.SCREEN_DIMENSIONS)
        self.DUMMY_WINDOW = pygame.Surface((1000, 800))
        self.WIDTH, HEIGHT = self.SCREEN_DIMENSIONS
        self.WINDOW_WIDTH = self.WINDOW.get_width()
        self.WINDOW_HEIGHT = self.WINDOW.get_height()
        self.FONT = pygame.font.SysFont('Impact', 50)
        self.WHITE = (255, 255, 255)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 10

        # Class Imports
        self.snake = Snake(self.DUMMY_WINDOW, 1)
        self.apple = Apple(self.DUMMY_WINDOW)
        self.assets = Assets()
        pygame.display.set_icon(self.assets.icon)

        # Game Variables
        self.running = True
        self.game_active = True
        self.high_score = 0

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
                    self.game_clear()
            self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))
            self.DUMMY_WINDOW.blit(self.assets.game_over, (268, 188))
            self.DUMMY_WINDOW.blit(self.assets.press_spacebar_surface, (260, 21))
            self.display_score()
            self.scale_window()

    def game_clear(self):
        self.snake.length = 1
        self.snake.direction = ""

    def play(self):
        self.DUMMY_WINDOW.blit(self.assets.background, (0, 0))
        self.snake.walk()
        
        if self.check_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            
        for i in range(3, self.snake.length):
            if self.check_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.game_over()

        self.display_score()
        self.apple.draw()
        pygame.display.flip()

    def check_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE:
            self.apple.play_sound()
            return True
        return False

    def scale_window(self):  # Scales the game window and assets to fit the user's monitor dimensions
        frame = pygame.transform.scale(self.DUMMY_WINDOW, self.SCREEN_DIMENSIONS)
        self.WINDOW.blit(frame, frame.get_rect())
        pygame.display.flip()

    @staticmethod
    def game_quit():
        pygame.quit()
        sys.exit()

    def display_score(self):
        score = self.FONT.render(f"Score: {self.snake.length - 1}", True, self.WHITE)
        hi_score = self.FONT.render(f"High Score: {self.high_score}", True, self.WHITE)
        
        self.high_score = update_score(self.snake.length - 1, self.high_score)

        self.DUMMY_WINDOW.blit(score, (823, 735))
        if not self.game_active:
            self.DUMMY_WINDOW.blit(hi_score, (365, 690))

    def run(self):
        self.assets.play_bgm()
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

            self.scale_window()

            self.CLOCK.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
