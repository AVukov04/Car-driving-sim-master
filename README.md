# Car Driving Simulator

A small 2D top-down driving game built with Python and Pygame.

## Features

- Keyboard-controlled player car
- Four NPC traffic vehicles with different appearances and speeds
- Traffic vehicles use two lanes and respawn ahead of the player
- Collectible gold coins alternate between the two lanes
- Points counter in the HUD; each collected coin adds one point
- Collected and missed coins respawn farther ahead in the opposite lane
- Camera that follows the player
- Continuous scrolling road with lane markings
- Collision detection with traffic and both road edges
- Procedurally drawn roadside houses, trees, and guardrail details
- English HUD and Game Over screen
- Restart after a collision
- Frame-rate-independent movement using elapsed frame time

## Requirements

- Python 3.10 or newer recommended
- Pygame

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install Pygame:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```
```powershell
pip install pygame
```

## Run

From the project root:

```bash
python main.py
```

## Controls

- **Up Arrow** — accelerate
- **Down Arrow** — brake or reverse
- **Left / Right Arrows** — steer
- **R** — restart after a collision
- **Esc** — quit

## Project structure

```text
Car-Driving-Simulator/
├── assets/       # Vehicle sprites and image resources
├── game/
│   ├── coin.py   # Collectible coin rendering and respawning
│   ├── car.py    # Player movement and rendering
│   ├── npc.py    # NPC traffic movement and respawning
│   ├── road.py   # Road, scenery, and edge collision
│   ├── world.py  # World rendering coordinator
│   └── settings.py
└── main.py       # Main game loop, HUD, scoring, and collisions
```
