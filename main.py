from enfocate import GameMetadata
import pygame
from game_logic import Game

if not pygame.get_init():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

meta = GameMetadata(
        title = "Recuerdo de Luces",
        description= "Juego donde se tiene que memorizar un camino y recrearlo",
        authors= ["Aguilera Jose", "Materano Fabiana", "Betancourt Kerlyannes", "Figueroa Adrian"],
        group_number= 1
)

game = Game(meta)

if __name__ == "__main__":
    game.run_preview()
