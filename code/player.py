from typing import Any
import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        spaceship1 = pygame.image.load("graphics/spaceship/spaceship1.png").convert_alpha()
        spaceship2 = pygame.image.load("graphics/spaceship/spaceship2.png").convert_alpha()
        
        self.frames = [spaceship1, spaceship2]
        self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_rect(midbottom = (400, 570))

    