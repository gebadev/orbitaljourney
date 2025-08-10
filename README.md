# Orbital Journey

A physics-based space exploration game where you navigate between planets using realistic orbital mechanics.

## Overview

Experience the thrill of space travel as you pilot a spacecraft through a solar system filled with planets of varying masses and gravitational fields. Master the delicate balance between orbital velocity and escape velocity to journey from planet to planet - but stay within the screen boundaries and don't take too long to find a new orbit!

## Game Features

### Realistic Physics
- **Gravitational mechanics**: Each planet has mass proportional to its volume (radius³)
- **First cosmic velocity**: Minimum speed required for stable orbit
- **Second cosmic velocity**: Escape velocity to leave planetary orbit
- **Dynamic orbit capture**: Your escape speed determines your new orbit size
- **Free flight physics**: Realistic space navigation with gravitational influences

### Gameplay Elements
- **Title screen**: Press Z or X to start your orbital journey
- **Orbital mechanics**: Maintain stable orbits around planets with precise velocity control
- **Velocity control**: Use arrow keys to accelerate/decelerate in orbit or during escape
- **Planet hopping**: Escape one planet's gravity to reach another
- **Time pressure**: Find a new orbit within 5 seconds or face game over
- **Boundary limits**: Stay within the screen boundaries to survive
- **Visual feedback**: 
  - Color-coded orbital stability indicators
  - Real-time velocity, orbital data, and countdown display
  - Trail effects during escape trajectories
  - Smooth camera following your spacecraft

### Controls
- **Title Screen**: Z or X to start game
- **↑ Arrow Key**: Accelerate (increase orbital velocity or apply forward thrust)
- **↓ Arrow Key**: Decelerate (decrease orbital velocity or apply reverse thrust)
- **Game Over Screen**: R to restart

## How to Play

1. **Title Screen**: Press Z or X to begin your orbital adventure
2. **Start in stable orbit**: Begin orbiting a planet with safe initial velocity
3. **Monitor your speed**: 
   - Too slow = crash into planet (Game Over!)
   - Perfect range = stable orbit (green circle)
   - Too fast = escape to space
4. **Navigate space**: When escaping, use thrust to navigate toward other planets
   - **Time limit**: You have 5 seconds to reach another planet's orbit
   - **Stay in bounds**: Don't let your spacecraft touch the screen edges
5. **Get captured**: Approach other planets to enter their gravitational influence
   - Your escape speed determines your new orbit size
   - Higher speeds = larger orbits, lower speeds = closer orbits
6. **Repeat the journey**: Continue exploring the solar system planet by planet

## Game Over Conditions

You'll face game over if:
- **Screen Boundary Contact**: Your spacecraft touches the screen edges
- **Planetary Crash**: Your velocity drops too low and you fall into a planet
- **Escape Timeout**: You spend more than 5 seconds in free space without finding an orbit

## Game States

### Stable Orbit
- **Green orbit circle** around your planet
- **White player circle** (2-pixel radius)
- Velocity within safe orbital range
- Planet-centered camera view

### Unstable Orbit Warning  
- **Red orbit circle** indicating danger
- Velocity approaching unsafe levels
- Risk of planetary crash

### Escape Trajectory
- **Blinking player indicator** during flight
- **Visible trail** showing your flight path
- **Player-following camera** during escape
- **Countdown timer** showing remaining time
- Free flight through space with gravitational influences from all planets

### Planetary Capture
- **Automatic orbital insertion** when approaching planets
- **Dynamic orbit calculation** based on your current escape velocity
- **Smooth transition** from escape to orbital flight

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
python main.py
```

## Educational Value

This game demonstrates key concepts in orbital mechanics:
- **Conservation of energy and momentum** in orbital systems
- **Gravitational field strength vs. distance** relationships
- **Circular vs. escape velocity** calculations and practical application
- **Multi-body gravitational systems** with realistic interactions
- **Spacecraft trajectory planning** and orbital maneuvering
- **Time-critical navigation** under physical constraints

Perfect for students learning physics, aspiring astronauts, or anyone fascinated by space exploration!

## Technical Details

### Game Engine
- Built with **Python** and **Pyxel** retro game engine
- **256×256 pixel** retro-style graphics
- **60 FPS** smooth gameplay with real-time physics

### Physics Simulation
- **Real gravitational calculations** using Newton's law of universal gravitation
- **Circular orbit mechanics** with proper velocity-radius relationships  
- **Multi-body gravitational influences** affecting escape trajectories
- **Dynamic orbital insertion** based on approach velocity and angle
- **Mass-based gravitational fields** (mass ∝ radius³)

### Game Features
- **Modular code architecture** with separated game logic
- **State-based game management** (Title → Playing → Game Over)
- **Smooth camera system** with interpolated following
- **Procedural planet generation** with collision avoidance
- **Physics-accurate orbital parameters** and velocity calculations
- **Visual feedback systems** for orbital stability and trajectory

### Performance Optimizations
- **Culling system** for off-screen object rendering
- **Efficient collision detection** for planetary boundaries
- **Optimized gravitational calculations** with reduced complexity for gameplay

---

🚀 *Master the art of orbital mechanics - Explore the cosmos, one orbit at a time!* 🌌