import random

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

def generate_creature(word, grid, creatures, GRID_SIZE, creature_area_is_free, draw_creature):
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

        if creature_area_is_free(test_x, test_y, size, shape, word, has_legs, grid, GRID_SIZE):
            spawn_x = test_x
            spawn_y = test_y
            break

    if spawn_x is None or spawn_y is None:
        spawn_x = random.randint(0, GRID_SIZE - size - 1)
        spawn_y = random.randint(0, GRID_SIZE - size - 1)

    color_seed = sum(ord(c) for c in word)
    r = (color_seed * 3) % 256
    g = (color_seed * 7) % 256
    b = (color_seed * 11) % 256

    color = (r, g, b)

    is_predator = random.random() < 0.1

    creature = {
        "x": spawn_x,
        "y": spawn_y,
        "size": size,
        "color": color,
        "word": word,
        "shape": shape,
        "has_legs": has_legs,
        "blink": 0,
        "cooldown": 0,
        "age": 0,
        "max_age": random.randint(1000, 2000),
        "hunger": -100,
        "is_predator": is_predator,
        "spawn_effect": 10 if is_predator else 0,
    }

    draw_creature(creature, grid, GRID_SIZE)
    creatures.append(creature)