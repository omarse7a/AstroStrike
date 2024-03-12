import pygame
from sys import exit
from random import randint
from math import ceil
import json
from os import path

from player import Player
from asteroids import Big_Asteriod, Small_Asteriod
from my_buttons import Button_1, Button_2
from score import Score


class Main:
    def __init__(self):
        # setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        pygame.init()
        pygame.display.set_caption("Space Fighter")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.icon = pygame.image.load(path.join("graphics","icon","icon.png")).convert()
        pygame.display.set_icon(self.icon)
        self.game_active = False
        self.game_state = "startMenu"
        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.Font(path.join("fonts", "kenvector_future.ttf"), 72)
        self.font2 = pygame.font.Font(path.join("fonts", "kenvector_future_thin.ttf"), 36)
        self.font3 = pygame.font.Font(path.join("fonts", "kenvector_future.ttf"), 24)
        self.score = Score()
        self.new_high_score = False
        self.level = 1
        
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
        self.astro_speed = 4
        
        # background
        self.bg_image = pygame.image.load(path.join("graphics","background", "background.png")).convert()
        self.bg_rect = self.bg_image.get_rect()
        self.bg_tiles = ceil(self.SCREEN_HEIGHT/self.bg_image.get_height()) + 1
        self.scroll = 0
        self.scroll_speed = 3

        # respawn timer
        self.astro_respawn = pygame.USEREVENT + 1
        pygame.time.set_timer(self.astro_respawn, 500)

        # sound effects
        self.lose_sound = pygame.mixer.Sound(path.join("audio", "sfx_lose.ogg"))
        self.lose_sound.set_volume(1)
        self.hit_sound = pygame.mixer.Sound(path.join("audio", "sfx_hit.wav"))
        self.hit_sound.set_volume(0.1)

        # theme song
        music_on = pygame.image.load(path.join("graphics","musicbutton","musicOn.png"))
        music_off = pygame.image.load(path.join("graphics","musicbutton","musicOff.png"))
        self.music_frames = [music_on, music_off]
        self.music_index = 0
        self.music_button = Button_1(music_on, 50, 0)
        self.theme_song = pygame.mixer.Sound(path.join("audio","Long_Away_Home.mp3"))
        self.theme_song.set_volume(0.4)

    def bg_scroll(self):
        # drawing bg
        for i in range(0, self.bg_tiles):
            self.bg_rect.bottomleft = (0, i*self.bg_image.get_height() + self.scroll)
            self.screen.blit(self.bg_image, self.bg_rect)   # drawing each tile
        # scroll bg
        self.scroll += self.scroll_speed  # moving each bg tile slightly down
        # reset scroll
        if self.scroll >= self.bg_image.get_height():   # when the bg image get below the window
            self.scroll = 0

    def check_collisions(self):
        # detects pixel mask collisions for between spaceship and asteroid
        if pygame.sprite.spritecollide(self.player.sprite, self.asteriods, False, pygame.sprite.collide_mask):
            self.lose_sound.play()
            self.game_active = False
            self.game_state = "gameOver"
            self.theme_song.stop()

        # detects rect collisions for between bullets and asteroid
        for sprite in self.asteriods.sprites():
            # small astro collision
            if sprite.destructible:
                if pygame.sprite.spritecollide(sprite, self.bullets, True):
                    self.hit_sound.play()
                    sprite.kill()   # remove the asteroid sprite from the asteroids group
                    self.score.astro_num += 1   # track the # of destroyed asteroids 
            # big astro collision
            else:
                if pygame.sprite.spritecollide(sprite, self.bullets, True):
                    self.hit_sound.play()

    def clear(self):
        # resets the game data for a new game
        self.asteriods.empty()
        self.bullets.empty()
        pygame.time.set_timer(self.astro_respawn, 500)
        self.player.sprite.rect.midtop = (400, 500)
        self.score.start_time = int(pygame.time.get_ticks()/1000)
        self.level = 1
        self.score.astro_num = 0
        self.astro_speed = 4
        self.scroll_speed = 3
        self.new_high_score = False
        self.music_index = 0
        self.music_button.switch_img(self.music_frames[self.music_index])

    def save_high_score(self, score):
        # open the json file as python object <file> on read-write mode
        with open("data.json", 'r+') as file:   
            data = json.load(file)  # loads the json data to a dictionary
            data["high_score"] = max(data["high_score"], score)
            file.seek(0) # move the file pointer to the begining
            json.dump(data, file, indent = 4)
    
    def load_high_score(self):
        try:
            # open the json file as python object <file> on read only mode
            with open("data.json", 'r') as file: 
                data = json.load(file) # loads the json data to a dictionary
                return data["high_score"]
        except FileNotFoundError:   # handling file doesn't exist
            print("High score file not found. Creating a new one.")
            return 0  # Default high score if file doesn't exist
        
    def level_up(self):
        # increasing the game's difficulty
        self.scroll_speed += 1
        self.astro_speed += 1
        self.level += 1

    def run(self):

        # game loop
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.astro_respawn and self.game_active:
                    if randint(0, 6):   # 5/6 of the time a small astro 
                        self.asteriods.add(Small_Asteriod(self.astro_speed))
                    else:           # 1/6 of the time a big astro 
                        self.asteriods.add(Big_Asteriod(self.astro_speed))
                if event.type == pygame.KEYDOWN:
                    # pause when ESC key is pressed
                    if event.key == pygame.K_ESCAPE and self.game_active:
                        pause_time = int(pygame.time.get_ticks()/1000) # the game time when the game is paused
                        self.game_active = False
                        self.game_state = "pause"
                        self.theme_song.stop()
                    # resume when ESC key is pressed again
                    elif event.key == pygame.K_ESCAPE and not self.game_active:
                        resume_time = int(pygame.time.get_ticks()/1000)     # the game time when the game is resumed
                        self.score.paused_time += resume_time - pause_time  # calc the total paused time to remove it from the score calculations
                        self.game_active = True
                        if self.music_index == 0:
                            self.theme_song.play(-1)

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
                self.asteriods.update(self.astro_speed)
                self.asteriods.draw(self.screen)

                # collisions
                self.check_collisions() 

                # score
                self.score.display(self.screen, (self.SCREEN_WIDTH/2, 30), self.font3, "white")
                # checking if the highscore is surpassed
                if self.score.get_score() > self.load_high_score(): 
                    self.new_high_score = True
                self.score.update()

                # music button
                self.music_button.draw(self.screen)
                if self.music_button.pressed():
                    if self.music_index == 0:
                        self.music_index = 1
                        self.music_button.switch_img(self.music_frames[self.music_index])
                        self.theme_song.stop()
                    else:
                        self.music_index = 0
                        self.music_button.switch_img(self.music_frames[self.music_index])
                        self.theme_song.play(-1)

                # difficulty handling (levels)
                # by reducing the asteroids respawn time and increasing their speed
                if self.score.get_score() > 100 and self.level == 1:
                    pygame.time.set_timer(self.astro_respawn, 400)  
                    self.level_up()
                elif self.score.get_score() > 250 and self.level == 2:
                    pygame.time.set_timer(self.astro_respawn, 300)
                    self.level_up()
                elif self.score.get_score() > 500 and self.level == 3:
                    pygame.time.set_timer(self.astro_respawn, 250)
                    self.level_up()
                elif self.score.get_score() > 1000 and self.level == 4:
                    pygame.time.set_timer(self.astro_respawn, 200)
                    self.level_up()

            # game states
            else:
                 # start menu screen
                if self.game_state == "startMenu":
                    self.screen.fill((0,8,64))

                    self.screen.blit(self.game_title, self.game_title_rect)

                    self.start_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    self.exit_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))

                    if self.start_button.pressed():
                        self.score.start_time = int(pygame.time.get_ticks()/1000)
                        self.game_active = True
                        self.theme_song.play(-1)

                    if self.exit_button.pressed():
                        pygame.quit()
                        exit()
                # game over screen
                elif self.game_state == "gameOver":
                    self.screen.fill((0,8,64))

                    self.lose_text = self.font1.render("Game Over", True,(66,22,210))
                    self.lose_rect = self.lose_text.get_rect(center = (self.SCREEN_WIDTH/2, 100))
                    self.screen.blit(self.lose_text, self.lose_rect)
                    
                    self.score.display(self.screen, (self.SCREEN_WIDTH/2, 230), self.font2, (66,22,210))

                    # print new beside the highscore in the gameover screen when the highscore is broken
                    if self.new_high_score:
                        self.high_score_text = self.font2.render(f"HighScore: {self.load_high_score()} (new)", True,(66,22,210))
                        self.save_high_score(self.score.get_score())  
                    else:
                        self.high_score_text = self.font2.render(f"HighScore: {self.load_high_score()}", True,(66,22,210))
                    self.high_score_rect = self.high_score_text.get_rect(center = (self.SCREEN_WIDTH/2, 320))
                    self.screen.blit(self.high_score_text, self.high_score_rect)
                    
                    self.restart_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))
                    self.menu_button.draw(self.screen, (145, 44, 238), "blue", 2, 10, (165, 64, 255))

                    keys = pygame.key.get_pressed()
                    if self.restart_button.pressed() or keys[pygame.K_RETURN]:
                        self.clear()
                        self.game_active = True
                        self.theme_song.play(-1)

                    if self.menu_button.pressed():
                        self.clear()
                        self.game_state = "startMenu"

                # pause screen
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
                        self.theme_song.play(-1)
                        
                    if self.menu_button.pressed():
                        self.clear()
                        self.game_state = "startMenu"
                

            # update game info
            pygame.display.update() # updating the pygame window
            self.clock.tick(60) # adjusting a maximum frame rate for game stability


# runs the script in class main only 
if __name__ == "__main__":  
    main = Main()
    main.run()
