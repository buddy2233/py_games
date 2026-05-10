import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
import sys

# --- Init ---
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Game")
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# --- Constants ---
QUESTION_TIME = 30000           # 30 seconds in milliseconds

# --- Questions ---
questions = [
    {"question": "What’s 2+2?", "options": ["3", "4", "5"], "answer": "4"},
    {"question": "Which color is the sky?", "options": ["Green", "Blue", "Red"], "answer": "Blue"},
    {"question": "Which is the largest animal on earth?", "options": ["Tiger", "Blue Whale", "Elephant"], "answer": "Blue Whale"},
    {"question": "If X/Y + Y/X = 1 than what is (X+Y)^3 = ?", "options": ["2", "1", "0"], "answer": "0"},
    {"question": "Find the difference:-", "options": ["Hen", "Parrot", "Human", "Dove"], "answer": "Human"},
    {"question": "If mouse is an input device; than a speaker is", "options": ["Input device", "Output device", "None of above"], "answer": "Output device"},
    {"question": "I ___ to a zoo, yesterday(Fill in the blank)", "options": ["went", "go", "gone"], "answer": "went"},
    {"question": "How many planets are in our solar system?", "options": ["8", "9", "1 X 10^10^10^10^10"], "answer": "8"},
    {"question": "1N = ?", "options": ["1 Kg.m/S^2", "9.8g.m/s", "0"], "answer": "1Kg.m/s^2"},
    {"question": "What is 6 ÷ 2(1+2) = ?", "options": ["1", "9", "0"], "answer": "1"}, #add your own questions
]
current_q = 0
score = 0
quiz_over = False
start_time = pygame.time.get_ticks()

def draw_question():
    """Draw the current question & options; return True if time’s up."""
    screen.fill((255, 255, 255))
    # Timer (top-right)
    elapsed = pygame.time.get_ticks() - start_time
    time_left = max(0, (QUESTION_TIME - elapsed) // 1000)
    timer_text = font.render(f"Time: {time_left}s", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH - 100, 10))
    
    # Question & options
    q_text = font.render(questions[current_q]["question"], True, (0, 0, 0))
    screen.blit(q_text, (20, 20))
    for i, opt in enumerate(questions[current_q]["options"]):
        opt_text = font.render(f"{i+1}. {opt}", True, (0, 0, 0))
        screen.blit(opt_text, (20, 60 + i * 30))
    
    return time_left <= 0

def draw_end_screen():
    """Draw “Quiz Over” + score + Reset button."""
    screen.fill((255, 255, 255))
    end_text = font.render(f"Quiz Over! Score: {score}/{len(questions)}", True, (0, 0, 0))
    screen.blit(end_text, (WIDTH//2 - 100, HEIGHT//2 - 20))
    reset_text = font.render("Reset", True, (0, 0, 0))
    reset_rect = pygame.Rect(WIDTH//2 - 40, HEIGHT//2 + 20, 80, 30)
    pygame.draw.rect(screen, (200, 200, 200), reset_rect)
    screen.blit(reset_text, (WIDTH//2 - 25, HEIGHT//2 + 25))
    return reset_rect

def reset_quiz():
    """Reset all game state."""
    global current_q, score, quiz_over, start_time
    current_q = 0
    score = 0
    quiz_over = False
    start_time = pygame.time.get_ticks()

# --- Main Loop ---
running = True
while running:
    if not quiz_over:
        time_up = draw_question()
        if time_up:
            current_q += 1
            if current_q >= len(questions):
                quiz_over = True
            else:
                start_time = pygame.time.get_ticks()  # Reset timer for next Q
    else:
        reset_rect = draw_end_screen()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and not quiz_over:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                chosen = questions[current_q]["options"][event.key - pygame.K_1]
                if chosen == questions[current_q]["answer"]:
                    score += 1
                current_q += 1
                if current_q >= len(questions):
                    quiz_over = True
                else:
                    start_time = pygame.time.get_ticks()  # Reset timer
        if event.type == pygame.MOUSEBUTTONDOWN and quiz_over:
            if reset_rect.collidepoint(event.pos):
                reset_quiz()

    clock.tick(30)

pygame.quit()
