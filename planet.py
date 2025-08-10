import pyxel
from constants import GRAVITY_WEAK, GRAVITY_MEDIUM, GRAVITY_STRONG

class Planet:
    def __init__(self, x, y, gravity_type):
        self.x = x
        self.y = y
        self.gravity_type = gravity_type
        self.radius = 8
        
        if gravity_type == "weak":
            self.gravity = GRAVITY_WEAK
            self.color = 3  # Green
            self.orbit_radius = 25
        elif gravity_type == "medium":
            self.gravity = GRAVITY_MEDIUM
            self.color = 10  # Yellow
            self.orbit_radius = 20
        else:  # strong
            self.gravity = GRAVITY_STRONG
            self.color = 8  # Red
            self.orbit_radius = 15
    
    def draw(self, is_visited=False):
        if is_visited:
            pyxel.circb(self.x, self.y, self.radius, self.color)
        else:
            pyxel.circ(self.x, self.y, self.radius, self.color)
        pyxel.circb(self.x, self.y, self.orbit_radius, 1)  # Orbit line