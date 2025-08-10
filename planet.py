import math

class Planet:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # Mass proportional to radius^3 (volume)
        self.mass = radius ** 3
        # Gravitational constant (scaled for game - reduced for slower speeds)
        self.G = 0.02
    
    def get_first_cosmic_velocity(self, orbit_radius):
        """Calculate minimum orbital velocity (circular orbit)"""
        return math.sqrt(self.G * self.mass / orbit_radius)
    
    def get_second_cosmic_velocity(self):
        """Calculate escape velocity from planet surface"""
        return math.sqrt(2 * self.G * self.mass / self.radius)
    
    def can_orbit(self, velocity, orbit_radius):
        """Check if velocity allows stable orbit"""
        v1 = self.get_first_cosmic_velocity(orbit_radius)
        v2 = self.get_second_cosmic_velocity()
        return v1 <= velocity < v2
    
    def get_orbit_radius_for_velocity(self, velocity):
        """Calculate stable orbit radius for given velocity"""
        # From circular orbit formula: v = sqrt(GM/r)
        # Therefore: r = GM/v^2
        if velocity <= 0:
            return None
        
        orbit_radius = (self.G * self.mass) / (velocity ** 2)
        
        # Ensure orbit is above planet surface
        min_orbit_radius = self.radius + 10  # Minimum safe distance
        return max(orbit_radius, min_orbit_radius)
    
    def get_stable_capture_parameters(self, velocity, current_distance):
        """Get stable orbit parameters for capture at given velocity and distance"""
        # Calculate ideal orbit radius for the velocity
        ideal_radius = self.get_orbit_radius_for_velocity(velocity)
        
        # Use current distance if it's reasonable, otherwise use ideal radius
        if current_distance >= self.radius + 10:
            capture_radius = current_distance
        else:
            capture_radius = ideal_radius
        
        # Calculate required velocity for this orbit radius
        required_velocity = self.get_first_cosmic_velocity(capture_radius)
        
        # Use the higher of current velocity or required velocity for stability
        stable_velocity = max(velocity, required_velocity * 1.05)  # 5% safety margin
        
        return capture_radius, stable_velocity