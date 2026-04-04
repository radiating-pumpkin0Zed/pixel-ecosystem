import pygame
import random
import sys
from creature import draw_creature, clear_creature, get_creature_pixels, creature_area_is_free
from generation import generate_creature
from ui import draw_menu

pygame.init()

WIDTH = 640
HEIGHT = 640
GRID_SIZE = 64
MENU_WIDTH = 260

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
typed_text = ""
paused = False
population_history = []
predator_history = []
prey_history = []
fruits = []
fruit_timer = 0

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

            if key and key.isalpha():
                typed_text += key

            if event.key == pygame.K_BACKSPACE:
                if creatures:
                    creature = creatures.pop()
                    clear_creature(creature, grid, GRID_SIZE)

            if event.key == pygame.K_SPACE:
                generate_creature(typed_text, grid, creatures, GRID_SIZE, creature_area_is_free, draw_creature)
                typed_text = ""

            if event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_CTRL:
                paused = not paused

            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.image.save(screen, "pixel_art.png")

            if event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                creatures.clear()
                population_history.clear()
                predator_history.clear()
                prey_history.clear()
                fruits.clear()
                grid = [[(0,0,0) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    screen.fill((30,30,30))

    if not paused:

        to_remove = set()

        for idx, creature in enumerate(creatures):

            if "hunger" not in creature:
                creature["hunger"] = 0

            if creature.get("spawn_effect", 0) > 0:
                creature["spawn_effect"] -= 1
                
            if creature["cooldown"] > 0:
                creature["cooldown"] -= 1

            #Age System
            creature["age"] += 1

            if creature["age"] > creature["max_age"]:
                clear_creature(creature, grid, GRID_SIZE)
                to_remove.add(idx)
                continue

            if creature.get("is_predator"):
                creature["hunger"] += 0.5

            if creature.get("is_predator") and creature["hunger"] > 600:
                clear_creature(creature, grid, GRID_SIZE)
                to_remove.add(idx)
                continue

            x = creature["x"]
            y = creature["y"]
            size = creature["size"]

            #clear old position
            clear_creature(creature, grid, GRID_SIZE)

            creature["blink"] += 1
            if creature["blink"] > 120:
                creature["blink"] = 0

            if creature.get("is_predator"):
                base_move = 0.06
            else:
                base_move = 0.02
            
            if creature.get("personality") == "aggressive":
                move_chance = base_move + 0.04
            elif creature.get("personality") == "lazy":
                move_chance = base_move - 0.01
            else:
                move_chance = base_move
            
            if random.random() < move_chance:
                dx, dy = 0, 0

                for other in creatures:
                    if other == creature:
                        continue
                        
                    dist_x = other["x"] - creature["x"]
                    dist_y = other["y"] - creature["y"]

                    distance = abs(dist_x) + abs(dist_y)

                    if distance < 8:

                        if creature.get("is_predator") and not other.get("is_predator"):
                            dx = 1 if dist_x > 0 else -1 if dist_x < 0 else 0
                            dy = 1 if dist_y > 0 else -1 if dist_y < 0 else 0
                            break

                        if not creature.get("is_predator") and other.get("is_predator"):
                            dx = -1 if dist_x > 0 else 1 if dist_x < 0 else 0
                            dy = -1 if dist_y > 0 else 1 if dist_y < 0 else 0
                            break

                if dx == 0 and dy == 0:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])

                new_x = creature["x"] + dx
                new_y = creature["y"] + dy

                if 0 <= new_x < GRID_SIZE - creature["size"] and 0 <= new_y < GRID_SIZE - creature["size"]:
                    creature["x"] = new_x
                    creature["y"] = new_y
                
                for fx, fy in fruits:
                    if abs(fx - creature["x"]) <= 1 and abs(fy - creature["y"]) <= 1:

                        fruits.remove((fx, fy))

                        # apply effect
                        if creature.get("is_predator"):
                            creature["hunger"] = max(0, creature["hunger"] - 200)
                        else:
                            creature["max_age"] += 300

                        break

            draw_creature(creature, grid, GRID_SIZE)

    new_creatures = []

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
    for i, j in collisions:

        if i in to_remove or j in to_remove:
            continue

        c1 = creatures[i]
        c2 = creatures[j]

        #Predator logic
        if c1.get("is_predator") and not c2.get("is_predator"):
            to_remove.add(j)
            c1["hunger"] = 0 #just ate
            continue
        if c2.get("is_predator") and not c1.get("is_predator"):
            to_remove.add(i)
            c2["hunger"] = 0
            continue

        if c1.get("is_predator") and c2.get("is_predator"):
            if random.random() < 0.5:
                to_remove.add(i)
            else:
                to_remove.add(j)
            continue

        if c1["cooldown"] > 0 or c2["cooldown"] > 0:
            continue
        
        new_word = c1["word"] + c2["word"]

        new_creatures.append(new_word)
        to_remove.add(i)
        to_remove.add(j)
    
    for idx in to_remove:
        clear_creature(creatures[idx], grid, GRID_SIZE)

    creatures = [c for idx, c in enumerate(creatures) if idx not in to_remove]

    fruit_timer += 1

    if fruit_timer > random.randint(100,120) and len(fruits) < 5:
        fx = random.randint(0, GRID_SIZE - 1)
        fy = random.randint(0, GRID_SIZE - 1)
        fruits.append((fx, fy))
        fruit_timer = 0

    predator_count = sum(1 for c in creatures if c.get("is_predator"))
    prey_count = len(creatures) - predator_count

    population_history.append(len(creatures))
    predator_history.append(predator_count)
    prey_history.append(prey_count)

    if len(population_history) > 100:
        population_history.pop(0)
        predator_history.pop(0)
        prey_history.pop(0)
    
    for word in new_creatures:
        generate_creature(
            word,
            grid,
            creatures,
            GRID_SIZE,
            creature_area_is_free,
            draw_creature
        )

        creatures[-1]["cooldown"] = 60

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            color = grid[x][y]

            if (x, y) in fruits:
                color = (255, 0, 255)

            pygame.draw.rect(
                    screen,
                    color,
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            )

            if (x,y) in fruits:
                pygame.draw.rect(
                    screen,
                    (255,255,255),
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                    1
                )


            pygame.draw.rect(
                    screen,
                    (50,50,50),
                    (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                    1
            )

    draw_menu(
        screen, WIDTH, MENU_WIDTH, HEIGHT,
        font, small_font,
        creatures, typed_text, paused,
        population_history, predator_history, prey_history,
        fruits)
    
    pygame.display.update()
    clock.tick(60)
