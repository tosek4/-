import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
SHIP_SPEED = 5
ASTEROID_SPEED = 3
CRYSTAL_SPEED = 2
FONT_COLOR = (255, 255, 255)
SHIP_SIZE = (50, 50)
ASTEROID_SIZE = (50, 50)
CRYSTAL_SIZE = (30, 30)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Load assets
ship_img = pygame.image.load("assets/images/spaceship.png")
ship_img = pygame.transform.scale(ship_img, SHIP_SIZE)
asteroid_img = pygame.image.load("assets/images/asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, ASTEROID_SIZE)
crystal_img = pygame.image.load("assets/images/crystal.png")
crystal_img = pygame.transform.scale(crystal_img, CRYSTAL_SIZE)

# Sound
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.play(-1)  # Loop background music
collect_sound = pygame.mixer.Sound("assets/sounds/collect.wav.mp3")
collision_sound = pygame.mixer.Sound("assets/sounds/collision.wav.mp3")

# Fonts
font = pygame.font.Font(None, 36)

# Display text on the screen
def display_text(text, x, y, color=FONT_COLOR):

    label = font.render(text, True, color)
    screen.blit(label, (x, y))


# Draw the player's ship
def draw_ship(x, y):
    screen.blit(ship_img, (x, y))


# Draw asteroids on the screen
def draw_asteroid(asteroids):
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid["x"], asteroid["y"]))


# Draw energy crystals on the screen
def draw_crystal(crystals):
    for crystal in crystals:
        screen.blit(crystal_img, (crystal["x"], crystal["y"]))


# Check if two rectangles collide
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def main():
    clock = pygame.time.Clock()

    # Game variables
    ship_x, ship_y = WIDTH // 2, HEIGHT - 70
    score = 0
    game_over = False
    asteroid_speed = ASTEROID_SPEED
    crystal_speed = CRYSTAL_SPEED

    # Asteroids and crystals
    asteroids = [{"x": random.randint(0, WIDTH - ASTEROID_SIZE[0]), "y": random.randint(-200, -50)} for _ in range(5)]
    crystals = [{"x": random.randint(0, WIDTH - CRYSTAL_SIZE[0]), "y": random.randint(-200, -50)} for _ in range(3)]

    while True:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT] and ship_x > 0:
                ship_x -= SHIP_SPEED
            if keys[pygame.K_RIGHT] and ship_x < WIDTH - SHIP_SIZE[0]:
                ship_x += SHIP_SPEED

        # Update asteroids
        for asteroid in asteroids:
            asteroid["y"] += asteroid_speed
            if asteroid["y"] > HEIGHT:
                asteroid["x"] = random.randint(0, WIDTH - ASTEROID_SIZE[0])
                asteroid["y"] = random.randint(-200, -50)

        # Update crystals
        for crystal in crystals:
            crystal["y"] += crystal_speed
            if crystal["y"] > HEIGHT:
                crystal["x"] = random.randint(0, WIDTH - CRYSTAL_SIZE[0])
                crystal["y"] = random.randint(-200, -50)

        # Check collisions
        ship_rect = pygame.Rect(ship_x, ship_y, SHIP_SIZE[0], SHIP_SIZE[1])

        for asteroid in asteroids:
            asteroid_rect = pygame.Rect(asteroid["x"], asteroid["y"], ASTEROID_SIZE[0], ASTEROID_SIZE[1])
            if check_collision(ship_rect, asteroid_rect):
                collision_sound.play()
                game_over = True

        for crystal in crystals:
            crystal_rect = pygame.Rect(crystal["x"], crystal["y"], CRYSTAL_SIZE[0], CRYSTAL_SIZE[1])
            if check_collision(ship_rect, crystal_rect):
                collect_sound.play()
                score += 1
                crystal["x"] = random.randint(0, WIDTH - CRYSTAL_SIZE[0])
                crystal["y"] = random.randint(-200, -50)

        # Draw everything
        draw_ship(ship_x, ship_y)
        draw_asteroid(asteroids)
        draw_crystal(crystals)
        display_text(f"Score: {score}", 10, 10)

        if game_over:
            display_text("GAME OVER!", WIDTH // 2 - 100, HEIGHT // 2, WHITE)
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        # Update screen
        pygame.display.flip()
        clock.tick(FPS)

        # Increase difficulty over time
        if not game_over and pygame.time.get_ticks() % 5000 == 0:
            asteroid_speed += 0.5
            crystal_speed += 0.3


# Run the game
if __name__ == "__main__":
    main()
