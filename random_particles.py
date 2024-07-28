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
K = 0.001 * 10

# Initialize variables
points = []
current_points = []
random_generation_mode = True
count = 0

# Velocity functions
vx = "np.cos((x**2 + y**2)**0.5)"
vy = "np.sin((x**2 + y**2)**0.5)"

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
frames = []

def map_from_screen(l):
    sample_x, sample_y = l
    return [(sample_x - WIDTH/2 - X_OFFSET) / X_SCALE, (HEIGHT/2 - Y_OFFSET - sample_y) / Y_SCALE]

def map_to_screen(l):
    sample_x, sample_y = l
    return [WIDTH/2 + X_OFFSET + X_SCALE * sample_x, HEIGHT/2 - Y_OFFSET - Y_SCALE * sample_y]

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
    for pt in current_points:
        x, y = pt
        dx = eval(vx)
        dy = eval(vy)
        magnitude = (dx**2 + dy**2)**0.5
        nx = dx / magnitude
        ny = dy / magnitude
        fx = x + K * nx
        fy = y + K * ny
        disp_i = map_to_screen([x, y])
        disp_f = map_to_screen([fx, fy])
        color = (255 - int(255 * magnitude / 4), 255, 255)
        pygame.draw.line(screen, color, disp_i, disp_f)
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

    video = VideoClip(make_frame, duration=len(frames)/30)
    video.write_videofile("simulation.mp4", fps=60)
