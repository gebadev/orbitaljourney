import math
import pyxel

class Player:
    def __init__(self, planet, orbit_radius):
        self.planet = planet
        self.orbit_radius = orbit_radius
        self.angle = 0
        
        # Calculate safe initial velocity between first and second cosmic velocities
        v1 = planet.get_first_cosmic_velocity(orbit_radius)  # Minimum orbital velocity
        v2 = planet.get_second_cosmic_velocity()  # Escape velocity
        
        # Set initial velocity to be stable (slightly above first cosmic velocity)
        self.velocity = v1 * 1.2  # 20% above minimum for stable orbit
        self.base_velocity = self.velocity
        self.acceleration = 0.02
        self.x = planet.x + orbit_radius * math.cos(self.angle)
        self.y = planet.y + orbit_radius * math.sin(self.angle)
        
        # Verify initial orbit is stable
        self.in_stable_orbit = planet.can_orbit(self.velocity, orbit_radius)
        if self.in_stable_orbit:
            self.status_message = "Stable orbit"
        else:
            # Fallback: ensure we have a stable orbit
            self.velocity = v1 * 1.1  # Reduce to 10% above minimum
            self.in_stable_orbit = True
            self.status_message = "Orbit stabilized"
        
        # Escape trajectory variables
        self.escaping = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.trail_points = []
        self.max_trail_length = 20
        self.escape_start_time = 0  # Track when escape started
        
        # Falling state
        self.falling = False
    
    def get_angular_velocity(self):
        """Convert linear velocity to angular velocity"""
        return self.velocity / self.orbit_radius
    
    def get_escape_time_seconds(self):
        """Get time elapsed since escape started in seconds"""
        if not self.escaping or self.escape_start_time == 0:
            return 0
        return (pyxel.frame_count - self.escape_start_time) / 30.0  # Assuming 30 FPS
    
    def update(self, planets):
        # Add trail point for escape trajectory
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)
        
        if self.escaping:
            # Free flight physics
            if pyxel.btn(pyxel.KEY_UP):
                # Apply thrust in current direction (reduced for better control)
                thrust_magnitude = self.acceleration * 0.3
                direction_x = math.cos(self.angle)
                direction_y = math.sin(self.angle)
                self.velocity_x += direction_x * thrust_magnitude
                self.velocity_y += direction_y * thrust_magnitude
            elif pyxel.btn(pyxel.KEY_DOWN):
                # Apply reverse thrust (reduced for better control)
                thrust_magnitude = self.acceleration * 0.3
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
                    # Gravitational acceleration (reduced for slower movement)
                    g_accel = planet.G * planet.mass / (distance**2)
                    # Normalize direction (reduced gravitational effect)
                    self.velocity_x += (dx / distance) * g_accel * 0.005
                    self.velocity_y += (dy / distance) * g_accel * 0.005
                    
                    # Check for re-capture
                    if distance < planet.radius + 50:  # Within capture range
                        capture_velocity = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
                        
                        # Get stable orbit parameters based on current velocity
                        orbit_radius, stable_velocity = planet.get_stable_capture_parameters(
                            capture_velocity, distance)
                        
                        # Check if we can establish a stable orbit
                        if planet.can_orbit(stable_velocity, orbit_radius):
                            self.planet = planet
                            self.orbit_radius = orbit_radius
                            self.velocity = stable_velocity
                            self.escaping = False
                            self.in_stable_orbit = True
                            self.status_message = f"Captured! New orbit at {orbit_radius:.1f}px"
                            # Reset escape timer when captured
                            self.escape_start_time = 0
                            # Calculate new angle based on current position
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
                self.velocity = max(self.velocity - self.acceleration, 0.05)
            
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
        # Check if we can reduce orbit radius to maintain orbit
        new_orbit_radius = max(self.orbit_radius - 5, self.planet.radius + 10)
        
        if new_orbit_radius <= self.planet.radius + 10:
            # Too close to planet - falling into planet
            self.falling = True
            self.status_message = "Falling into planet!"
            return
        
        # Try to adjust to lower orbit
        self.orbit_radius = new_orbit_radius
        min_velocity = self.planet.get_first_cosmic_velocity(self.orbit_radius)
        
        # If velocity is still too low even for the lowest orbit, fall
        if self.velocity < min_velocity * 0.8:  # Give some margin
            self.falling = True
            self.status_message = "Falling into planet!"
        else:
            # Adjust velocity for new orbit
            if self.velocity < min_velocity:
                self.velocity = min_velocity * 1.05
    
    def start_escape(self):
        """Start escape trajectory from current orbit"""
        self.escaping = True
        self.in_stable_orbit = False
        
        # Record escape start time
        self.escape_start_time = pyxel.frame_count
        
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