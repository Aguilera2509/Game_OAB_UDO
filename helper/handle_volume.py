import pygame
from .draw_titles import Titles

class Volume:
    def __init__(self):
        self.volume = 4
        self.numbers_images = []

        self.__music_file = "src/music/audioOgg.ogg"

        self.image_up = pygame.image.load("src/music/img_up_and_down_vol/up.png").convert_alpha()
        self.image_down = pygame.image.load("src/music/img_up_and_down_vol/down.png").convert_alpha()
                
        self.title_volume = Titles(350, 280, "src/img_titles_background/volume.png")

        self.rect_right = self.image_up.get_rect()
        self.rect_right.topleft = (880, 290)

        self.rect_left = self.image_down.get_rect()
        self.rect_left.topleft = (700, 290)

        self.clicked = False

        pygame.mixer.music.load(self.__music_file)
        pygame.mixer.music.play(-1, 0.0)

        self.get_img_number()
        self.music()

    def get_img_number(self):
        for n in range(11):
            img = pygame.image.load(f"src/music/img_number_vol/{n}.png").convert_alpha()
            self.numbers_images.append(img)
        
    def handle_events(self):
        pos = pygame.mouse.get_pos()

        if self.rect_right.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.volume == 10: return

                self.volume += 1
                self.music()
        
        if self.rect_left.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                if self.volume == 0: return
                
                self.volume -= 1
                self.music()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def music(self):
        pygame.mixer.music.set_volume(self.volume/10)

    def draw(self, screen):
        screen.blit(self.image_down, self.rect_left)
        screen.blit(self.image_up, self.rect_right)

        img_actual = self.numbers_images[self.volume]
        self.title_volume.draw(screen)
        screen.blit(img_actual, (790, 290))