import pygame
import random
import sys

pygame.init()

WIDTH = 512
HEIGHT = 512
GRID_SIZE = 64
MENU_WIDTH = 220

PIXEL_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH + MENU_WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Ecosystem")
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 20)

#grid 
grid = [[(0,0,0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

#test

grid[10][10] = (255,0,0)
grid[20][20] = (0,255,0)
grid[30][30] = (0,0,255)
grid[40][5] = (255,255,0)

clock = pygame.time.Clock()

creatures = []

def in_bounds(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE

def area_is_free(x,y,size):
    for i in range(size):
        for j in range(size):

            if x+i >= GRID_SIZE or y+j >= GRID_SIZE:
                return False

            if grid[x+i][y+j] != (0,0,0):
                return False
    return True

def make_shape(word, size):
    shape_type = sum(ord(c) for c in word) % 4
    shape = []

    for i in range(size):
        for j in range(size):
            add_pixel = False

            if shape_type == 0:
                if j >= 1 and j < size-1:
                    add_pixel = True
                if i >= 1 and i < size-1 and j == size-1:
                    add_pixel = True
                if size >= 5 and j == 0 and i >= 2 and i < size-2:
                    add_pixel = True
            elif shape_type == 1:
                if i >= 1 and i < size-1 and j >= 1 and j < size-1:
                    add_pixel = True
                if j == 1 and i >= 1 and i < size-1:
                    add_pixel = True
                if j == size-2 and i >= 1 and i < size-1:
                    add_pixel = True
                if j == 0 and i >= 2 and i < size-2:
                    add_pixel = True
            elif shape_type == 2:
                if j >= 1 and j < size-1 and i >= 1 and i < size-1:
                    add_pixel = True
                if abs(i - size//2) <= 1:
                    add_pixel = True
                if j == size-2 and i >= 1 and i < size-1:
                    add_pixel = True
                if j == 0 and i == size//2:
                    add_pixel = True
            else:
                if i >= 1 and i < size-1 and j >= 1 and j < size-1:
                    add_pixel = True
                if j == 0 and i >= 1 and i < size-1:
                    add_pixel = True
                if j == size-1 and i >= 1 and i < size-1:
                    add_pixel = True
                if j == 1 and (i == 0 or i == size-1):
                    add_pixel = True

            if add_pixel:
                shape.append((i, j))

    return shape

def draw_creature_shape(x, y, color, shape):
    for i, j in shape:
        if in_bounds(x+i, y+j):
            grid[x+i][y+j] = color

def get_eye_positions(x, y, size, word):
    if "o" in word:
        return [
            (x+1, y+1),
            (x+2, y+1),
            (x+size-3, y+1),
            (x+size-2, y+1),
        ]

    return [
        (x+1, y+1),
        (x+size-2, y+1),
    ]

def get_eye_frame_positions(x, y, size, word):
    frame_pixels = []

    if "o" in word:
        left_eye = [(x+1, y+1), (x+2, y+1)]
        right_eye = [(x+size-3, y+1), (x+size-2, y+1)]

        for eye_pixels in [left_eye, right_eye]:
            min_x = min(pixel_x for pixel_x, _ in eye_pixels)
            max_x = max(pixel_x for pixel_x, _ in eye_pixels)
            eye_y = eye_pixels[0][1]

            for frame_x in range(min_x - 1, max_x + 2):
                frame_pixels.append((frame_x, eye_y - 1))
                frame_pixels.append((frame_x, eye_y + 1))

            frame_pixels.append((min_x - 1, eye_y))
            frame_pixels.append((max_x + 1, eye_y))
    else:
        for eye_x, eye_y in get_eye_positions(x, y, size, word):
            frame_pixels.append((eye_x - 1, eye_y))
            frame_pixels.append((eye_x + 1, eye_y))
            frame_pixels.append((eye_x, eye_y - 1))
            frame_pixels.append((eye_x, eye_y + 1))

    return frame_pixels

def get_creature_pixels(x, y, size, shape, word, has_legs):
    pixels = []

    for i, j in shape:
        pixels.append((x+i, y+j))

    if has_legs:
        pixels.append((x+1, y+size))
        pixels.append((x+size-2, y+size))

    if "x" in word:
        pixels.append((x, y))
        pixels.append((x+size-1, y))
    
    if "z" in word:
        pixels.append((x + size//2, y + size + 1))
    
    if "m" in word:
        for i in range(3):
            pixels.append((x+i+1, y+size))
            pixels.append((x+size-i-2, y+size))

    for eye_x, eye_y in get_eye_positions(x, y, size, word):
        pixels.append((eye_x, eye_y))

    for frame_x, frame_y in get_eye_frame_positions(x, y, size, word):
        pixels.append((frame_x, frame_y))

    return pixels

def creature_area_is_free(x, y, size, shape, word, has_legs):
    for pixel_x, pixel_y in get_creature_pixels(x, y, size, shape, word, has_legs):
        if not in_bounds(pixel_x, pixel_y):
            return False

        if grid[pixel_x][pixel_y] != (0,0,0):
            return False

    return True

def clear_creature(creature):
    for pixel_x, pixel_y in get_creature_pixels(
        creature["x"],
        creature["y"],
        creature["size"],
        creature["shape"],
        creature["word"],
        creature["has_legs"]
    ):
        if in_bounds(pixel_x, pixel_y):
            grid[pixel_x][pixel_y] = (0,0,0)

def draw_creature(creature):
    x = creature["x"]
    y = creature["y"]
    size = creature["size"]
    color = creature["color"]
    shape = creature["shape"]
    word = creature["word"]

    draw_creature_shape(x, y, color, shape)

    if creature["has_legs"]:
        if in_bounds(x+1, y+size):
            grid[x+1][y+size] = color
        if in_bounds(x+size-2, y+size):
            grid[x+size-2][y+size] = color

    if "x" in word:
        if in_bounds(x, y):
            grid[x][y] = (255,255,255)
        if in_bounds(x+size-1, y):
            grid[x+size-1][y] = (255,255,255)
    
    if "z" in word:
        if in_bounds(x + size//2, y + size + 1):
            grid[x + size//2][y + size + 1] = (255,255,255)
    
    if "m" in word:
        for i in range(3):
            if in_bounds(x+i+1, y+size):
                grid[x+i+1][y+size] = color
            if in_bounds(x+size-i-2, y+size):
                grid[x+size-i-2][y+size] = color

    for frame_x, frame_y in get_eye_frame_positions(x, y, size, word):
        if in_bounds(frame_x, frame_y):
            grid[frame_x][frame_y] = (255,255,255)

    eye_color = (0,0,0)
    if creature["blink"] >= 110:
        eye_color = color

    for eye_x, eye_y in get_eye_positions(x, y, size, word):
        if in_bounds(eye_x, eye_y):
            grid[eye_x][eye_y] = eye_color

def generate_creature(word):
    if word == "":
        return
    
    size = min(max(3, len(word)), GRID_SIZE - 2)
    shape = make_shape(word, size)
    has_legs = random.random() > 0.5
    spawn_x = None
    spawn_y = None

    for _ in range(50):
        test_x = random.randint(0, GRID_SIZE- size - 2)
        test_y = random.randint(0, GRID_SIZE- size - 2)

        if creature_area_is_free(test_x, test_y, size, shape, word, has_legs):
            spawn_x = test_x
            spawn_y = test_y
            break

    if spawn_x is None or spawn_y is None:
        return

    color_seed = sum(ord(c) for c in word)
    r = (color_seed * 3) % 256
    g = (color_seed * 7) % 256
    b = (color_seed * 11) % 256

    color = (r, g, b)

    creature = {
        "x": spawn_x,
        "y": spawn_y,
        "size": size,
        "color": color,
        "word": word,
        "shape": shape,
        "has_legs": has_legs,
        "blink": 0
    }

    draw_creature(creature)
    creatures.append(creature)

def draw_menu():
    pygame.draw.rect(screen, (18,18,18), (WIDTH, 0, MENU_WIDTH, HEIGHT))
    pygame.draw.line(screen, (70,70,70), (WIDTH, 0), (WIDTH, HEIGHT), 2)

    title = font.render("Instructions", True, (255,255,255))
    screen.blit(title, (WIDTH + 16, 16))

    lines = [
        "Type letters to build a name",
        "Press SPACE to spawn creature",
        "Click and drag to draw",
        "BACKSPACE removes last creature",
        "CTRL+S saves pixel_art.png",
        "",
        "Creature count: " + str(len(creatures)),
        "",
        "Creature words change:",
        "x = horns",
        "z = tail",
        "m = extra legs",
        "o = bigger eyes",
        "",
        "Current text: " + typed_text,
    ]

    y = 52
    for line in lines:
        text = small_font.render(line, True, (220,220,220))
        screen.blit(text, (WIDTH + 16, y))
        y += 24

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
                
                if creatures:
                    creature = creatures.pop()
                    clear_creature(creature)

            if event.key == pygame.K_SPACE:
                generate_creature(typed_text)
                typed_text = ""

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.image.save(screen, "pixel_art.png")

    screen.fill((30,30,30))

    for creature in creatures:
            
        x = creature["x"]
        y = creature["y"]
        size = creature["size"]

        #clear old position
        clear_creature(creature)

        creature["blink"] += 1
        if creature["blink"] > 120:
            creature["blink"] = 0

        if random.random() < 0.02:
            dx = random.choice([-1,0,1])
            dy = random.choice([-1,0,1])
   
            new_x = creature["x"] + dx
            new_y = creature["y"] + dy

            if 0 <= new_x < GRID_SIZE - creature["size"] and 0 <= new_y < GRID_SIZE - creature["size"]:
                creature["x"] = new_x
                creature["y"] = new_y

        draw_creature(creature)

    new_creatures = []
    to_remove = set()
    
    # Collision detection ----
    collisions = []

    for i in range(len(creatures)):
        for j in range(i+1, len(creatures)):

            c1 = creatures[i]
            c2 = creatures[j]

            pixels1 = set(get_creature_pixels(
                c1["x"], c1["y"], c1["size"],
                c1["shape"], c1["word"], c1["has_legs"]
            ))

            pixels2 = set(get_creature_pixels(
                c2["x"], c2["y"], c2["size"],
                c2["shape"], c2["word"], c2["has_legs"]
            ))

            if pixels1 & pixels2:
                collisions.append((i,j))
    
    # Handle collisions
    to_remove = set()
    for i, j in collisions:
        if i in to_remove or j in to_remove:
            continue
        c1 = creatures[i]
        c2 = creatures[j]
        new_word = c1["word"] + c2["word"]

        new_creatures.append(new_word)
        to_remove.add(i)
        to_remove.add(j)
    
    creatures = [c for idx, c in enumerate(creatures) if idx not in to_remove]

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

    draw_menu()
    
    pygame.display.update()
    clock.tick(60)
