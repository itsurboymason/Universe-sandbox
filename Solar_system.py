import pygame
import math
import sys
from dataclasses import dataclass
from typing import List, Tuple

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System - Universe Sandbox Style")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
LIGHT_GRAY = (211, 211, 211)

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

@dataclass
class CelestialBody:
    """Represents a celestial body in the solar system"""
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    color: Tuple[int, int, int]
    orbit_distance: float
    angle: float
    orbital_speed: float
    
    def update(self, dt: float):
        """Update position based on orbital mechanics"""
        self.angle += self.orbital_speed * dt
        if self.orbit_distance > 0:
            self.x = WIDTH // 2 + math.cos(self.angle) * self.orbit_distance
            self.y = HEIGHT // 2 + math.sin(self.angle) * self.orbit_distance
    
    def draw(self, surface: pygame.Surface):
        """Draw the celestial body and its orbit"""
        # Draw orbit path
        if self.orbit_distance > 0:
            pygame.draw.circle(surface, DARK_GRAY, (WIDTH // 2, HEIGHT // 2), 
                             int(self.orbit_distance), 1)
        
        # Draw the body
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 
                         int(self.radius))
        
        # Draw glow effect for stars and bright objects
        if self.name == "Sun":
            pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), 
                             int(self.radius) + 3, 1)
            pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), 
                             int(self.radius) + 6, 1)
        
        # Draw label
        label = small_font.render(self.name, True, WHITE)
        surface.blit(label, (int(self.x) + int(self.radius) + 5, 
                           int(self.y) - int(self.radius)))

def create_solar_system() -> List[CelestialBody]:
    """Create celestial bodies for the solar system"""
    bodies = [
        CelestialBody(
            name="Sun",
            mass=1.989e30,
            x=WIDTH // 2,
            y=HEIGHT // 2,
            vx=0,
            vy=0,
            radius=20,
            color=YELLOW,
            orbit_distance=0,
            angle=0,
            orbital_speed=0
        ),
        CelestialBody(
            name="Mercury",
            mass=3.285e23,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=4,
            color=GRAY,
            orbit_distance=80,
            angle=0,
            orbital_speed=0.04
        ),
        CelestialBody(
            name="Venus",
            mass=4.867e24,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=7,
            color=(255, 200, 100),
            orbit_distance=120,
            angle=2,
            orbital_speed=0.015
        ),
        CelestialBody(
            name="Earth",
            mass=5.972e24,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=8,
            color=LIGHT_BLUE,
            orbit_distance=170,
            angle=4,
            orbital_speed=0.01
        ),
        CelestialBody(
            name="Mars",
            mass=6.417e23,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=5,
            color=RED,
            orbit_distance=220,
            angle=1,
            orbital_speed=0.008
        ),
        CelestialBody(
            name="Jupiter",
            mass=1.898e27,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=14,
            color=ORANGE,
            orbit_distance=300,
            angle=3,
            orbital_speed=0.002
        ),
        CelestialBody(
            name="Saturn",
            mass=5.683e26,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=12,
            color=(210, 180, 140),
            orbit_distance=380,
            angle=5,
            orbital_speed=0.0009
        ),
        CelestialBody(
            name="Uranus",
            mass=8.681e25,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=9,
            color=(173, 216, 230),
            orbit_distance=450,
            angle=2,
            orbital_speed=0.0004
        ),
        CelestialBody(
            name="Neptune",
            mass=1.024e26,
            x=0,
            y=0,
            vx=0,
            vy=0,
            radius=9,
            color=(0, 0, 255),
            orbit_distance=500,
            angle=1,
            orbital_speed=0.0001
        ),
    ]
    return bodies

def main():
    """Main simulation loop"""
    clock = pygame.time.Clock()
    bodies = create_solar_system()
    paused = False
    show_info = True
    speed_multiplier = 1.0
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_i:
                    show_info = not show_info
                elif event.key == pygame.K_UP:
                    speed_multiplier = min(speed_multiplier + 0.5, 10.0)
                elif event.key == pygame.K_DOWN:
                    speed_multiplier = max(speed_multiplier - 0.5, 0.1)
                elif event.key == pygame.K_r:
                    bodies = create_solar_system()
                    paused = False
                    speed_multiplier = 1.0
        
        # Update bodies
        if not paused:
            for body in bodies:
                body.update(dt * speed_multiplier)
        
        # Draw
        screen.fill(BLACK)
        
        # Draw stars in background
        for i in range(100):
            star_x = (i * 127) % WIDTH
            star_y = (i * 311) % HEIGHT
            pygame.draw.circle(screen, LIGHT_GRAY, (star_x, star_y), 1)
        
        # Draw celestial bodies
        for body in bodies:
            body.draw(screen)
        
        # Draw UI
        if show_info:
            info_text = [
                "SPACE: Pause/Resume",
                "UP/DOWN: Speed Control",
                "I: Toggle Info",
                "R: Reset",
                f"Speed: {speed_multiplier:.1f}x",
                f"Status: {'PAUSED' if paused else 'RUNNING'}"
            ]
            
            for i, text in enumerate(info_text):
                surface = small_font.render(text, True, WHITE)
                screen.blit(surface, (10, 10 + i * 25))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
