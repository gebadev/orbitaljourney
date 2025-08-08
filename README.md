# Orbital Journey

A physics-based space exploration game where you navigate between planets using realistic orbital mechanics.

## Overview

Experience the thrill of space travel as you pilot a spacecraft through a solar system filled with planets of varying masses and gravitational fields. Master the delicate balance between orbital velocity and escape velocity to journey from planet to planet.

## Game Features

### Realistic Physics
- **Gravitational mechanics**: Each planet has mass proportional to its size
- **First cosmic velocity**: Minimum speed required for stable orbit
- **Second cosmic velocity**: Escape velocity to leave planetary orbit
- **Free flight physics**: Realistic space navigation between planets

### Gameplay Elements
- **Orbital mechanics**: Maintain stable orbits around planets
- **Velocity control**: Use arrow keys to accelerate/decelerate
- **Planet hopping**: Escape one planet's gravity to reach another
- **Visual feedback**: 
  - Trail effects during escape trajectories
  - Color-coded orbital stability indicators
  - Real-time velocity and orbital data display

### Controls
- **↑ Arrow Key**: Accelerate (increase orbital velocity or apply thrust)
- **↓ Arrow Key**: Decelerate (decrease orbital velocity or apply reverse thrust)

## How to Play

1. **Start in orbit**: Begin orbiting a random planet
2. **Monitor your speed**: 
   - Too slow = crash into planet
   - Perfect range = stable orbit
   - Too fast = escape to space
3. **Navigate space**: When escaping, use thrust to navigate toward other planets
4. **Get captured**: Approach other planets to enter their gravitational influence
5. **Repeat the journey**: Continue exploring the solar system

## Game States

### Stable Orbit
- Green orbit circle
- White player dot
- Safe orbital velocity range

### Crash Warning
- Red orbit circle
- Velocity below minimum orbital speed
- Automatic orbit adjustment to prevent crash

### Escape Trajectory
- Blinking player indicator
- Visible trail showing flight path
- Free flight through space with gravitational influences

### Re-capture
- Automatic orbital insertion when approaching planets
- New orbital parameters based on approach velocity

## Installation

### Requirements
- Python 3.6+
- Pyxel game engine

### Setup
```bash
pip install pyxel
```

### Run the Game
```bash
python orbit_game.py
```

## Educational Value

This game demonstrates key concepts in orbital mechanics:
- Conservation of energy and momentum
- Gravitational field strength vs. distance
- Circular vs. escape velocity calculations
- Multi-body gravitational systems
- Spacecraft trajectory planning

Perfect for students learning physics or anyone fascinated by space exploration!

## Technical Details

- Built with Python and Pyxel
- 256x256 pixel retro-style graphics
- Real-time physics simulation
- Procedural planet generation
- Dynamic gravitational field calculations

---

*Explore the cosmos, one orbit at a time.*