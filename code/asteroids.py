from typing import Any
import pygame
from random import choice, randint

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, speed):
        super().__init__()
        self.speed = speed

    def update_speed(self, speed):
        self.speed = speed

    def move(self):
        if self.rect.top <= 800:    # moving down while the astro is inside the display screen 
            self.rect.y += self.speed    
        else:                   # destroying the sprite when it goes outside the screen
            self.kill()

    def update(self, speed):
        # updating the sprite's frames
        self.update_speed(speed)
        self.move()

class Big_Asteriod(Asteroid):

    def __init__(self, speed):
        super().__init__(speed)
        # importing images
        big_astro_1 = pygame.image.load("graphics/asteroids/astroBig1.png").convert_alpha()
        big_astro_2 = pygame.image.load("graphics/asteroids/astroBig2.png").convert_alpha()
        big_astro_3 = pygame.image.load("graphics/asteroids/astroBig3.png").convert_alpha()
        
        self.image = choice([big_astro_1,big_astro_2,big_astro_3])  # displaying astro image randomly
        # positioning the astro above the display screen in random x pos inside the screen borders
        self.rect = self.image.get_rect(midbottom = (randint(self.image.get_width(), 800-self.image.get_width()), -100))
        self.destructible = False  

class Small_Asteriod(Asteroid):

    def __init__(self, speed):
        super().__init__(speed)
         # importing images       
        small_astro_1 = pygame.image.load("graphics/asteroids/astroSmall1.png").convert_alpha()
        small_astro_2 = pygame.image.load("graphics/asteroids/astroSmall2.png").convert_alpha()
        small_astro_3 = pygame.image.load("graphics/asteroids/astroSmall3.png").convert_alpha()
        
        self.image = choice([small_astro_1,small_astro_2,small_astro_3])    # displaying astro image randomly
        # positioning the astro above the display screen in random x pos inside the screen borders
        self.rect = self.image.get_rect(midbottom = (randint(self.image.get_width(), 800-self.image.get_width()), -100))
        self.destructible = True