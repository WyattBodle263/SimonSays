import random
import time
import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    '''
    Constructor for color buttons
    '''
    def __init__(self, color_on, color_off, sound, x, y, text): #Adds text to constructor to allow for other buttons
        pygame.sprite.Sprite.__init__(self)
        # Initialize properties
        self.color_on = color_on
        self.color_off = color_off
        self.sound = sound
        self.x = x
        self.y = y
        self.text = text
        #Create the starting square
        self.image = pygame.Surface((230,230))
        self.image.fill(self.color_off)
        self.rect = self.image.get_rect()
        # Assign x, y coordinates to the top left of the sprite
        self.rect.topleft = (x, y)
        self.clicked = False

    '''
    Draws button sprite onto pygame window when called
    '''

    def draw(self, screen):
        # Draw the button image
        screen.blit(self.image, (self.x, self.y))

        # Create a font object
        font = pygame.font.Font(None, 32)

        # Create a text surface with the specified text and color
        text_surface = font.render(self.text, True, (0, 0, 0))

        # Calculate the center position for the text
        text_x = self.x + (self.image.get_width() - text_surface.get_width()) // 2
        text_y = self.y + (self.image.get_height() - text_surface.get_height()) // 2

        # Draw the text surface onto the button
        screen.blit(text_surface, (text_x, text_y))
        pygame.display.flip()

    '''
    Used to check if given button is clicked/selected by player
    '''

    def selected(self, mouse_pos):
        #check if button was selected. Pass in mouse_pos.
        if self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


    '''
    Illuminates button selected and plays corresponding sound.
    Sells button color back tot default color after being illuminated
    '''

    def update(self, screen):
        # Illuminate button by filling color here
        self.image.fill(self.color_on)
        # Blit the image here so it is visable to the player
        screen.blit(self.image, (self.x, self.y))
        # Play sound
        self.sound.play()

        pygame.display.update()
        self.image.fill(self.color_off)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.time.wait(500)
        pygame.display.update()