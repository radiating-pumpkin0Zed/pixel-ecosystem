import pygame
import random
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
grid[40][5] = (255,255,0)

clock = pygame.time.Clock()

def area_is_free(x,y,size):
    for i in range(size):
        for j in range(size):

            if x+i >= GRID_SIZE or y+j >= GRID_SIZE:
                return False

            if grid[x+i][y+j] != (0,0,0):
                return False
    return True

def generate_creature(word):
    
    size = max(3, len(word))

    for _ in range(50):
        spawn_x = random.randint(0, GRID_SIZE-10)
        spawn_y = random.randint(0, GRID_SIZE-10)

        if area_is_free(spawn_x, spawn_y, 5):
            break

    color_seed = sum(ord(c) for c in word)
    r = (color_seed * 3) % 256
    g = (color_seed * 7) % 256
    b = (color_seed * 11) % 256

    color = (r, g, b)

    #draw body
    for i in range(size):
        for j in range(size):
            grid[spawn_x+i][spawn_y+j] = color

    #draw eyes
    grid[spawn_x+1][spawn_y+1] = (0,0,0)
    grid[spawn_x+size-2][spawn_y+1] = (0,0,0)

    #random legs
    if random.random() > 0.5:
        grid[spawn_x+1][spawn_y+size] = color
        grid[spawn_x+size-2][spawn_y+size] = color

    if "x" in word:
        grid[spawn_x][spawn_y] = (255,255,255)
        grid[spawn_x+size-1][spawn_y] = (255,255,255)
    
    if "z" in word:
        grid[spawn_x + size//2][spawn_y + size + 1] = (255,255,255)
    
    if "m" in word:
        for i in range(3):
            grid[spawn_x+i+1][spawn_y+size] = color
            grid[spawn_x+size-i-2][spawn_y+size] = color
        
    if "o" in word:
        grid[spawn_x+1][spawn_y+1] = (0,0,0)
        grid[spawn_x+2][spawn_y+1] = (0,0,0)
        grid[spawn_x+size-3][spawn_y+1] = (0,0,0)
        grid[spawn_x+size-2][spawn_y+1] = (0,0,0)
    else:
        grid[spawn_x+1][spawn_y+1] = (0,0,0)
        grid[spawn_x+size-2][spawn_y+1] = (0,0,0)

typed_text = ""

while True:
    
    if pygame.mouse.get_pressed()[0]:

        mx, my = pygame.mouse.get_pos()

        grid_x = mx // PIXEL_SIZE
        grid_y = my // PIXEL_SIZE
        
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            grid[grid_x][grid_y] = (255,255,255)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            key = event.unicode

            if key.isalpha():
                typed_text += key

            if event.key == pygame.K_BACKSPACE:
                
                spawn_x -= 6
                if spawn_x < 5:
                    spawn_x = GRID_SIZE - 11
                    spawn_y -= 6
                
                if spawn_y < 5:
                    spawn_y = 5

                for i in range(5):
                    for j in range(5):
                        grid[spawn_x+i][spawn_y+j] = (0,0,0)

            if event.key == pygame.K_SPACE:
                generate_creature(typed_text)
                typed_text = ""

            if event.key == pygame.K_s:
                pygame.image.save(screen, "pixel_art.png")

    screen.fill((30,30,30))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            color = grid[x][y]

            pygame.draw.rect(
                    screen,
                    color,
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            )

            pygame.draw.rect(
                    screen,
                    (50,50,50),
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                    1
            )

    
    pygame.display.update()
    clock.tick(60)
