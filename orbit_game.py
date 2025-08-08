import pyxel
import math
import random

class Planet:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        # Mass proportional to radius^3 (volume)
        self.mass = radius ** 3
        # Gravitational constant (scaled for game)
        self.G = 0.1
    
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

class Player:
    def __init__(self, planet, orbit_radius):
        self.planet = planet
        self.orbit_radius = orbit_radius
        self.angle = 0
        # Convert angular velocity to linear velocity
        self.velocity = 0.02 * orbit_radius
        self.base_velocity = 0.02 * orbit_radius
        self.acceleration = 0.1
        self.x = planet.x + orbit_radius * math.cos(self.angle)
        self.y = planet.y + orbit_radius * math.sin(self.angle)
        self.in_stable_orbit = True
        self.status_message = ""
        
        # Escape trajectory variables
        self.escaping = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.trail_points = []
        self.max_trail_length = 20
    
    def get_angular_velocity(self):
        """Convert linear velocity to angular velocity"""
        return self.velocity / self.orbit_radius
    
    def update(self, planets):
        # Add trail point for escape trajectory
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)
        
        if self.escaping:
            # Free flight physics
            if pyxel.btn(pyxel.KEY_UP):
                # Apply thrust in current direction
                thrust_magnitude = self.acceleration * 0.5
                direction_x = math.cos(self.angle)
                direction_y = math.sin(self.angle)
                self.velocity_x += direction_x * thrust_magnitude
                self.velocity_y += direction_y * thrust_magnitude
            elif pyxel.btn(pyxel.KEY_DOWN):
                # Apply reverse thrust
                thrust_magnitude = self.acceleration * 0.5
                direction_x = math.cos(self.angle)
                direction_y = math.sin(self.angle)
                self.velocity_x -= direction_x * thrust_magnitude
                self.velocity_y -= direction_y * thrust_magnitude
            
            # Apply gravitational forces from all planets
            for planet in planets:
                dx = planet.x - self.x
                dy = planet.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > planet.radius:  # Avoid division by zero
                    # Gravitational acceleration
                    g_accel = planet.G * planet.mass / (distance**2)
                    # Normalize direction
                    self.velocity_x += (dx / distance) * g_accel * 0.01
                    self.velocity_y += (dy / distance) * g_accel * 0.01
                    
                    # Check for re-capture
                    if distance < planet.radius + 50:  # Within capture range
                        capture_velocity = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
                        if planet.can_orbit(capture_velocity, distance):
                            self.planet = planet
                            self.orbit_radius = distance
                            self.velocity = capture_velocity
                            self.escaping = False
                            self.in_stable_orbit = True
                            self.status_message = "Captured by new planet!"
                            # Calculate new angle
                            self.angle = math.atan2(self.y - planet.y, self.x - planet.x)
                            break
            
            # Update position in free flight
            self.x += self.velocity_x
            self.y += self.velocity_y
            
            # Update angle based on velocity direction
            if self.velocity_x != 0 or self.velocity_y != 0:
                self.angle = math.atan2(self.velocity_y, self.velocity_x)
            
            # Check boundaries
            if self.x < 0 or self.x > 256 or self.y < 0 or self.y > 256:
                self.status_message = "Lost in space..."
            else:
                self.status_message = "Free flight in space"
                
        else:
            # Normal orbital mechanics
            if pyxel.btn(pyxel.KEY_UP):
                self.velocity += self.acceleration
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.velocity = max(self.velocity - self.acceleration, 0.1)
            
            # Check if current velocity allows stable orbit
            self.in_stable_orbit = self.planet.can_orbit(self.velocity, self.orbit_radius)
            
            if not self.in_stable_orbit:
                v1 = self.planet.get_first_cosmic_velocity(self.orbit_radius)
                v2 = self.planet.get_second_cosmic_velocity()
                
                if self.velocity < v1:
                    self.status_message = "Too slow! Crashing into planet!"
                    # Try to find a closer stable orbit or crash
                    self.handle_crash()
                elif self.velocity >= v2:
                    self.status_message = "Escape velocity reached! Leaving orbit!"
                    # Start escape sequence
                    self.start_escape()
            else:
                self.status_message = "Stable orbit"
            
            # Update orbital position
            angular_velocity = self.get_angular_velocity()
            self.angle += angular_velocity
            self.x = self.planet.x + self.orbit_radius * math.cos(self.angle)
            self.y = self.planet.y + self.orbit_radius * math.sin(self.angle)
    
    def handle_crash(self):
        """Handle velocity too low for orbit"""
        # Reduce orbit radius and adjust velocity
        new_orbit_radius = max(self.orbit_radius - 5, self.planet.radius + 10)
        if new_orbit_radius > self.planet.radius + 10:
            self.orbit_radius = new_orbit_radius
            # Adjust velocity for new orbit
            min_velocity = self.planet.get_first_cosmic_velocity(self.orbit_radius)
            if self.velocity < min_velocity:
                self.velocity = min_velocity * 1.1
    
    def start_escape(self):
        """Start escape trajectory from current orbit"""
        self.escaping = True
        self.in_stable_orbit = False
        
        # Convert orbital velocity to cartesian coordinates
        # Tangential velocity for circular orbit
        tangential_velocity = self.velocity
        velocity_angle = self.angle + math.pi/2  # Perpendicular to radius
        
        self.velocity_x = tangential_velocity * math.cos(velocity_angle)
        self.velocity_y = tangential_velocity * math.sin(velocity_angle)
        
        # Clear trail for fresh escape trajectory
        self.trail_points = []
    
    def handle_escape(self, planets):
        """Legacy method - now uses start_escape"""
        _ = planets  # Suppress unused parameter warning
        self.start_escape()

