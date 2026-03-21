import pygame

def draw_menu(screen, WIDTH, MENU_WIDTH, HEIGHT, font, small_font, creatures, typed_text):
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
        f"Creature count: {len(creatures)}",
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
