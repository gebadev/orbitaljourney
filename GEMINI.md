# GEMINI.md

## Project Overview

This project is a 2D space exploration game called "Orbital Journey," built with Python and the Pyxel game engine. The player controls an orbiter that travels between planets, using their gravitational fields to navigate. The goal is to visit all planets in a stage to advance to the next, accumulating a high score.

The game features realistic orbital mechanics, three levels of gravity for planets, and dynamic rotation of the orbiter based on its approach angle to a planet.

## Building and Running

To build and run this project, follow these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Game:**
    ```bash
    python main.py
    ```

## Development Conventions

*   **Game Logic:** The core game logic is encapsulated in the `Game` class in `game.py`.
*   **Game Objects:** The primary game objects are `Orbiter` (in `orbiter.py`) and `Planet` (in `planet.py`).
*   **Constants:** Game-wide constants, such as screen dimensions and gravity values, are stored in `constants.py`.
*   **Entry Point:** The main entry point for the application is `main.py`.
*   **Game State:** The game's state is managed within the `Game` class, transitioning between "title", "playing", and "game_over".
