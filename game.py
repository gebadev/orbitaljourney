import pyxel
import random
import math
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from planet import Planet
from orbiter import Orbiter

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Orbital Journey")
        
        self.game_state = "title"  # "title", "playing", "game_over"
        self.planets = []
        self.orbiter = None
        self.game_over = False
        self.game_over_reason = ""
        self.stage = 1
        self.total_score = 0
        
        pyxel.run(self.update, self.draw)
    
    def generate_planets(self):
        gravity_types = ["weak", "medium", "strong"]
        
        # Generate 8-12 planets
        num_planets = random.randint(8, 12)
        
        for _ in range(num_planets):
            attempts = 0
            while attempts < 50:
                x = random.randint(40, SCREEN_WIDTH - 40)
                y = random.randint(40, SCREEN_HEIGHT - 40)
                gravity_type = random.choice(gravity_types)
                
                # Check if planet overlaps with existing planets
                valid_position = True
                for existing_planet in self.planets:
                    distance = math.sqrt((x - existing_planet.x)**2 + (y - existing_planet.y)**2)
                    if distance < 60:  # Minimum distance between planets
                        valid_position = False
                        break
                
                if valid_position:
                    self.planets.append(Planet(x, y, gravity_type))
                    break
                
                attempts += 1
    
    def start_game(self):
        self.game_state = "playing"
        self.planets = []
        self.generate_planets()
        
        # Start orbiter orbiting a random planet
        start_planet = random.choice(self.planets)
        self.orbiter = Orbiter(start_planet)
        
        self.game_over = False
        self.game_over_reason = ""
        self.stage = 1
        self.total_score = 0
    
    def next_stage(self):
        self.total_score += len(self.orbiter.visited_planets)
        self.stage += 1
        
        # Generate new planets for next stage
        self.planets = []
        self.generate_planets()
        
        # Start orbiter orbiting a random planet and reset visited planets
        start_planet = random.choice(self.planets)
        self.orbiter = Orbiter(start_planet)
    
    def restart(self):
        self.start_game()
    
    def update(self):
        if self.game_state == "title":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.start_game()
        
        elif self.game_state == "playing":
            # Handle input
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.orbiter.leave_orbit()
            
            # Update orbiter
            self.orbiter.update(self.planets)
            
            # Check for stage completion (all planets visited)
            if len(self.orbiter.visited_planets) == len(self.planets):
                self.next_stage()
            
            # Check game over conditions
            
            # Check collision with planets
            for planet in self.planets:
                distance = math.sqrt((self.orbiter.x - planet.x)**2 + (self.orbiter.y - planet.y)**2)
                if distance <= planet.radius:
                    self.game_over = True
                    self.game_over_reason = "Planet Collision!"
                    self.game_state = "game_over"
            
            # Check collision with screen boundaries
            if (self.orbiter.x <= 0 or self.orbiter.x >= SCREEN_WIDTH or 
                self.orbiter.y <= 0 or self.orbiter.y >= SCREEN_HEIGHT):
                self.game_over = True
                self.game_over_reason = "Screen Boundary!"
                self.game_state = "game_over"
        
        elif self.game_state == "game_over":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
    
    def draw(self):
        pyxel.cls(0)  # Clear screen with black
        
        if self.game_state == "title":
            # Title screen
            pyxel.text(SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 - 40, "ORBITAL JOURNEY", 11)
            pyxel.text(SCREEN_WIDTH//2 - 55, SCREEN_HEIGHT//2 - 20, "Navigate through space using", 7)
            pyxel.text(SCREEN_WIDTH//2 - 45, SCREEN_HEIGHT//2 - 10, "planetary gravity fields", 7)
            pyxel.text(SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 + 10, "Visit all planets to advance", 7)
            pyxel.text(SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//2 + 30, "Press SPACE to Start", 8)
        
        elif self.game_state == "playing":
            # Draw planets
            for planet in self.planets:
                is_visited = planet in self.orbiter.visited_planets
                planet.draw(is_visited)
            
            # Draw orbiter
            self.orbiter.draw()
            
            # Draw UI
            current_stage_score = len(self.orbiter.visited_planets)
            total_display_score = self.total_score + current_stage_score
            pyxel.text(5, 5, f"Score: {total_display_score}", 7)
            pyxel.text(5, 15, f"Stage: {self.stage}", 7)
            pyxel.text(5, 25, f"Planets: {current_stage_score}/{len(self.planets)}", 7)
            pyxel.text(5, 35, "Press SPACE to leave orbit", 6)
        
        elif self.game_state == "game_over":
            # Game over screen
            final_score = self.total_score + len(self.orbiter.visited_planets)
            pyxel.text(SCREEN_WIDTH//2 - 30, SCREEN_HEIGHT//2 - 20, "GAME OVER", 8)
            pyxel.text(SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//2 - 10, self.game_over_reason, 7)
            pyxel.text(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT//2, f"Score: {final_score}", 11)
            pyxel.text(SCREEN_WIDTH//2 - 25, SCREEN_HEIGHT//2 + 10, f"Stage: {self.stage}", 11)
            pyxel.text(SCREEN_WIDTH//2 - 40, SCREEN_HEIGHT//2 + 30, "Press SPACE to restart", 6)