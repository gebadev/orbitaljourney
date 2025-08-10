#!/usr/bin/env python3
"""
Orbital Journey - A 2D orbital mechanics game built with Pyxel

Controls:
- UP Arrow: Increase orbital velocity / Apply forward thrust (when escaping)
- DOWN Arrow: Decrease orbital velocity / Apply reverse thrust (when escaping)
- R: Restart game (when game over)

Game Rules:
- Stay within the screen boundaries to avoid game over
- Use velocity to achieve stable orbits or escape planets
- Explore different planets by escaping and getting captured
"""

from game import Game

if __name__ == "__main__":
    Game()