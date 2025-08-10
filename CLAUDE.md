# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A 2D space exploration game built with Python and Pyxel where you control an orbiter using planetary gravity fields to visit planets across multiple stages. The game features stage progression, score tracking, and different gravity types.

## Dependencies

- **pyxel**: Python game development library (version 2.4.10)
- Install with: `pip install -r requirements.txt`

## Common Commands

### Running the Game
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

## Code Architecture

### Core Classes

1. **Planet** (`planet.py`): 
   - Celestial bodies with position, radius, gravity strength, and color
   - Three gravity types: weak (green), medium (yellow), strong (red)
   - Orbit radius determined by gravity strength

2. **Orbiter** (`orbiter.py`): 
   - Player orbiter that orbits planets and travels between them
   - Tracks visited planets for stage progression
   - Dynamic rotation direction based on approach angle
   - Handles orbital mechanics and free-flight physics

3. **Game** (`game.py`): 
   - Main game controller with state management
   - Stage progression system (advance when all planets visited)
   - Score tracking and collision detection
   - UI rendering and input handling

4. **Constants** (`constants.py`):
   - Screen dimensions and gravity strength values
   - ORBITAL_SPEED constant for easy game tuning

### Key Systems

- **Stage Progression**: Complete stages by visiting all planets
- **Gravity-Based Capture**: Orbiter captured when entering planet's orbit radius
- **Dynamic Rotation**: Orbital direction determined by approach velocity vector
- **Score System**: Points awarded only for visiting new planets
- **Visual Feedback**: Visited planets show as outlines, unvisited as filled

### Game Flow

1. Start with orbiter orbiting a random planet
2. Press SPACE to leave orbit and travel in straight line
3. Get captured by other planets' gravity fields
4. Visit all planets to advance to next stage
5. Game over on planet collision or screen boundary exit

## Development Notes

### Current Parameters
- Screen: 256×192 pixels (SCREEN_WIDTH × SCREEN_HEIGHT)
- Gravity strengths: 50 (weak), 80 (medium), 120 (strong)
- Orbital speed: 0.12 radians per frame (configurable via ORBITAL_SPEED in constants.py)
- Orbiter: 2-pixel radius white circle

### Physics Implementation
- Simple orbital mechanics: fixed radius circular orbits
- Velocity inheritance when leaving orbit based on orbital motion
- Cross product calculation determines rotation direction
- No complex gravitational physics - simplified arcade-style mechanics

### File Structure
```
orbitaljourney/
├── main.py          # Entry point
├── game.py          # Main game logic and state management
├── orbiter.py       # Orbiter physics and mechanics
├── planet.py        # Planet properties and rendering
├── constants.py     # Game configuration constants
├── requirements.txt # Python dependencies
├── sc01.png         # Game screenshot
└── README.md        # User documentation
```