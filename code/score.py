import pygame

class Score:
    def __init__(self):
        self.start_time = 0 # to reset the score when the game restarts
        self.score = 0
        self.astro_num = 0  # number of destroyed asteroids

    def display(self, surface, font):
        # display the score at the top of the game screen
        self.score_surface = font.render(f"Score: {self.score}", True, "grey")
        self.score_rect = self.score_surface.get_rect(center = (400, 30)) 
        surface.blit(self.score_surface, self.score_rect)

    def update(self):
        # updating the score each frame
        time_elapsed = int(pygame.time.get_ticks()/1000)
        self.score = (time_elapsed-self.start_time) + self.astro_num*10