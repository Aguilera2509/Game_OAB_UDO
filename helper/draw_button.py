import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, image_hover, value):
        super().__init__() #pygame.sprite.Sprite.__init__(self)
        self.original_source = image
        self.image_hover_source = image_hover
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.value = value

    def handle_events(self, event):
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(pos):
                self.image = pygame.image.load(self.image_hover_source).convert_alpha()
            else:
                self.image = pygame.image.load(self.original_source).convert_alpha()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return self.value

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return None