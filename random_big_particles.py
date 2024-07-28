import pygame
import numpy as np
import random
from moviepy.editor import VideoClip

# Constants
WIDTH, HEIGHT = 800, 800
X_SCALE = 100
Y_SCALE = 100
X_OFFSET = 0
Y_OFFSET = 0
MAX_LENGTH = 2000
K = 0.01  # Step size
PARTICLE_SIZE = 10  # Size of the particles
TRAIL_SIZE = 2  # Size of the trail

# Initialize variables
points = []
current_points = []
random_generation_mode = True
count = 0

# Velocity functions for circular motion
vx = "np.cos(t)"
vy = "np.sin(t)"

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
frames = []

def map_from_screen(l):
    sample_x, sample_y = l
    return [(sample_x - WIDTH / 2 - X_OFFSET) / X_SCALE, (HEIGHT / 2 - Y_OFFSET - sample_y) / Y_SCALE]

def map_to_screen(l):
    sample_x, sample_y = l
    return [WIDTH / 2 + X_OFFSET + X_SCALE * sample_x, HEIGHT / 2 - Y_OFFSET - Y_SCALE * sample_y]

def add_point(pt):
    if len(points) < MAX_LENGTH:
        points.append(pt)
        current_points.append(points[-1])

def draw():
    global current_points, vx, vy
    screen.fill((0, 0, 0))
    
    if random_generation_mode:
        if len(points) < MAX_LENGTH:
            px = random.randint(0, WIDTH)
            py = random.randint(0, HEIGHT)
            add_point(map_from_screen([px, py]))
    
    current_points_new = []
    for i, pt in enumerate(current_points):
        x, y = pt
        t = i / 20.0  # Adjust this value to change the speed of circular motion
        dx = eval(vx)
        dy = eval(vy)
        fx = x + K * dx
        fy = y + K * dy
        disp_i = map_to_screen([x, y])
        disp_f = map_to_screen([fx, fy])
        color = (int(255 * abs(np.sin(t))), int(255 * abs(np.cos(t))), 255 - int(255 * abs(np.sin(t))))
        pygame.draw.line(screen, color, disp_i, disp_f, TRAIL_SIZE)
        pygame.draw.circle(screen, color, disp_f, PARTICLE_SIZE)
        current_points_new.append([fx, fy])
    
    current_points = current_points_new
    frames.append(pygame.surfarray.array3d(screen))

def main():
    global vx, vy, count, random_generation_mode
    running = True
    while running:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    points.clear()
                    current_points.clear()
                    count += 1
                    if count == 1:
                        vx = "np.cos((x**2 + y**2)**0.5) - y"
                        vy = "min((x**2 + y**2)**0.5, np.sin(x))"
                    elif count == 2:
                        vx = "(x**2 + y**2)**0.5 * np.cos((x**2 + y**2)**0.5)"
                        vy = "(x**2 + y**2)**0.5 * np.sin((x**2 + y**2)**0.5)"
                elif event.key == pygame.K_SPACE:
                    random_generation_mode = not random_generation_mode
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

    # Save frames to video
    def make_frame(t):
        return frames[int(t * 30)]

    video = VideoClip(make_frame, duration=len(frames) / 30)
    video.write_videofile("simulation.mp4", fps=30)
