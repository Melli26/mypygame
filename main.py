import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Click the Circles')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color for the controllable circle
BLUE = (0, 0, 255)   # Color for the outer circle
BLACK = (0, 0, 0)    # Color for the health bar border
LIGHT_RED = (255, 100, 100)  # Color for the health bar background

# Font
FONT = pygame.font.Font(None, 36)

# Circle settings
CIRCLE_RADIUS = 30
PLAYER_RADIUS = 10
ARROW_SPEED = 5
ACCELERATED_SPEED = 10
OUTER_RADIUS = CIRCLE_RADIUS + 10  # Initial outer circle radius
OUTER_RADIUS_MIN = CIRCLE_RADIUS    # Minimum radius of the outer circle

# Timing settings
TIME_LIMIT = 3  # Time in seconds for the outer circle to shrink

# Game settings
PLAYER_INITIAL_HP = 3  # Number of misses allowed before the game ends
HEALTH_BAR_WIDTH = 80
HEALTH_BAR_HEIGHT = 10

def spawn_circle():
    x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)
    return x, y

def draw_health_bar(surface, hp):
    bar_x = 10
    bar_y = 10  # Position the bar in the upper-left corner
    hp_percentage = hp / PLAYER_INITIAL_HP
    pygame.draw.rect(surface, BLACK, [bar_x - 2, bar_y - 2, HEALTH_BAR_WIDTH + 4, HEALTH_BAR_HEIGHT + 4], 0)  # Border
    pygame.draw.rect(surface, LIGHT_RED, [bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT])  # Background
    pygame.draw.rect(surface, RED, [bar_x, bar_y, HEALTH_BAR_WIDTH * hp_percentage, HEALTH_BAR_HEIGHT])  # Foreground

def draw_instructions(surface):
    instructions = [
        "Instructions:",
        "Use arrow keys to move",
        "Press Shift to move faster",
        "Press Space to start the game"
    ]
    for i, line in enumerate(instructions):
        text = FONT.render(line, True, BLACK)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + i * 40))

def draw_game_over(surface, highest_combo):
    game_over_message = [
        "Game Over!",
        "You lost!",
        f"Highest Combo: {highest_combo}",
        "Press Space to try again"
    ]
    for i, line in enumerate(game_over_message):
        text = FONT.render(line, True, BLACK)
        surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 + i * 40))

def draw_combo(surface, combo):
    combo_text = FONT.render(f"Combo: {combo}", True, BLACK)
    surface.blit(combo_text, (WIDTH - combo_text.get_width() - 10, 10))  # Upper-right corner

def main():
    clock = pygame.time.Clock()
    show_instructions = True
    game_over = False
    highest_combo = 0
    current_combo = 0
    circle_x, circle_y = spawn_circle()
    player_x, player_y = WIDTH // 2, HEIGHT // 2  # Initial position of the controllable circle
    start_time = None
    player_hp = PLAYER_INITIAL_HP
    missed_circles = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if show_instructions:
                        show_instructions = False
                        start_time = time.time()  # Start the timer
                    elif game_over:
                        game_over = False
                        highest_combo = max(highest_combo, current_combo)
                        current_combo = 0
                        player_hp = PLAYER_INITIAL_HP
                        missed_circles = 0
                        circle_x, circle_y = spawn_circle()  # Spawn new circle
                        start_time = time.time()  # Reset the timer
                    else:
                        # Check if the click was within the circle bounds
                        if (player_x - circle_x) ** 2 + (player_y - circle_y) ** 2 <= CIRCLE_RADIUS ** 2:
                            circle_x, circle_y = spawn_circle()  # Spawn new circle
                            start_time = time.time()  # Reset the timer
                            current_combo += 1  # Increase combo
                        else:
                            missed_circles += 1
                            player_hp -= 1  # Reduce player's HP for each miss
                            if player_hp <= 0:
                                game_over = True  # End the game
                                show_instructions = False  # Show game over message
                            current_combo = 0  # Reset combo

        if not show_instructions and not game_over:
            keys = pygame.key.get_pressed()
            move_speed = ACCELERATED_SPEED if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else ARROW_SPEED

            if keys[pygame.K_LEFT]:
                player_x -= move_speed
            if keys[pygame.K_RIGHT]:
                player_x += move_speed
            if keys[pygame.K_UP]:
                player_y -= move_speed
            if keys[pygame.K_DOWN]:
                player_y += move_speed

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            # Calculate the radius of the outer circle
            outer_radius = max(OUTER_RADIUS - (OUTER_RADIUS - OUTER_RADIUS_MIN) * (elapsed_time / TIME_LIMIT), OUTER_RADIUS_MIN)
            
            # Check if the outer circle has shrunk to the minimum size and collapse the circle if needed
            if outer_radius == OUTER_RADIUS_MIN:
                player_hp -= 1  # Reduce player's HP when the circle collapses
                missed_circles += 1
                if player_hp <= 0:
                    game_over = True  # End the game
                    highest_combo = max(highest_combo, current_combo)
                    show_instructions = False  # Show game over message
                elif missed_circles >= PLAYER_INITIAL_HP:
                    game_over = True  # End the game if max misses are reached
                    highest_combo = max(highest_combo, current_combo)
                    show_instructions = False  # Show game over message
                if not game_over:
                    circle_x, circle_y = spawn_circle()  # Spawn new circle
                    start_time = time.time()  # Reset the timer

            screen.fill(WHITE)
            pygame.draw.circle(screen, BLUE, (circle_x, circle_y), outer_radius, 1)  # Draw the outer circle (outline only)
            pygame.draw.circle(screen, RED, (circle_x, circle_y), CIRCLE_RADIUS)  # Draw the inner circle
            pygame.draw.circle(screen, GREEN, (player_x, player_y), PLAYER_RADIUS)  # Draw the controllable circle
            draw_health_bar(screen, player_hp)  # Draw the player's health bar
            draw_combo(screen, current_combo)  # Draw the current combo
        elif game_over:
            screen.fill(WHITE)
            draw_game_over(screen, highest_combo)  # Show game over message with highest combo
        else:
            screen.fill(WHITE)
            draw_instructions(screen)  # Show instructions

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
