import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Bubble")

# Bubble properties
bubble_radius = 20
bubble_color = (255, 0, 0)
bubble_speed = 5

# Initial bubble position
bubble_x, bubble_y = screen_width // 2, screen_height // 2
bubble_dx, bubble_dy = 0, 0

# Flag to indicate if bubble should follow the mouse
follow_mouse = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            follow_mouse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            follow_mouse = False

    if follow_mouse:
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate direction towards the mouse
        bubble_dx = mouse_x - bubble_x
        bubble_dy = mouse_y - bubble_y

        # Normalize direction vector
        length = max(1, pygame.math.Vector2(bubble_dx, bubble_dy).length())
        bubble_dx /= length
        bubble_dy /= length

    # Update bubble position
    bubble_x += bubble_dx * bubble_speed
    bubble_y += bubble_dy * bubble_speed

    # Bounce off the screen edges
    if bubble_x < bubble_radius or bubble_x > screen_width - bubble_radius:
        bubble_dx *= -1
    if bubble_y < bubble_radius or bubble_y > screen_height - bubble_radius:
        bubble_dy *= -1

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the bubble
    pygame.draw.circle(screen, bubble_color, (int(bubble_x), int(bubble_y)), bubble_radius)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(60)
