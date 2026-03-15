# Pixel Ecosystem

Originally this project started as a **pixel art generator**.

Three days later it accidentally turned into a **procedural creature ecosystem simulator**.

So here we are.

You type a word → a creature appears → it wanders around the grid blinking like a confused alien lifeform.

Basically: tiny pixel creatures generated from text.

---

## What It Does

- Turns **words into creatures**
- Creatures spawn on a **64x64 pixel grid**
- Each creature has:
  - a **unique color**
  - a **shape generated from the word**
  - **mutations based on letters**
- Creatures **blink**
- Creatures **wander randomly**
- Creatures **persist on the grid**

It's basically a **tiny pixel ecosystem sandbox**.

---

## Controls

| Key | Action |
|----|----|
| Type letters | Build a creature name |
| SPACE | Spawn creature |
| BACKSPACE | Remove last creature |
| CTRL + S | Save screenshot (`pixel_art.png`) |
| Mouse Drag | Draw pixels manually |

---

## Word Mutations

Some letters change how creatures look.

| Letter | Effect |
|------|------|
| `x` | Horns |
| `z` | Tail |
| `m` | Extra legs |
| `o` | Bigger eyes |

Example:

```
cat
```

Small creature.

```
zombie
```

Bigger creature with tail.

```
xenomorph
```

Now you're summoning monsters.

---

## How Creatures Work

Each creature stores data like this:

```
{
    x,
    y,
    size,
    color,
    word,
    shape,
    has_legs,
    blink
}
```

The simulation loop basically does this:

```
clear creature
update blink
maybe move
redraw creature
```

This happens **60 times per second**.

---

## Grid

The world is:

```
64 x 64 pixels
```

Each pixel is rendered as an **8×8 square** in the window.

Total window size:

```
512 x 512
```

Plus a **side menu with instructions**.

---

## Why This Exists

Mostly for fun and experimentation with:

- procedural generation
- simple simulation loops
- pygame rendering
- turning text into visuals

Also because small experiments tend to spiral into weird projects.

---

## Current Features

- Procedural creature generation
- Deterministic shapes from words
- Mutation traits
- Random wandering AI
- Blinking animation
- Creature deletion
- Manual pixel drawing
- Screenshot export
- Instruction menu UI

---

## Upcoming Features

Planned upgrades:

### Creature Evolution

When two creatures collide they will combine into a **new species**.

Example:

```
cat + zombie
→ catzombie
```

The new creature will inherit:

- combined color
- combined size
- combined word DNA

---

### Creature Library

A system to store species so you can spawn them again later.

Basically a **Pokédex for pixel monsters**.

---

### Population Control

Limit the number of creatures to avoid:

```
pixel overpopulation apocalypse
```

---

### Creature Stats

Possible additions:

- age
- generation
- speed
- mutation chance

---

## Running the Project

Install pygame:

```
pip install pygame
```

Run the program:

```
python main.py
```

Then start typing words and summoning creatures.

---

## Example Words to Try

```
cat
zombie
dragon
xenomorph
blobmonster
```

Some produce surprisingly weird creatures.

---

## Final Note

This project started as a **pixel art generator**.

It somehow turned into a **tiny artificial life simulator**.

Classic scope creep.
