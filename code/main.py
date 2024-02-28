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
        self.game_state = "startMenu"
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font("fonts/kenvector_future.ttf", 72)
        self.font2 = pygame.font.Font("fonts/kenvector_future_thin.ttf", 46)
        self.font3 = pygame.font.Font("fonts/kenvector_future.ttf", 24)
        self.score = Score()
        
        # start menu
        self.game_title = self.font1.render("Space Fighter", True,(66,22,210))
        self.game_title_rect = self.game_title.get_rect(center = (self.SCREEN_WIDTH/2, 150))

        # buttons
        self.start_button = Button_2("Start", (300,80), (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/2 + 30), self.font2, (66,22,210))
        self.exit_button = Button_2("Exit", (300,80), (self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT/1.5 + 50), self.font2, (66,22,210))
        self.restart_button = Button_2("Restart", (200,60), (self.SCREEN_WIDTH/3, 450), self.font3, (66,22,210))
        self.menu_button = Button_2("Main Menu", (200,60), (self.SCREEN_WIDTH/1.5, 450), self.font3, (66,22,210))

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

        # sound effects
        self.lose_sound = pygame.mixer.Sound("audio/sfx_lose.ogg")
        self.lose_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound("audio/sfx_hit.wav")
        self.hit_sound.set_volume(0.05)

    def bg_scroll(self):
         # drawing bg
        for i in range(0, self.bg_tiles):
            self.bg_rect.bottomleft = (0, i*self.bg_image.get_height() + self.scroll)
            self.screen.blit(self.bg_image, self.bg_rect)
        # scroll bg
        self.scroll += 3
        # reset scroll
        if self.scroll >= self.bg_image.get_height():
            self.scroll = 0

    def check_collisions(self):
        # detects pixel mask collisions for between spaceship and asteroid
        if pygame.sprite.spritecollide(self.player.sprite, self.asteriods, False, pygame.sprite.collide_mask):
            self.lose_sound.play()
            self.game_active = False
            self.game_state = "gameOver"

        # detects rect collisions for between bullets and asteroid
        for sprite in self.asteriods.sprites():
            # big astro collisions
            if sprite.destructible:
                if pygame.sprite.spritecollide(sprite, self.bullets, True):
                    self.hit_sound.play()
                    sprite.kill() 
                    self.score.astro_num += 1
            # small astro collision
            elif pygame.sprite.spritecollide(sprite, self.bullets, True):
                self.hit_sound.play()

    # def display_text(self, text, color, font):
    #     self.text = font.render(text, True, color)
    #     self.rect = self.text.get_rect(center = (self.SCREEN_WIDTH/2, 150))

    def clear(self):
        self.asteriods.empty()
        self.bullets.empty()
        self.score.start_time = int(pygame.time.get_ticks()/1000)
        self.score.astro_num = 0

    def run(self):

        # game loop
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.astro_timer and self.game_active:
                    if randint(0, 6):   # 5/6 of the time a small astro 
                        self.asteriods.add(Small_Asteriod())
                    else:           # 1/6 of the time a big astro 
                        self.asteriods.add(Big_Asteriod())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.game_active:
                        self.game_active = False
                        self.game_state = "pause"
                    elif event.key == pygame.K_ESCAPE and not self.game_active:
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
                self.score.display(self.screen, (self.SCREEN_WIDTH/2, 30), self.font3, "grey")
                self.score.update()

            # game states
            else:
                 # start menu
                if self.game_state == "startMenu":
                    self.screen.fill((0,8,64))
                    self.screen.blit(self.game_title, self.game_title_rect)
                    self.start_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    self.exit_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    if self.start_button.pressed():
                        self.score.start_time = int(pygame.time.get_ticks()/1000)
                        self.game_active = True
                    if self.exit_button.pressed():
                        pygame.quit()
                        exit()
                # game over 
                elif self.game_state == "gameOver":
                    self.end_text = self.font1.render("Game Over", True,(66,22,210))
                    self.end_text_rect = self.end_text.get_rect(center = (self.SCREEN_WIDTH/2, 200))
                    self.screen.fill((0,8,64))
                    self.screen.blit(self.end_text, self.end_text_rect)
                    self.score.display(self.screen, (self.SCREEN_WIDTH/2, 300), self.font2, (66,22,210))
                    self.restart_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    self.menu_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    keys = pygame.key.get_pressed()
                    if self.restart_button.pressed() or keys[pygame.K_RETURN]:
                        self.clear()
                        self.game_active = True
                    if self.menu_button.pressed():
                        self.clear()
                        self.game_state = "startMenu"

                # pause
                elif self.game_state == "pause":
                    self.screen.fill((0,8,64))
                    self.pause_text = self.font1.render("Pause", True,(66,22,210))
                    self.pause_text_rect = self.pause_text.get_rect(center = (self.SCREEN_WIDTH/2, 200))
                    self.screen.blit(self.pause_text, self.pause_text_rect)
                    self.restart_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    self.menu_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    if self.restart_button.pressed():
                        self.clear()
                        self.game_active = True
                    if self.menu_button.pressed():
                        self.clear()
                        self.game_state = "startMenu"
                

            # update game info
            pygame.display.update()
            self.clock.tick(60)


# runs the script in class main only 
if __name__ == "__main__":  
    main = Main()
    main.run()
