from typing import Any
import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, display_surf):

        super().__init__()
        spaceship1 = pygame.image.load("graphics/spaceship/spaceship1.png").convert_alpha()
        spaceship2 = pygame.image.load("graphics/spaceship/spaceship2.png").convert_alpha()
        
        self.screen = display_surf

        self.frames = [spaceship1, spaceship2]
        self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_rect(midtop = (400, 500))

        self.bullets = pygame.sprite.Group()
        self.shoot = False

    def player_input(self):
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < 800:
            self.rect.x += 5
        
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT] )and self.rect.left > 0:
            self.rect.x -= 5

        if keys[pygame.K_SPACE] and not self.shoot:
            self.shoot = True
        elif not keys[pygame.K_SPACE] and self.shoot:
            self.shoot = False
            self.bullets.add(Bullet(self.rect.center[0]))

        # for collisions
        ################

    def player_animation(self):

        self.index += 0.04
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        
        self.player_input()
        self.player_animation()
        self.bullets.draw(self.screen)
        self.bullets.update()

class Bullet(pygame.sprite.Sprite):

    def __init__(self, player_x):

        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/bullet.png"), (10, 25))
        self.rect = self.image.get_rect(midbottom = (player_x, 510))

    def move(self):

        if self.rect.top >= 0:
            self.rect.y -= 7
        else:
            self.kill()
    
    def update(self):

        self.move()
