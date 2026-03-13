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
grid[40][5] = (255,255,0)

clock = pygame.time.Clock()

cursor_x = 5
cursor_y = 5

def draw_h():
    global cursor_x, cursor_y

    for i in range(5):
        for j in range(5):
            grid[cursor_x+i][cursor_y+j] = (255,255,255)

def draw_e():
    global cursor_x, cursor_y

    grid[cursor_x+1][cursor_y+1] = (255,255,255)
    grid[cursor_x+3][cursor_y+1] = (255,255,255)

def draw_l():
    global cursor_x, cursor_y

    for j in range(5):
        grid[cursor_x+2][cursor_y+j] = (255,255,255)

def draw_o():
    global cursor_x, cursor_y

    for i in range(5):
        grid[cursor_x+i][cursor_y] = (255,255,255)
        grid[cursor_x+i][cursor_y+4] = (255,255,255)

    for j in range(5):
        grid[cursor_x][cursor_y+j] = (255,255,255)
        grid[cursor_x+4][cursor_y+j] = (255,255,255)

def move_cursor():
    global cursor_x, cursor_y

    cursor_x += 6

    if cursor_x + 5 >= GRID_SIZE:
        cursor_x = 5
        cursor_y += 6

    if cursor_y + 5 >= GRID_SIZE:
        cursor_x = 5
        cursor_y = 5

rules = {
    "h": draw_h,
    "e": draw_e,
    "l": draw_l,
    "o": draw_o
}

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
            print(key)

            if event.key == pygame.K_BACKSPACE:
                
                cursor_x -= 6
                if cursor_x < 5:
                    cursor_x = GRID_SIZE - 11
                    cursor_y -= 6
                
                if cursor_y < 5:
                    cursor_y = 5

                for i in range(5):
                    for j in range(5):
                        grid[cursor_x+i][cursor_y+j] = (0,0,0)


            if key in rules:
                rules[key]()
                move_cursor()

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
