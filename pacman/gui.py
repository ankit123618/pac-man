import pygame
import random

# Game constants
WIDTH = 640
HEIGHT = 480
PACMAN_RADIUS = 20
GHOST_RADIUS = 18
COIN_RADIUS = 6
PACMAN_SPEED = 5
GHOST_SPEED = 3
COIN_SCORE = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create game objects
pacman_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
pacman_dir = pygame.Vector2(0, 0)
ghost_pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
ghost_dir = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))
coins = [pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(20)]

# Game loop
running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pacman_dir = pygame.Vector2(0, -1)
    elif keys[pygame.K_DOWN]:
        pacman_dir = pygame.Vector2(0, 1)
    elif keys[pygame.K_LEFT]:
        pacman_dir = pygame.Vector2(-1, 0)
    elif keys[pygame.K_RIGHT]:
        pacman_dir = pygame.Vector2(1, 0)

    pacman_pos += pacman_dir * PACMAN_SPEED
    ghost_pos += ghost_dir * GHOST_SPEED

    # Check collision with walls
    if pacman_pos.x < 0:
        pacman_pos.x = WIDTH
    elif pacman_pos.x > WIDTH:
        pacman_pos.x = 0
    if pacman_pos.y < 0:
        pacman_pos.y = HEIGHT
    elif pacman_pos.y > HEIGHT:
        pacman_pos.y = 0

    if ghost_pos.x < 0 or ghost_pos.x > WIDTH:
        ghost_dir.x *= -1
    if ghost_pos.y < 0 or ghost_pos.y > HEIGHT:
        ghost_dir.y *= -1

    # Check collision with coins
    for coin in coins:
        if coin.distance_to(pacman_pos) < PACMAN_RADIUS + COIN_RADIUS:
            coins.remove(coin)
            score += COIN_SCORE

    # Check collision with ghost
    if pacman_pos.distance_to(ghost_pos) < PACMAN_RADIUS + GHOST_RADIUS:
        running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, pacman_pos, PACMAN_RADIUS)

    # Draw ghost
    pygame.draw.circle(screen, RED, ghost_pos, GHOST_RADIUS)

    # Draw coins
    for coin in coins:
        pygame.draw.circle(screen, BLUE, coin, COIN_RADIUS)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Game over
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(2000)

# Quit the game
pygame.quit()
