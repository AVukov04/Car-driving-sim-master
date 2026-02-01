# Car Driving Simulator

A simple 2D car driving simulation game built with Python and Pygame.

## Features

- Player-controlled car with keyboard controls
- NPC traffic vehicles
- Scrolling road environment
- Collision detection
- Camera system that follows the player

## Requirements

- Python 3.x
- Pygame

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
```

2. Install dependencies:
```bash
pip install pygame
```

## Running the Game

```bash
python main.py
```

## Project Structure

```
Car-driving-sim-master/
├── assets/           # Game images and sprites
├── game/             # Game logic modules
│   ├── car.py       # Player car class
│   ├── npc.py       # NPC car class
│   ├── road.py      # Road rendering
│   ├── world.py     # Game world
│   └── settings.py  # Game configuration
└── main.py          # Entry point
```

## Controls

Use keyboard controls (up/down/left/right) to drive the player car and avoid collisions with NPC vehicles/walls.
