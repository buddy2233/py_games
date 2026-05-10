import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
import sys
import random

TILE = 32
BASE_W, BASE_H = 15, 11 # Starting maze size
PLAYER_SIZE = 14
PLAYER_SPEED = 3

def generate_maze(w, h):
    maze = [[1 for _ in range(w)] for _ in range(h)]

    def carve(x, y):
        maze[y][x] = 0
        dirs = [(0,-2), (2,0), (0,2), (-2,0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < w-1 and 0 < ny < h-1 and maze[ny][nx] == 1:
                maze[y + dy//2][x + dx//2] = 0
                carve(nx, ny)

    carve(1, 1)
    maze[h-2][w-2] = 2 # goal
    return maze

pygame.init()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()

level = 1
MAZE_W = BASE_W + (level - 1) * 4
MAZE_H = BASE_H + (level - 1) * 2
MAZE = generate_maze(MAZE_W, MAZE_H)
WIDTH, HEIGHT = MAZE_W * TILE, MAZE_H * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player:
    def __init__(self):
        self.x = 1.5 * TILE
        self.y = 1.5 * TILE

    def move(self, dx, dy):
        new_rect = pygame.Rect(self.x + dx, self.y + dy, PLAYER_SIZE, PLAYER_SIZE)
        tile_x1 = int(new_rect.left // TILE)
        tile_y1 = int(new_rect.top // TILE)
        tile_x2 = int(new_rect.right // TILE)
        tile_y2 = int(new_rect.bottom // TILE)

        for ty in range(tile_y1, tile_y2 + 1):
            for tx in range(tile_x1, tile_x2 + 1):
                if 0 <= ty < len(MAZE) and 0 <= tx < len(MAZE[0]):
                    if MAZE[ty][tx] == 1:
                        wall = pygame.Rect(tx*TILE, ty*TILE, TILE, TILE)
                        if new_rect.colliderect(wall):
                            return
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.circle(screen, (80, 220, 255), (int(self.x), int(self.y)), PLAYER_SIZE//2)
        pygame.draw.circle(screen, (200, 240, 255), (int(self.x), int(self.y)), PLAYER_SIZE//2, 2)

def draw_maze():
    for y in range(len(MAZE)):
        for x in range(len(MAZE[0])):
            tile = MAZE[y][x]
            px, py = x * TILE, y * TILE
            if tile == 1:
                pygame.draw.rect(screen, (35, 35, 50), (px, py, TILE, TILE))
                pygame.draw.rect(screen, (50, 50, 70), (px, py, TILE, TILE), 1)
            elif tile == 2:
                # Pulsing goal
                pulse = int(128 + 127 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
                pygame.draw.rect(screen, (50, pulse, 120), (px+4, py+4, TILE-8, TILE-8))
                pygame.draw.rect(screen, (200, 255, 200), (px+4, py+4, TILE-8, TILE-8), 2)

def check_win(p):
    tile_x = int(p.x // TILE)
    tile_y = int(p.y // TILE)
    if 0 <= tile_y < len(MAZE) and 0 <= tile_x < len(MAZE[0]):
        return MAZE[tile_y][tile_x] == 2
    return False

def next_level():
    global level, MAZE_W, MAZE_H, MAZE, WIDTH, HEIGHT, screen, player
    level += 1
    MAZE_W = BASE_W + (level - 1) * 4
    MAZE_H = BASE_H + (level - 1) * 2
    MAZE = generate_maze(MAZE_W, MAZE_H)
    WIDTH, HEIGHT = MAZE_W * TILE, MAZE_H * TILE
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player()

player = Player()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: # Reset current level
                MAZE = generate_maze(MAZE_W, MAZE_H)
                player = Player()

    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = PLAYER_SPEED
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -PLAYER_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = PLAYER_SPEED

    player.move(dx, dy)

    screen.fill((15, 15, 25))
    draw_maze()
    player.draw()

    # UI
    level_text = font.render(f"Level: {level}", True, (200, 200, 200))
    info_text = font.render("WASD: Move | R: Reset Level", True, (200, 200, 200))
    screen.blit(level_text, (10, 10))
    screen.blit(info_text, (10, HEIGHT - 30))

    if check_win(player):
        win_text = big_font.render(f"Level {level} Complete!", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.wait(1500)
        next_level()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
