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
        self.rect = self.image.get_rect(midbottom = (400, 590))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < 800:
            self.rect.x += 5
        
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT] )and self.rect.left > 0:
            self.rect.x -= 5

    def player_animation(self):

        self.index += 0.04
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        
        self.player_input()
        self.player_animation()