import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH = 1000
HEIGHT = 800
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Game")

# Set up the font
font = pygame.font.Font(None, 36)

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = "RIGHT"
        self.food = self.generate_food()

    def generate_food(self):
        while True:
            food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE, random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
            if food not in self.snake:
                return food

    def draw(self):
        win.fill(BLACK)
        for i, pos in enumerate(self.snake):
            if i == len(self.snake) - 1:
                pygame.draw.rect(win, ORANGE, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            else:
                pygame.draw.rect(win, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(win, RED, (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f"Score: {len(self.snake)}", True, WHITE)
        win.blit(text, (10, 10))
        pygame.display.update()

    def move(self):
        head = self.snake[-1]
        if self.direction == "RIGHT":
            new_head = (head[0] + BLOCK_SIZE, head[1])
        elif self.direction == "LEFT":
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif self.direction == "UP":
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + BLOCK_SIZE)
        self.snake.append(new_head)
        if self.food == new_head:
            self.food = self.generate_food()
        else:
            self.snake.pop(0)

    def check_collision(self):
        head = self.snake[-1]
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.snake[:-1]):
            return True
        return False

def draw_menu():
    win.fill(BLACK)
    text = font.render("Python Game", True, WHITE)
    win.blit(text, (WIDTH // 2 - 75, 100))
    text = font.render("Movement:-WASD", True, WHITE)
    win.blit(text, (WIDTH // 2 - 75, 150))
    text = font.render("Press 1 to play", True, WHITE)
    win.blit(text, (WIDTH // 2 - 75, 200))
    text = font.render("Press 2 to quit", True, WHITE)
    win.blit(text, (WIDTH // 2 - 75, 250))
    pygame.display.update()

def draw_game_over(score):
    win.fill(BLACK)
    text = font.render("Game Over!", True, WHITE)
    win.blit(text, (WIDTH // 2 - 75, 100))
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, (WIDTH // 2 - 50, 150))
    pygame.draw.rect(win, GREEN, (WIDTH // 2 - 100, 250, 200, 50))
    text = font.render("Restart", True, WHITE)
    win.blit(text, (WIDTH // 2 - 60, 260))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    game = None
    menu = True
    game_over = False
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if menu:
                    if event.key == pygame.K_1:
                        game = SnakeGame()
                        menu = False
                    elif event.key == pygame.K_2:
                        pygame.quit()
                        sys.exit()
                elif not game_over:
                    if event.key == pygame.K_w and game.direction != "DOWN":
                        game.direction = "UP"
                    elif event.key == pygame.K_s and game.direction != "UP":
                        game.direction = "DOWN"
                    elif event.key == pygame.K_a and game.direction != "RIGHT":
                        game.direction = "LEFT"
                    elif event.key == pygame.K_d and game.direction != "LEFT":
                        game.direction = "RIGHT"
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if WIDTH // 2 - 100 < event.pos[0] < WIDTH // 2 + 100 and 250 < event.pos[1] < 300:
                    game = SnakeGame()
                    game_over = False
        if menu:
            draw_menu()
        elif not game_over:
            game.move()
            if game.check_collision():
                score = len(game.snake)
                game_over = True
            game.draw()
        else:
            draw_game_over(score)
        clock.tick(10)

if __name__ == "__main__":
    main()
