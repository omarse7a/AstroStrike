import pygame
from os import path
from bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # importing images
        spaceship_1 = pygame.image.load(path.join("graphics","spaceship","spaceship1.png")).convert_alpha()
        spaceship_2 = pygame.image.load(path.join("graphics","spaceship","spaceship2.png")).convert_alpha()

        self.frames = [spaceship_1, spaceship_2]
        self.index = 0
        self.image = self.frames[int(self.index)]
        self.rect = self.image.get_rect(midtop = (400, 500))    # putting the spaceship in the middle bottom of the screen

        self.bullets = pygame.sprite.Group()
        self.shoot_clicked = False

        self.laser_sound = pygame.mixer.Sound(path.join("audio","sfx_laser1.ogg"))   # laser sound effect
        self.laser_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < 800:
            self.rect.x += 6
        
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT] )and self.rect.left > 0:
            self.rect.x -= 6

        if keys[pygame.K_SPACE] and not self.shoot_clicked: # spacebar pressed
            self.bullets.add(Bullet(self.rect.center[0]))   # create a bullet sprite from the center of the spaceship
            self.shoot_clicked = True
            self.laser_sound.play()
        elif not keys[pygame.K_SPACE] and self.shoot_clicked:   # spacebar released
            self.shoot_clicked = False
            
    def player_animation(self): 
        # animating spaceship movement
        self.index += 0.05
        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]


    def update(self):
        # updating the sprite's frames
        self.player_input()
        self.player_animation()
