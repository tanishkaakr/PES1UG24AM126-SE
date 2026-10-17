"""
Target Shooting (Lab Starter)

Run with:  python3 main.py

Click on targets to hit them.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE
from game.renderer import Renderer

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Target Shooting")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine(width=800, height=600, round_time=30.0)
    renderer = Renderer()
    running = True

    while running:
        # Calculate delta time in seconds
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if engine.is_game_over:
                    engine.reset_game()  # Restart on any key press
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if engine.is_game_over:
                        engine.reset_game()  # Restart on click
                    else:
                        engine.handle_click(event.pos)

        # Update game logic
        engine.update(dt)

        # Draw main game layer
        engine.draw(screen)
        renderer.draw_hud(screen, engine.score, engine.combo, engine.time_remaining)

        # Render overlay if round ended
        if engine.is_game_over:
            renderer.draw_game_over(screen, engine.score)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
