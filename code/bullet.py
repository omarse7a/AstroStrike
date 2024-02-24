import pygame
class Bullet(pygame.sprite.Sprite):

    def __init__(self, player_x):

        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("graphics/bullet.png").convert_alpha(), (10, 25))
        self.rect = self.image.get_rect(midbottom = (player_x, 510))

    def move(self):

        if self.rect.top >= 0:
            self.rect.y -= 7
        else:
            self.kill()
    
    def update(self):

        self.move()