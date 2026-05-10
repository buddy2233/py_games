import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pygame')
import pygame
import sys
import random

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# Paddle
paddle_width = 10
paddle_height = 100
paddle_speed = 6

# Ball
ball_size = 15
ball_speed_x = 5 * random.choice((1,-1))
ball_speed_y = 5 * random.choice((1,-1))

# Player paddles
left_paddle = pygame.Rect(20, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH-30, HEIGHT//2 - paddle_height//2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_size, ball_size)

# Score
left_score = 0
right_score = 0
font = pygame.font.Font(None, 50)

# Mode select
mode = ""
clock = pygame.time.Clock()
while mode not in ["ai", "multi"]:
    screen.fill(BLACK)
    text1 = font.render("Press 1 for AI", True, WHITE)
    text2 = font.render("Press 2 for Multiplayer", True, WHITE)
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 50))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "ai"
            if event.key == pygame.K_2:
                mode = "multi"
    clock.tick(60)

def reset_ball():
    ball.center = (WIDTH//2, HEIGHT//2)
    return 5 * random.choice((1,-1)), 5 * random.choice((1,-1))

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # Left paddle (Player 1)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed

    # Right paddle
    if mode == "multi":
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed
    elif mode == "ai":
        # Simple AI tracking
        if right_paddle.centery < ball.centery:
            right_paddle.y += paddle_speed - 2
        if right_paddle.centery > ball.centery:
            right_paddle.y -= paddle_speed - 2

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Wall collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Paddle collision
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1

    # Scoring
    if ball.left <= 0:
        right_score += 1
        ball_speed_x, ball_speed_y = reset_ball()
    if ball.right >= WIDTH:
        left_score += 1
        ball_speed_x, ball_speed_y = reset_ball()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2,0),(WIDTH//2,HEIGHT))
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text,(WIDTH//4,20))
    screen.blit(right_text,(WIDTH*3//4,20))
    pygame.display.flip()
