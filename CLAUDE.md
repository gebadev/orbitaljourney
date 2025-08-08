# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple 2D orbital mechanics game built with Pyxel, a Python game engine. The game features a player that orbits around randomly generated planets in space.

## Dependencies

- **pyxel**: Python game development library for retro-style games
- Install with: `pip install pyxel`

## Running the Game

```bash
python orbit_game.py
```

## Code Architecture

### Core Classes

1. **Planet**: Represents celestial bodies with position (x,y), radius, and color
2. **Player**: Manages the orbiting entity with orbital mechanics (angle, angular velocity, orbit radius)  
3. **Game**: Main game controller handling initialization, planet generation, game loop (update/draw)

### Key Systems

- **Planet Generation**: Procedurally places 5-8 planets with collision avoidance (minimum 40px separation)
- **Orbital Mechanics**: Player follows circular orbit using trigonometric calculations (angle-based positioning)
- **Rendering**: Uses Pyxel's circle drawing functions for planets and orbit visualization

### Game Flow

1. Initialize 256x256 window
2. Generate random planets with collision detection
3. Spawn player orbiting a random planet
4. Run continuous update/draw loop

## Development Notes

- Game uses Pyxel's color palette (colors 0-15)
- Planet sizes range from 8-25 pixels radius
- Player orbit radius is planet radius + 20 pixels
- Angular velocity is fixed at 0.02 radians per frame