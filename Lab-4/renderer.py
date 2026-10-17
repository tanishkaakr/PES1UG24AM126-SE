"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 25, 35)
COLOR_TEXT = (255, 255, 255)

# game/renderer.py


class Renderer:
    def __init__(self):
        # Default font fallbacks
        self.font_main = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_combo = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 22)

    def draw_hud(self, surface, score, combo,time_remaining):
        """
        Renders the Heads-Up Display (Score and Combo Multiplier).
        """
        # Render Score
        score_text = f"Score: {score:,}"
        score_surface = self.font_main.render(score_text, True, (255, 255, 255))
        surface.blit(score_surface, (20, 20))

        # Render Combo Multiplier (highlighted when active)
        if combo > 1:
            combo_color = (255, 215, 0)  # Gold highlight for active combos
            combo_text = f"Combo: {combo}x!"
        else:
            combo_color = (180, 180, 180)  # Dim gray for 0x / 1x
            combo_text = f"Combo: {combo}x"

        combo_surface = self.font_combo.render(combo_text, True, combo_color)
        surface.blit(combo_surface, (20, 50))

        # 3. Timer (Top Right)
        timer_color = (255, 80, 80) if time_remaining <= 5 else (255, 255, 255)
        timer_text = f"Time: {max(0.0, time_remaining):.1f}s"
        timer_surface = self.font_main.render(timer_text, True, timer_color)
        timer_rect = timer_surface.get_rect(topright=(surface.get_width() - 20, 20))
        surface.blit(timer_surface, timer_rect)

    def draw_game_over(self, surface, final_score):
        """Renders the game over overlay when time expires."""
        # Dark semi-transparent overlay
        overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2

        # Game Over Title
        title_surf = self.font_title.render("TIME'S UP!", True, (255, 65, 65))
        title_rect = title_surf.get_rect(center=(center_x, center_y - 60))
        surface.blit(title_surf, title_rect)

        # Final Score
        score_surf = self.font_main.render(f"Final Score: {final_score:,}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(center_x, center_y))
        surface.blit(score_surf, score_rect)

        # Restart Instruction
        restart_surf = self.font_sub.render("Press any key or click to Restart", True, (200, 200, 200))
        restart_rect = restart_surf.get_rect(center=(center_x, center_y + 60))
        surface.blit(restart_surf, restart_rect)


def draw_scene(surface, targets):
    surface.fill(COLOR_BG)
    for target in targets:
        pygame.draw.circle(surface, target.color, (int(target.x), int(target.y)), target.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(target.x), int(target.y)), target.radius, 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


