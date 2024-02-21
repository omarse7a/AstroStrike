import pygame
from player import Player

class Main:
    def __init__(self):
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Fighter")
        self.game_active = True
        self.clock = pygame.time.Clock()

        # components
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.bg_image = pygame.image.load("graphics/background/background1.png").convert()
        self.bg_rect = self.bg_image.get_rect(topleft = (0, 0))
        
    
    def run(self):
        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_active = False

            self.screen.blit(self.bg_image, self.bg_rect)
            
            self.player.update()
            self.player.draw(self.screen)
            

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        
main = Main()
main.run()
