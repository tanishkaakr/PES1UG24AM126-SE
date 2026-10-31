"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28


import pygame

from game.target import Target
from game.hit_detection import check_hit

class GameEngine:
    def __init__(self, width=800, height=600,round_time=30.0):
        self.width = width
        self.height = height
        self.targets = []
        # Score and Combo tracking
        self.score = 0
        self.combo = 0
        self.base_points = 100
        self.round_time = round_time  # Total time in seconds
        
        self.reset_game()
        self.spawn_targets()

    def reset_game(self):
        """Resets all game parameters for a new round."""
        self.score = 0
        self.combo = 0
        self.base_points = 100
        self.time_remaining = self.round_time
        self.is_game_over = False
        
        self.targets = []
        self.spawn_targets()

    def spawn_targets(self):
        patterns = ["fast", "slow", "horizontal", "vertical"]
        for _ in range(5):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            pattern = random.choice(patterns)
            
            # Instantiate target with varying speeds/patterns
            self.targets.append(Target(x, y, radius=25, pattern=pattern, speed=3))

    def update(self,dt):
        """Update target positions every frame."""
        if self.is_game_over:
            return

        # Update timer
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.is_game_over = True
            return
        for target in self.targets:
            target.update(self.width, self.height)
        

    def handle_click(self, click_pos):
        """Check hit detection against moving targets."""
        """Processes clicks: updates score/combo on hit, resets combo on miss."""
        hit_detected = False

        # Iterate backward to hit top targets first
        for target in reversed(self.targets):
            if check_hit(click_pos, target):
                hit_detected = True
                self.targets.remove(target)
                
                # Increment combo multiplier
                self.combo += 1
                
                # Award points: Base Points * Current Combo Multiplier
                points_awarded = self.base_points * self.combo
                self.score += points_awarded
                
                print(f"HIT! Combo: {self.combo}x | +{points_awarded} pts | Total: {self.score}")
                break

        # Reset combo if click misses all targets
        if not hit_detected:
            self.combo = 0
            print("MISS! Combo reset.")

    def spawn_single_target(self):
        """Respawns a target when one is hit."""
        patterns = ["fast", "slow", "horizontal", "vertical"]
        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)
        pattern = random.choice(patterns)
        self.targets.append(Target(x, y, radius=25, pattern=pattern, speed=3))

    def draw(self, surface, font=None):
        surface.fill((30, 30, 30))
        for target in self.targets:
            target.draw(surface)
            
        # Optional: draw score or stats using font if provided
        if font:
            score_surface = font.render(f"Targets Left: {len(self.targets)}", True, (255, 255, 255))
            surface.blit(score_surface, (10, 10))
