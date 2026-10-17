"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame
import random

class Target:
    def __init__(self, x, y, radius=20, pattern="linear", speed=3):
        """
        :param x: Initial center X position
        :param y: Initial center Y position
        :param radius: Target radius
        :param pattern: Movement pattern ('fast', 'slow', 'zigzag', 'horizontal', 'vertical')
        :param speed: Base movement speed multiplier
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.pattern = pattern
        
        # Configure initial velocity components based on pattern
        if pattern == "fast":
            self.vx = random.choice([-1, 1]) * speed * 2
            self.vy = random.choice([-1, 1]) * speed * 2
        elif pattern == "slow":
            self.vx = random.choice([-1, 1]) * speed * 0.75
            self.vy = random.choice([-1, 1]) * speed * 0.75
        elif pattern == "horizontal":
            self.vx = random.choice([-1, 1]) * speed * 1.5
            self.vy = 0
        elif pattern == "vertical":
            self.vx = 0
            self.vy = random.choice([-1, 1]) * speed * 1.5
        else:  # Default balanced linear movement
            self.vx = random.choice([-1, 1]) * speed
            self.vy = random.choice([-1, 1]) * speed

    def update(self, screen_width, screen_height):
        """Updates position and handles bouncing off screen boundaries."""
        self.x += self.vx
        self.y += self.vy

        # Horizontal boundary bounce (account for target radius)
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.vx *= -1

        # Vertical boundary bounce (account for target radius)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.vy *= -1

    def draw(self, surface):
        """Draws the target at its current (x, y) center position."""
        import pygame
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
