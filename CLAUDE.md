# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 2D orbital mechanics game built with Pyxel, a Python game engine. The game features realistic physics-based orbital mechanics where a player spacecraft navigates between planets using proper orbital dynamics.

## Dependencies

- **pyxel**: Python game development library for retro-style games
- Install with: `pip install pyxel`

## Running the Game

```bash
python main.py
```

## Code Architecture

### Core Classes (Modular Structure)

1. **Planet** (`planet.py`): 
   - Celestial bodies with position, radius, mass, color, and gravitational properties
   - Calculates first cosmic velocity (minimum orbital speed)
   - Calculates second cosmic velocity (escape velocity)
   - Determines orbital stability and capture parameters

2. **Player** (`player.py`): 
   - Spacecraft with orbital and escape trajectory physics
   - Handles orbital mechanics, escape sequences, and planetary re-capture
   - Manages falling/crashing states and escape timer
   - Velocity-based orbital calculations

3. **Game** (`game.py`): 
   - Main game controller with state management (title, playing, game_over)
   - Camera system following player or planet
   - Collision detection and game over conditions
   - UI rendering and user input handling

### Key Systems

- **Physics-Based Orbital Mechanics**: Real gravitational calculations using GM/r formulas
- **Camera System**: Smooth following camera centered on current planet or escaping player
- **Planet Generation**: 3-5 planets placed within screen bounds avoiding player orbit collision
- **State Management**: Title screen, gameplay, and game over states
- **Game Over Conditions**: 
  - Screen boundary collision
  - Planetary impact (speed too low)
  - 5-second escape timeout
- **Dynamic Orbit Capture**: Speed-based orbit radius calculation during planetary re-capture

### Game Flow

1. Display title screen with controls and instructions
2. Z/X key starts game initialization
3. Generate starting planet (center screen, medium size)
4. Generate additional planets avoiding player orbit
5. Initialize player with stable orbital velocity (v1 × 1.2)
6. Run state-based update/draw loop with camera following
7. Handle orbital mechanics, escape physics, and re-capture
8. Game over on boundary touch, crash, or timeout
9. R key restarts from title

## Development Notes

### Current Parameters
- Game window: 256×256 pixels
- Planet sizes: 3-12 pixel radius (reduced from original)
- Starting planet: 5-10 pixel radius, centered position
- Player orbit: planet radius + 20 pixels
- Player visual: 2-pixel radius circle (enlarged from 1-pixel dot)
- Gravitational constant: 0.02 (reduced for balanced gameplay)
- Initial velocity: First cosmic velocity × 1.2 (ensures stable orbit)
- Camera lerp speed: 0.1 (smooth following)
- Escape timeout: 5 seconds

### Physics Implementation
- Circular orbit formula: v = √(GM/r)
- Escape velocity: v = √(2GM/r)
- Orbital stability check: v1 ≤ velocity < v2
- Re-capture uses current escape velocity to determine new orbit radius
- Gravitational acceleration during escape: a = GM/r² × 0.005

### Visual Elements
- Orbit path: Green (stable) / Red (unstable) circle outline
- Player: White (stable) / Red (unstable) / Blinking (escaping)
- Trail: Fading dots during escape trajectory
- UI: Fixed-position velocity/status information
- Game over: Semi-transparent dithered overlay

### File Structure
```
orbit3/
├── main.py          # Entry point with game description
├── game.py          # Main game class with state management
├── player.py        # Player physics and mechanics
├── planet.py        # Planet properties and orbital calculations
├── CLAUDE.md        # This development guide
└── README.md        # User-facing game documentation
```