# Import packages
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Ball dimensions
BALL_SIZE = 10
BALL_SPEED = [5, 5]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ping Pong Game')

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Ball class
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.vx = BALL_SPEED[0]
        self.vy = BALL_SPEED[1]

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Create paddles and ball
player_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2)

player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_paddle.rect.top > 0:
        player_paddle.rect.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player_paddle.rect.bottom < SCREEN_HEIGHT:
        player_paddle.rect.y += PADDLE_SPEED

    # AI opponent
    if ball.vx > 0:
        if ai_paddle.rect.centery < ball.rect.centery:
            ai_paddle.rect.y += PADDLE_SPEED
        elif ai_paddle.rect.centery > ball.rect.centery:
            ai_paddle.rect.y -= PADDLE_SPEED

    # Update ball position
    ball.rect.x += ball.vx
    ball.rect.y += ball.vy

    # Ball collision with walls
    if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
        ball.vy = -ball.vy

    # Ball collision with paddles
    if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(ai_paddle.rect):
        ball.vx = -ball.vx

    # Ball out of bounds
    if ball.rect.left <= 0:
        ai_score += 1
        ball.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        ball.vx = BALL_SPEED[0]
        ball.vy = BALL_SPEED[1]

    if ball.rect.right >= SCREEN_WIDTH:
        player_score += 1
        ball.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        ball.vx = -BALL_SPEED[0]
        ball.vy = BALL_SPEED[1]

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()

    # Draw the score
    score_text = font.render(f"{player_score} - {ai_score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit frame rate to 60 FPS
