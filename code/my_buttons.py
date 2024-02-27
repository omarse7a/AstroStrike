import pygame

# image button
class Button_1:
    def __init__(self, image, x, y, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect(midtop = (x, y))
        self.clicked = False
    
     # draw the button
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    # returns true when the mouse is over the button
    def hover(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos();
        return  self.rect.collidepoint(mouse_pos)

    # returns true when the click is released
    def pressed(self):  
        # get mouse position
        mouse_pos = pygame.mouse.get_pos();
        # check mouseover the button and mouse click
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # mouse left click
                self.clicked = True
            if not pygame.mouse.get_pressed()[0] and self.clicked == True:  # mouse click released
                self.clicked = False
                return True

# text rect button        
class Button_2:
    def __init__(self, text, size, pos, font, text_color = "white"):

        self.rect = pygame.rect.Rect((0,0), size) # (0,0) is the topleft value to be changed later
        self.rect.center = pos
        
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center = pos)
        
        self.clicked = False

    # draw the button
    def draw(self, screen, button_color = "black", border_col = "white", border = 0, border_radius = 0, hover_color = None):
        if hover_color and self.hover():         
            pygame.draw.rect(screen, hover_color, self.rect, 0, border_radius)
        else:
            pygame.draw.rect(screen, button_color, self.rect, 0, border_radius)
        pygame.draw.rect(screen, border_col, self.rect, border, border_radius)
        screen.blit(self.text_surface, self.text_rect)

    # returns true when the mouse is over the button
    def hover(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos();
        return  self.rect.collidepoint(mouse_pos)

    # returns true when the click is released
    def pressed(self):  
        # get mouse position
        mouse_pos = pygame.mouse.get_pos();
        # check mouseover the button and mouse click
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False: # mouse left click
                self.clicked = True
            if not pygame.mouse.get_pressed()[0] and self.clicked == True:  # mouse click released
                self.clicked = False
                return True