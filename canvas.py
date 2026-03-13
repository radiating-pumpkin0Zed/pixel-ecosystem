import pygame
import sys

pygame.init()

WIDTH = 512
HEIGHT = 512
GRID_SIZE = 64

PIXEL_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Art Generator")

#grid 
grid = [[(0,0,0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

#test

grid[10][10] = (255,0,0)
grid[20][20] = (0,255,0)
grid[30][30] = (0,0,255)

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30,30,30))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            color = grid[x][y]

            pygame.draw.rect(
                    screen,
                    color,
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            )

    pygame.display.update()
    clock.tick(60)
