import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 40
ITEM_RADIUS = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hoppy Rabbit")

# Load images
player_image = pygame.image.load("pet.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

food_images = []
food_files = ["carrot.png", "hay.png"]
for food_file in food_files:
    food_image = pygame.image.load(food_file)
    food_image = pygame.transform.scale(food_image, (ITEM_RADIUS * 2, ITEM_RADIUS * 2))
    food_images.append(food_image)

obstacle_images = []
obstacle_files = ["avocado.png", "chocolate.png", "meat.png"]
for obstacle_file in obstacle_files:
    obstacle_image = pygame.image.load(obstacle_file)
    obstacle_image = pygame.transform.scale(obstacle_image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    obstacle_images.append(obstacle_image)

background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize player position
player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE - 120

# Initialize obstacles and items
obstacles = []
items = []

# Initialize the number of collected items
collected_items = 0

# Game loop
running = True
clock = pygame.time.Clock()

# Game over function
def game_over_screen(collected_items):
    screen.fill((0, 0, 0))  # Fill screen with black

    font_large = pygame.font.Font(None, 64)
    text_game_over = font_large.render("Game Over", True, WHITE)
    text_points = font_large.render("Points: " + str(collected_items), True, WHITE)

    font_small = pygame.font.Font(None, 36)
    text_restart = font_small.render("Restart", True, BLACK)
    text_quit = font_small.render("Quit", True, BLACK)

    # Display game over text and points
    screen.blit(text_game_over, (SCREEN_WIDTH // 2 - text_game_over.get_width() // 2, 200))
    screen.blit(text_points, (SCREEN_WIDTH // 2 - text_points.get_width() // 2, 300))

    # Draw restart and quit buttons
    restart_rect = pygame.Rect(300, 400, 200, 50)
    quit_rect = pygame.Rect(300, 500, 200, 50)
    pygame.draw.rect(screen, WHITE, restart_rect)
    pygame.draw.rect(screen, WHITE, quit_rect)
    screen.blit(text_restart, (350, 410))
    screen.blit(text_quit, (370, 510))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Check if restart button clicked
                if restart_rect.collidepoint(mouse_pos):
                    return True

                # Check if quit button clicked
                if quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keys
    keys = pygame.key.get_pressed()

    # Update player position based on key presses
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED

    # Spawn new obstacles and items
    if random.randint(1, 100) < 5:
        obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        obstacle_type = random.choice(obstacle_images)
        obstacles.append([obstacle_x, -OBSTACLE_HEIGHT, obstacle_type])
    if random.randint(1, 100) < 2:
        item_x = random.randint(0, SCREEN_WIDTH - ITEM_RADIUS * 2)
        item_type = random.choice(food_images)
        items.append([item_x, -ITEM_RADIUS, item_type])

    # Update obstacle and item positions
    for obstacle in obstacles:
        obstacle[1] += 5
    for item in items:
        item[1] += 5

    # Check for collisions with obstacles and items
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        if player_rect.colliderect(obstacle_rect):
            print("Game Over! You hit an obstacle.")
            running = False
            # Display game over screen and get restart choice
            restart = game_over_screen(collected_items)
            if restart:
                # Reset game state
                obstacles = []
                items = []
                collected_items = 0
                player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
                player_y = SCREEN_HEIGHT - PLAYER_SIZE - 120
                running = True

    for item in items:
        item_rect = pygame.Rect(item[0], item[1], ITEM_RADIUS * 2, ITEM_RADIUS * 2)
        if player_rect.colliderect(item_rect):
            items.remove(item)
            collected_items += 1
            print("Item collected! Total items:", collected_items)

    # Clear the screen and draw the background
    screen.blit(background_image, (0, 0))

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    # Draw obstacles and items
    for obstacle in obstacles:
        screen.blit(obstacle[2], (obstacle[0], obstacle[1]))
    for item in items:
        screen.blit(item[2], (item[0], item[1]))

    # Display collected items
    font = pygame.font.Font(None, 36)
    text = font.render("Points: " + str(collected_items), True, WHITE)
    screen.blit(text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
