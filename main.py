import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Click the Circles')

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Circle settings
CIRCLE_RADIUS = 30

def spawn_circle():
    x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)
    return x, y

def main():
    clock = pygame.time.Clock()
    circle_x, circle_y = spawn_circle()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2 <= CIRCLE_RADIUS ** 2:
                    circle_x, circle_y = spawn_circle()

        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, (circle_x, circle_y), CIRCLE_RADIUS)
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()