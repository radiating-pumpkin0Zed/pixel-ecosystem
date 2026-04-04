import pygame

def draw_menu(screen, WIDTH, MENU_WIDTH, HEIGHT, font, small_font, creatures, typed_text, paused, population_history, predator_history, prey_history, fruits):
    pygame.draw.rect(screen, (25,25,30), (WIDTH, 0, MENU_WIDTH, HEIGHT))
    pygame.draw.line(screen, (70,70,70), (WIDTH, 0), (WIDTH, HEIGHT), 2)

    title = font.render("Pixel Ecosystem", True, (255,255,255))
    screen.blit(title, (WIDTH + 16, 16))

    predator_count = sum(1 for c in creatures if c["is_predator"])
    prey_count = len(creatures) - predator_count

    lines = []
    
    if paused:
        lines.append("⏸ PAUSED")
        lines.append("") 
    
    if predator_count > prey_count and predator_count > 0:
        lines.append("⚠ PREDATORS DOMINATING ⚠")
        lines.append("")

    lines += [
        "=== CONTROLS ===",
        "Type letters to build a name",
        "Press SPACE to spawn creature",
        "Click and drag to draw",
        "BACKSPACE removes last creature",
        "CTRL+S saves pixel_art.png",
        "CTRL+R to reset",
        "CTRL+P to pause",
        "",
        "=== STATS ===",
        f"Total creatures: {len(creatures)}",
        f"Predators: {predator_count}",
        f"Prey: {prey_count}",
        f"Helix Fruits: {len(fruits)}",
        "",
        "=== TRAITS ===",
        "x = horns",
        "z = tail",
        "m = extra legs",
        "o = bigger eyes",
        "",
        lines.insert(10, f"Current text: [{typed_text}]")
    ]

    y = 52

    for line in lines:
        if line is None:
            continue

        color = (220, 220, 220)

        if "===" in line:
            color = (255, 180, 80)
        elif line.startswith("Predators"):
            if predator_count > prey_count:
                color = (255, 40, 40)
            else:
                color = (255, 120, 120)
        elif line.startswith("Prey"):
            color = (80, 200, 120)
        elif "Helix Fruits" in line:
            color=(200, 100, 255)
        elif "⚠" in line:
            color = (255, 60, 60)
        elif "PAUSED" in line:
            color = (255, 220, 120)
        elif "Current text" in line:
            color = (120, 180, 255)
        
        text = small_font.render(line, True, color)
        screen.blit(text, (WIDTH + 16, y))

        if line == "":
            y += 12
            continue
        else:
            y += 26
    
    #GRAPH 
    graph_x = WIDTH + 16
    graph_y = y + 10
    graph_width = MENU_WIDTH - 32
    graph_height = 100

    pygame.draw.rect(screen, (40,40,50), (graph_x, graph_y, graph_width, graph_height))

    if len(population_history) > 1:
        max_pop = max(population_history)

        if max_pop > 0:

            points_total = []
            points_pred = []
            points_prey = []

            step = graph_width / max(1, len(population_history) - 1)
            
            for i in range(len(population_history)):

                x = int(graph_x + i * step)

                y_total = graph_y + graph_height - (population_history[i] / max_pop) * graph_height
                y_pred  = graph_y + graph_height - (predator_history[i] / max_pop) * graph_height
                y_prey  = graph_y + graph_height - (prey_history[i] / max_pop) * graph_height

                points_total.append((x, int(y_total)))
                points_pred.append((x, int(y_pred)))
                points_prey.append((x, int(y_prey)))

                if len(points_total) > 1:
                    pygame.draw.lines(screen, (100, 200, 255), False, points_total, 2)
                    pygame.draw.lines(screen, (255, 80, 80), False, points_pred, 2)
                    pygame.draw.lines(screen, (80, 200, 120), False, points_prey, 2)
                
                if len(points_prey) > 1:
                    filled = points_prey + [(points_prey[-1][0], graph_y + graph_height),
                                            (points_prey[0][0], graph_y + graph_height)]
                    pygame.draw.polygon(screen, (50, 120, 80), filled)