class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Orbital Journey")
        
        self.planets = []
        self.generate_planets()
        
        start_planet = random.choice(self.planets)
        self.player = Player(start_planet, start_planet.radius + 20)
        
        pyxel.run(self.update, self.draw)
    
    def generate_planets(self):
        num_planets = random.randint(5, 8)
        
        for _ in range(num_planets):
            attempts = 0
            while attempts < 50:
                x = random.randint(30, 226)
                y = random.randint(30, 226)
                radius = random.randint(8, 25)
                
                valid_position = True
                for planet in self.planets:
                    distance = math.sqrt((x - planet.x) ** 2 + (y - planet.y) ** 2)
                    if distance < radius + planet.radius + 40:
                        valid_position = False
                        break
                
                if valid_position:
                    color = random.choice([8, 9, 10, 11, 12, 13, 14, 15])
                    self.planets.append(Planet(x, y, radius, color))
                    break
                
                attempts += 1
    
    def update(self):
        self.player.update(self.planets)
    
    def draw(self):
        pyxel.cls(0)
        
        for planet in self.planets:
            pyxel.circ(planet.x, planet.y, planet.radius, planet.color)
        
        # Draw orbit path (different color based on stability)
        orbit_color = 3 if self.player.in_stable_orbit else 8
        pyxel.circb(self.player.planet.x, self.player.planet.y, 
                   self.player.orbit_radius, orbit_color)
        
        # Draw escape trail
        if self.player.escaping and len(self.player.trail_points) > 1:
            for i in range(len(self.player.trail_points) - 1):
                x1, y1 = self.player.trail_points[i]
                # Fade trail color based on age
                trail_color = max(1, 8 - (len(self.player.trail_points) - i) // 3)
                if 0 <= x1 < 256 and 0 <= y1 < 256:
                    pyxel.pset(int(x1), int(y1), trail_color)
        
        # Draw player
        if self.player.escaping:
            # Blinking effect when escaping
            player_color = 8 if pyxel.frame_count % 10 < 5 else 10
            # Draw direction indicator
            end_x = self.player.x + 10 * math.cos(self.player.angle)
            end_y = self.player.y + 10 * math.sin(self.player.angle)
            if 0 <= end_x < 256 and 0 <= end_y < 256:
                pyxel.line(int(self.player.x), int(self.player.y), int(end_x), int(end_y), 8)
        else:
            player_color = 7 if self.player.in_stable_orbit else 8
        
        pyxel.pset(int(self.player.x), int(self.player.y), player_color)
        
        # Display information
        if self.player.escaping:
            # Free flight information
            total_velocity = math.sqrt(self.player.velocity_x**2 + self.player.velocity_y**2)
            pyxel.text(5, 5, f"Velocity: {total_velocity:.2f}", 7)
            pyxel.text(5, 15, f"Vel X: {self.player.velocity_x:.2f}", 6)
            pyxel.text(5, 25, f"Vel Y: {self.player.velocity_y:.2f}", 6)
            pyxel.text(5, 35, f"Status: {self.player.status_message}", 8)
            pyxel.text(5, 45, f"Position: ({int(self.player.x)}, {int(self.player.y)})", 7)
        else:
            # Orbital information
            v1 = self.player.planet.get_first_cosmic_velocity(self.player.orbit_radius)
            v2 = self.player.planet.get_second_cosmic_velocity()
            
            pyxel.text(5, 5, f"Velocity: {self.player.velocity:.2f}", 7)
            pyxel.text(5, 15, f"Min orbit: {v1:.2f}", 6)
            pyxel.text(5, 25, f"Escape: {v2:.2f}", 8)
            pyxel.text(5, 35, f"Status: {self.player.status_message}", 7)
            pyxel.text(5, 45, f"Planet mass: {self.player.planet.mass}", 7)

if __name__ == "__main__":
    Game()