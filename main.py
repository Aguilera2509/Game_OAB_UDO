from enfocate import GameMetadata
import pygame
from game_logic import Game

if not pygame.get_init():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

game = Game()

if __name__ == "__main__":
    game.run_preview()
