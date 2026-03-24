import pygame

def draw_menu(screen, WIDTH, MENU_WIDTH, HEIGHT, font, small_font, creatures, typed_text, paused):
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
        "",
        "=== TRAITS ===",
        "x = horns",
        "z = tail",
        "m = extra legs",
        "o = bigger eyes",
        "",
        f"Current text: [{typed_text}]"
    ]

    y = 52
    for line in lines:
        color = (220, 220, 220)

        if "===" in line:
            color = (255, 180, 80)
        elif "Predators" in line:
            color = (255, 80, 80)
        elif "Prey" in line:
            color = (80, 200, 120)
        elif "PAUSED" in line:
            color = (255, 220, 120)
        
        text = small_font.render(line, True, color)
        screen.blit(text, (WIDTH + 16, y))
        
        if line == "":
            y += 12
        else:
            y += 26