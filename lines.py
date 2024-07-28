import pygame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
r1 = 0
r2 = 7
s = 0.5
phi = 0.02
sc = 100
t = 0
t2 = 0
x0 = 0
y0 = 0
width = 800
height = 600

circles = []
circles_mapped = []
circles_d = []

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define circles
for i in np.arange(r1, r2 + s, s):
    a = []
    for j in np.arange(0, 2 * np.pi, phi):
        a.append([i * np.cos(j), i * np.sin(j)])
    circles.append(a)

# Define circles_mapped
def c_map(a):
    x, y = a
    return [np.sin(x) * np.sqrt(x ** 2 + y ** 2), np.cos(x) * np.sqrt(x ** 2 + y ** 2)]

for i in range(len(circles)):
    c = []
    for j in range(len(circles[i])):
        c.append(c_map(circles[i][j]))
    circles_mapped.append(c)

def define_d():
    global circles_d
    circles_d = []
    for i in range(len(circles)):
        a = []
        for j in range(len(circles[i])):
            x1, y1 = circles[i][j]
            x2, y2 = circles_mapped[i][j]
            a.append([(1 - t) * x1 + t * x2, (1 - t) * y1 + t * y2])
        circles_d.append(a)

def display_d():
    for i in range(len(circles_d)):
        for j in range(len(circles_d[i]) - 1):
            x1, y1 = circles_d[i][j]
            x2, y2 = circles_d[i][j + 1]
            pygame.draw.line(screen, (255, 255, 255), (width // 2 + sc * (x1 - x0), height // 2 - sc * (y1 - y0)), (width // 2 + sc * (x2 - x0), height // 2 - sc * (y2 - y0)), 2)

def show_grid():
    pygame.draw.line(screen, (255, 255, 255), (0, height // 2 + int(y0 * sc)), (width, height // 2 + int(y0 * sc)), 2)
    pygame.draw.line(screen, (255, 255, 255), (width // 2 - int(x0 * sc), 0), (width // 2 - int(x0 * sc), height), 2)

# Animation setup
fig = plt.figure()
ims = []

while True:
    screen.fill((0, 0, 0))
    t += 0.008
    if t > 1:
        t2 += 0.01
        t = 1
        if t2 > 0.5:
            t = 0
            t2 = 0

    define_d()
    display_d()
    show_grid()
    
    # Capture frame for animation
    frame = pygame.surfarray.array3d(screen)
    frame = np.transpose(frame, (1, 0, 2))
    ims.append([plt.imshow(frame, animated=True)])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                y0 += 10 / sc
            elif event.key == pygame.K_DOWN:
                y0 -= 10 / sc
            elif event.key == pygame.K_RIGHT:
                x0 += 10 / sc
            elif event.key == pygame.K_LEFT:
                x0 -= 10 / sc
            elif event.key == pygame.K_w:
                sc *= 1.1
            elif event.key == pygame.K_s:
                sc /= 1.1
            elif event.key == pygame.K_RETURN:
                sc = 100
                x0 = 0
                y0 = 0

    pygame.display.flip()
    clock.tick(30)

    if len(ims) >= 300:  # Limiting to 300 frames for the example
        break

# Save animation using matplotlib
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)
ani.save('animation.mp4', writer='ffmpeg')

pygame.quit()
