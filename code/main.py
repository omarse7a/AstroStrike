import pygame
from random import randint
from math import ceil
from player import Player
from asteroids import Big_asteriod, Small_asteriod

class Main:
    def __init__(self):
        # setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Fighter")
        self.game_active = True
        self.clock = pygame.time.Clock()

        # components
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.bullets = pygame.sprite.Group()

        self.asteriods = pygame.sprite.Group()
        
        
        # background
        self.bg_image = pygame.image.load("graphics/background/background.png").convert()
        self.bg_rect = self.bg_image.get_rect()
        self.bg_tiles = ceil(self.SCREEN_HEIGHT/self.bg_image.get_height()) + 1
        self.scroll = 0

        # respawn timer
        self.astro_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.astro_timer, 500)

    def bg_scroll(self):
         # drawing bg
        for i in range(0, self.bg_tiles):
            self.bg_rect.bottomleft = (0, i*self.bg_image.get_height() + self.scroll)
            self.screen.blit(self.bg_image, self.bg_rect)
        # scroll bg
        self.scroll += 2
        # reset scroll
        if self.scroll >= self.bg_image.get_height():
            self.scroll = 0

    # def check_collisions(self):
    #     if pygame.sprite.spritecollide(self.player.sprite, self.asteriods, False):
    #         self.game_active = False
    
    def run(self):
        # game loop
        while self.game_active:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_active = False
                if event.type == self.astro_timer:
                    if randint(0, 6):   # 5/6 of the time a small astro 
                        self.asteriods.add(Small_asteriod())
                    else:           # 1/6 of the time a big astro 
                        self.asteriods.add(Big_asteriod())

            # draw scrolling bg
            self.bg_scroll()
            
            # player
            self.player.update()
            self.player.draw(self.screen)

            # bullets
            if self.player.sprite.bullets: # player has shot bullets
                self.bullets = self.player.sprite.bullets
                self.bullets.draw(self.screen)
                self.bullets.update()
            
            # asteroids
            self.asteriods.draw(self.screen)
            self.asteriods.update()

            # collisions
            # self.check_collisions()
            
            # update game info
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        
main = Main()
main.run()
