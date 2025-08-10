import pyxel
import math
from constants import ORBITAL_SPEED

class Orbiter:
    def __init__(self, planet):
        self.orbiting_planet = planet
        self.angle = 0
        self.x = planet.x + planet.orbit_radius
        self.y = planet.y
        self.vx = 0
        self.vy = 0
        self.in_orbit = True
        self.visited_planets = {planet}
        self.rotation_direction = 1  # 1 for clockwise, -1 for counter-clockwise
    
    def update(self, planets):
        if self.in_orbit:
            self.angle += ORBITAL_SPEED * self.rotation_direction
            self.x = self.orbiting_planet.x + self.orbiting_planet.orbit_radius * math.cos(self.angle)
            self.y = self.orbiting_planet.y + self.orbiting_planet.orbit_radius * math.sin(self.angle)
        else:
            self.x += self.vx
            self.y += self.vy
            
            # Check for planet gravity capture
            for planet in planets:
                if planet != self.orbiting_planet:
                    distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
                    if distance <= planet.orbit_radius and distance > planet.radius:
                        self.enter_orbit(planet)
                        break
    
    def leave_orbit(self):
        if self.in_orbit:
            self.in_orbit = False
            # Calculate velocity based on orbital motion and rotation direction
            self.vx = -self.orbiting_planet.orbit_radius * math.sin(self.angle) * ORBITAL_SPEED * self.rotation_direction
            self.vy = self.orbiting_planet.orbit_radius * math.cos(self.angle) * ORBITAL_SPEED * self.rotation_direction
    
    def enter_orbit(self, planet):
        self.in_orbit = True
        self.orbiting_planet = planet
        
        # Only add to visited planets if it's a new planet
        if planet not in self.visited_planets:
            self.visited_planets.add(planet)
        
        # Calculate angle based on current position
        dx = self.x - planet.x
        dy = self.y - planet.y
        self.angle = math.atan2(dy, dx)
        
        # Determine rotation direction based on velocity and position
        # Calculate cross product to determine if planet is on left or right
        cross_product = self.vx * dy - self.vy * dx
        
        # If cross product is positive, planet is on the right (counter-clockwise rotation)
        # If cross product is negative, planet is on the left (clockwise rotation)
        self.rotation_direction = -1 if cross_product > 0 else 1
    
    def draw(self):
        pyxel.circ(self.x, self.y, 2, 7)  # White orbiter