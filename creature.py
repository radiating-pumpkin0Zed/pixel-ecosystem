from utils import in_bounds

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

def clear_creature(creature, grid, GRID_SIZE):
    for pixel_x, pixel_y in get_creature_pixels(
        creature["x"],
        creature["y"],
        creature["size"],
        creature["shape"],
        creature["word"],
        creature["has_legs"]
    ):
        if in_bounds(pixel_x, pixel_y, GRID_SIZE):
            grid[pixel_x][pixel_y] = (0,0,0)

def draw_creature(creature, grid, GRID_SIZE):
    x = creature["x"]
    y = creature["y"]
    size = creature["size"]
    color = creature["color"]
    shape = creature["shape"]
    word = creature["word"]

    draw_creature_shape(x, y, color, shape, grid, GRID_SIZE)

    if creature["has_legs"]:
        if in_bounds(x+1, y+size, GRID_SIZE):
            grid[x+1][y+size] = color
        if in_bounds(x+size-2, y+size, GRID_SIZE):
            grid[x+size-2][y+size] = color

    if "x" in word:
        if in_bounds(x, y, GRID_SIZE):
            grid[x][y] = (255,255,255)
        if in_bounds(x+size-1, y, GRID_SIZE):
            grid[x+size-1][y] = (255,255,255)
    
    if "z" in word:
        if in_bounds(x + size//2, y + size + 1, GRID_SIZE):
            grid[x + size//2][y + size + 1] = (255,255,255)
    
    if "m" in word:
        for i in range(3):
            if in_bounds(x+i+1, y+size, GRID_SIZE):
                grid[x+i+1][y+size] = color
            if in_bounds(x+size-i-2, y+size, GRID_SIZE):
                grid[x+size-i-2][y+size] = color

    for frame_x, frame_y in get_eye_frame_positions(x, y, size, word):
        if in_bounds(frame_x, frame_y, GRID_SIZE):
            grid[frame_x][frame_y] = (255,255,255)

    #normal or predator
    if creature["is_predator"]:
        eye_color = (255, 0, 0)
    else:
        eye_color = (0,0,0)
        if creature["blink"] >= 110:
            eye_color = color

    for eye_x, eye_y in get_eye_positions(x, y, size, word):
        if in_bounds(eye_x, eye_y, GRID_SIZE):
            grid[eye_x][eye_y] = eye_color

def draw_creature_shape(x, y, color, shape, grid, GRID_SIZE):
    for i, j in shape:
        if in_bounds(x+i, y+j, GRID_SIZE):
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

def creature_area_is_free(x, y, size, shape, word, has_legs, grid, GRID_SIZE):
    for pixel_x, pixel_y in get_creature_pixels(x, y, size, shape, word, has_legs):
        if not in_bounds(pixel_x, pixel_y, GRID_SIZE):
            return False

        if grid[pixel_x][pixel_y] != (0,0,0):
            return False

    return True