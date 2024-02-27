import pygame
from sys import exit
from random import randint
from math import ceil
from player import Player
from asteroids import Big_Asteriod, Small_Asteriod
from my_buttons import Button_2
from score import Score

class Main:
    def __init__(self):
        # setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Space Fighter")
        self.game_active = False
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font("fonts/kenvector_future.ttf", 72)
        self.font2 = pygame.font.Font("fonts/kenvector_future_thin.ttf", 46)
        self.font3 = pygame.font.Font("fonts/kenvector_future.ttf", 24)
        self.score = Score()
        

        # start menu
        self.game_title = self.font1.render("Space Fighter", True,(66,22,210))
        self.game_title_rect = self.game_title.get_rect(center = (self.SCREEN_WIDTH/2, 150))
        self.start_button = Button_2("Start", (300,80), (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2 + 30), self.font2, (66,22,210))
        self.exit_button = Button_2("Exit", (300,80), (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/1.5 + 50), self.font2, (66,22,210))


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

    def check_collisions(self):
        # detects pixel mask collisions for between spaceship and asteroid
        if pygame.sprite.spritecollide(self.player.sprite, self.asteriods, False, pygame.sprite.collide_mask): 
            self.game_active = False

        # detects rect collisions for between bullets and asteroid
        for sprite in self.asteriods.sprites():
            # big astro collisions
            if sprite.destructible:
                if pygame.sprite.spritecollide(sprite, self.bullets, True):
                    sprite.kill() 
                    self.score.astro_num += 1
            # small astro collision
            else:
                pygame.sprite.spritecollide(sprite, self.bullets, True)


    
    def run(self):

        # game loop
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.exit_button.pressed():
                    pygame.quit()
                    exit()
                if event.type == self.astro_timer and self.game_active:
                    if randint(0, 6):   # 5/6 of the time a small astro 
                        self.asteriods.add(Small_Asteriod())
                    else:           # 1/6 of the time a big astro 
                        self.asteriods.add(Big_Asteriod())
                        
            # start menu
            self.screen.fill((0,8,64))
            self.screen.blit(self.game_title, self.game_title_rect)
            self.start_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
            self.exit_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
            if self.start_button.pressed():
                self.game_active = True

            if self.game_active:
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
                self.asteriods.update()
                self.asteriods.draw(self.screen)

                # collisions
                self.check_collisions() 

                # score
                self.score.display(self.screen, self.font3)
                self.score.update()

            # game over / pause states
            else:
                pass
            # update game info
            pygame.display.update()
            self.clock.tick(60)


# runs the script in class main only 
if __name__ == "__main__":  
    main = Main()
    main.run()
