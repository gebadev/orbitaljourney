import math
import random
import pyxel
from planet import Planet
from player import Player


class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Orbital Journey")

        # Camera system
        self.camera_x = 0
        self.camera_y = 0
        self.screen_width = 256
        self.screen_height = 256

        # Initialize variables
        self.planets = []
        self.player = None

        # Game state
        self.game_state = "title"  # "title", "playing", "game_over"
        self.game_over_message = ""

        pyxel.run(self.update, self.draw)

    def generate_start_planet(self):
        """Generate the starting planet for the player"""
        # Place starting planet near center of screen for better initial view
        x = random.randint(100, 156)  # More centered
        y = random.randint(100, 156)
        radius = random.randint(5, 10)  # Smaller size planet
        color = random.choice([8, 9, 10, 11, 12, 13, 14, 15])
        return Planet(x, y, radius, color)

    def generate_other_planets(self):
        """Generate other planets avoiding player's orbit"""
        num_planets = random.randint(3, 5)  # Reduced number for better fit

        # Keep all planets within initial screen bounds
        margin = 25  # Small margin from screen edges
        world_min_x = margin
        world_max_x = self.screen_width - margin
        world_min_y = margin
        world_max_y = self.screen_height - margin

        for _ in range(num_planets):
            attempts = 0
            while attempts < 100:  # More attempts for better placement
                x = random.randint(world_min_x, world_max_x)
                y = random.randint(world_min_y, world_max_y)
                radius = random.randint(3, 12)  # Smaller planets

                valid_position = True

                # Check collision with existing planets
                for planet in self.planets:
                    distance = math.sqrt((x - planet.x) ** 2 + (y - planet.y) ** 2)
                    if distance < radius + planet.radius + 25:  # Reduced spacing
                        valid_position = False
                        break

                # Check collision with player's orbit (only for starting planet)
                if valid_position and len(self.planets) > 0:  # Starting planet exists
                    start_planet = self.planets[0]  # Starting planet is first in list
                    player_orbit_radius = start_planet.radius + 20
                    distance_to_start = math.sqrt(
                        (x - start_planet.x) ** 2 + (y - start_planet.y) ** 2
                    )

                    # Ensure new planet doesn't interfere with player's orbit
                    min_safe_distance = (
                        player_orbit_radius + radius + 15
                    )  # Reduced safety margin
                    if distance_to_start < min_safe_distance:
                        valid_position = False

                if valid_position:
                    color = random.choice([8, 9, 10, 11, 12, 13, 14, 15])
                    self.planets.append(Planet(x, y, radius, color))
                    break

                attempts += 1

    def initialize_game(self):
        """Initialize planets and player for a new game"""
        self.planets = []

        # First generate the starting planet
        start_planet = self.generate_start_planet()
        self.planets.append(start_planet)
        self.player = Player(start_planet, start_planet.radius + 20)

        # Then generate other planets avoiding player's orbit
        self.generate_other_planets()

        # Initialize camera to center on player's planet
        self.camera_x = self.player.planet.x - self.screen_width // 2
        self.camera_y = self.player.planet.y - self.screen_height // 2

    def update(self):
        if self.game_state == "title":
            self.update_title()
        elif self.game_state == "playing":
            self.update_game()
        elif self.game_state == "game_over":
            self.update_game_over()

    def update_title(self):
        """Handle title screen updates"""
        # Check for Z or X key press (case insensitive)
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_X):
            self.initialize_game()
            self.game_state = "playing"

    def update_game(self):
        """Handle main game updates"""
        if self.player:
            self.player.update(self.planets)
            self.update_camera()
            self.check_game_over()

    def update_game_over(self):
        """Handle game over screen updates"""
        # Check for restart
        if pyxel.btnp(pyxel.KEY_R):
            self.restart_game()

    def update_camera(self):
        """Update camera to center on player's current planet"""
        if self.player.escaping:
            # When escaping, follow the player
            target_x = self.player.x - self.screen_width // 2
            target_y = self.player.y - self.screen_height // 2
        else:
            # When in orbit, center on the planet
            target_x = self.player.planet.x - self.screen_width // 2
            target_y = self.player.planet.y - self.screen_height // 2

        # Smooth camera following (lerp)
        camera_speed = 0.1
        self.camera_x += (target_x - self.camera_x) * camera_speed
        self.camera_y += (target_y - self.camera_y) * camera_speed

    def check_game_over(self):
        """Check if player touches screen boundary and trigger game over"""
        # Get player position in screen coordinates
        player_screen_x = self.player.x - self.camera_x
        player_screen_y = self.player.y - self.camera_y

        # Player circle radius is 2, check if it touches screen edges
        if (
            player_screen_x - 2 <= 0
            or player_screen_x + 2 >= self.screen_width
            or player_screen_y - 2 <= 0
            or player_screen_y + 2 >= self.screen_height
        ):
            self.game_state = "game_over"
            self.game_over_message = "GAME OVER - Player touched screen boundary!"
            return

        # Check if player has been escaping for more than 5 seconds
        if self.player.escaping and self.player.get_escape_time_seconds() >= 5.0:
            self.game_state = "game_over"
            self.game_over_message = "GAME OVER - Failed to orbit for 5 seconds!"
            return
        
        # Check if player is falling into planet
        if self.player.falling:
            self.game_state = "game_over"
            self.game_over_message = "GAME OVER - Crashed into planet!"

    def draw(self):
        pyxel.cls(0)

        if self.game_state == "title":
            self.draw_title()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def draw_title(self):
        """Draw title screen"""
        # Title
        pyxel.text(90, 60, "ORBITAL JOURNEY", 7)

        # Subtitle
        pyxel.text(70, 80, "2D Orbital Mechanics Game", 6)

        # Instructions
        pyxel.text(95, 120, "Controls:", 7)
        pyxel.text(60, 140, "UP/DOWN: Adjust orbital velocity", 6)
        pyxel.text(70, 150, "Stay within screen boundaries", 6)
        pyxel.text(65, 160, "Escape and orbit new planets!", 6)

        # Start prompt
        pyxel.text(80, 190, "Press Z or X to start", 8)

        # Blinking effect for start prompt
        if pyxel.frame_count % 60 < 30:
            pyxel.text(80, 190, "Press Z or X to start", 8)

    def draw_game(self):
        """Draw main game screen"""
        if not self.player:
            return

        # Draw planets with camera offset
        for planet in self.planets:
            screen_x = planet.x - self.camera_x
            screen_y = planet.y - self.camera_y
            # Only draw if visible on screen (with some margin for large planets)
            if (
                -50 <= screen_x <= self.screen_width + 50
                and -50 <= screen_y <= self.screen_height + 50
            ):
                pyxel.circ(screen_x, screen_y, planet.radius, planet.color)

        # Draw orbit path (different color based on stability) with camera offset
        if not self.player.escaping:
            orbit_color = 3 if self.player.in_stable_orbit else 8
            orbit_screen_x = self.player.planet.x - self.camera_x
            orbit_screen_y = self.player.planet.y - self.camera_y
            # Only draw orbit if visible
            if (
                -100 <= orbit_screen_x <= self.screen_width + 100
                and -100 <= orbit_screen_y <= self.screen_height + 100
            ):
                pyxel.circb(
                    orbit_screen_x,
                    orbit_screen_y,
                    self.player.orbit_radius,
                    orbit_color,
                )

        # Draw escape trail with camera offset
        if self.player.escaping and len(self.player.trail_points) > 1:
            for i in range(len(self.player.trail_points) - 1):
                x1, y1 = self.player.trail_points[i]
                screen_x1 = x1 - self.camera_x
                screen_y1 = y1 - self.camera_y
                # Fade trail color based on age
                trail_color = max(1, 8 - (len(self.player.trail_points) - i) // 3)
                if (
                    0 <= screen_x1 < self.screen_width
                    and 0 <= screen_y1 < self.screen_height
                ):
                    pyxel.pset(int(screen_x1), int(screen_y1), trail_color)

        # Draw player with camera offset
        player_screen_x = self.player.x - self.camera_x
        player_screen_y = self.player.y - self.camera_y

        if self.player.escaping:
            # Blinking effect when escaping
            player_color = 8 if pyxel.frame_count % 10 < 5 else 10
            # Draw direction indicator
            end_x = player_screen_x + 10 * math.cos(self.player.angle)
            end_y = player_screen_y + 10 * math.sin(self.player.angle)
            if 0 <= end_x < self.screen_width and 0 <= end_y < self.screen_height:
                pyxel.line(
                    int(player_screen_x),
                    int(player_screen_y),
                    int(end_x),
                    int(end_y),
                    8,
                )
        else:
            player_color = 7 if self.player.in_stable_orbit else 8

        pyxel.circ(int(player_screen_x), int(player_screen_y), 2, player_color)

        # Display information
        if self.player.escaping:
            # Free flight information
            total_velocity = math.sqrt(
                self.player.velocity_x**2 + self.player.velocity_y**2
            )
            escape_time = self.player.get_escape_time_seconds()
            time_remaining = max(0, 5.0 - escape_time)

            pyxel.text(5, 5, f"Velocity: {total_velocity:.2f}", 7)
            pyxel.text(5, 15, f"Vel X: {self.player.velocity_x:.2f}", 6)
            pyxel.text(5, 25, f"Vel Y: {self.player.velocity_y:.2f}", 6)
            pyxel.text(5, 35, f"Status: {self.player.status_message}", 8)
            pyxel.text(
                5,
                45,
                f"Time left: {time_remaining:.1f}s",
                8 if time_remaining < 2.0 else 7,
            )
            pyxel.text(
                5, 55, f"Position: ({int(self.player.x)}, {int(self.player.y)})", 7
            )
        else:
            # Orbital information
            v1 = self.player.planet.get_first_cosmic_velocity(self.player.orbit_radius)
            v2 = self.player.planet.get_second_cosmic_velocity()

            pyxel.text(5, 5, f"Velocity: {self.player.velocity:.2f}", 7)
            pyxel.text(5, 15, f"Min orbit: {v1:.2f}", 6)
            pyxel.text(5, 25, f"Escape: {v2:.2f}", 8)
            pyxel.text(5, 35, f"Status: {self.player.status_message}", 7)
            pyxel.text(5, 45, f"Planet mass: {self.player.planet.mass}", 7)

    def draw_game_over(self):
        """Draw game over screen"""
        # First draw the current game state as background
        if self.player:
            self.draw_game()

        # Draw semi-transparent overlay
        for y in range(80, 180):
            for x in range(20, 236):
                if (x + y) % 2 == 0:  # Dithering pattern
                    pyxel.pset(x, y, 1)

        # Draw game over message
        pyxel.text(70, 100, "GAME OVER", 8)
        if "boundary" in self.game_over_message:
            pyxel.text(40, 120, "Player touched boundary!", 7)
        elif "orbit" in self.game_over_message:
            pyxel.text(30, 120, "Failed to orbit for 5 seconds!", 7)
        elif "planet" in self.game_over_message:
            pyxel.text(45, 120, "Crashed into planet!", 7)
        else:
            pyxel.text(60, 120, "Game Over!", 7)
        pyxel.text(60, 140, "Press R to restart", 6)

    def restart_game(self):
        """Restart the game by reinitializing everything"""
        self.initialize_game()
        self.game_state = "playing"
        self.game_over_message = ""
