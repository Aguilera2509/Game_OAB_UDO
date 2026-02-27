import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, image:str, image_hover:str, value:str):
        super().__init__() #pygame.sprite.Sprite.__init__(self)
        self.image_normal = pygame.image.load(image).convert_alpha()
        self.image_hover = pygame.image.load(image_hover).convert_alpha()
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.value = value
        self.clicked = False

    def handle_events(self, event):
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(pos):
                self.image = self.image_hover
            else:
                self.image = self.image_normal

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pos) and not self.clicked:
                    self.clicked = True
                    return self.value

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False

        return None