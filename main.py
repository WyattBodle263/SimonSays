import pygame
import random
import time
from button import Button # By importing Button we can access methods from the Button class

pygame.init() #Initialize the pygame library/class

clock = pygame.time.Clock()

#Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 227, 0)
RED_ON = (255, 0, 0)
RED_OFF = (227, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 227)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)
WHITE_COLOR = (255, 255, 255) #Setting color

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound("bell1.mp3") #bell1
RED_SOUND = pygame.mixer.Sound("bell2.mp3") #bell2
BLUE_SOUND = pygame.mixer.Sound("bell3.mp3") #bell3
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3") #bell4
GAME_OVER_SOUND =pygame.mixer.Sound("game_over.mp3") #game over

#Button Sprite Objects

#Game buttons
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 100,"")
red = Button(RED_ON, RED_OFF, RED_SOUND, 260, 100,"")
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 360,"")
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 360,"")
#Game over buttons
quit_button = Button(WHITE_COLOR, WHITE_COLOR, RED_SOUND, 260, 360, "Quit")
continue_button = Button(WHITE_COLOR, WHITE_COLOR, RED_SOUND, 10, 360, "Play Again")

#Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""
score = 0


'''
draws the text
'''
def draw_text(text, placement):
    #Sets up the font
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, WHITE_COLOR)
    text_rect = text.get_rect()

    # Sets the position based on where I want the text and clears previous text by drwaing over it
    if placement == "center": #Center for any object centered in the whitespace
        SCREEN_X = (SCREEN_WIDTH - text_rect.width)/2 #Gets the horizontal center of the whitespace
        SCREEN_Y = 50 - text_rect.height / 2 #Gets the vertical center of the whitespace
        text_rect = (SCREEN_X, SCREEN_Y)
        clear_rectangle = pygame.Rect((SCREEN_WIDTH / 2 - text.get_rect().width / 2), (50 - text.get_rect().height / 2), text.get_rect().width, text.get_rect().height)
    else: #Anything else will be pushed to the left top corner of the whitespace
        text_rect = (10,10)
        clear_rectangle = pygame.Rect(10, 10, text.get_rect().width, text.get_rect().height)

    #Draw and update screen
    SCREEN.fill((0, 0, 0), clear_rectangle)
    SCREEN.blit(text, text_rect)
    pygame.display.flip() #Display


'''
Draws game board
'''

def draw_board():

    #Call the draw method on all four button objects and two texts
    draw_text("Score: " + str(score), "center")
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

'''
Draws game over screen
'''

def draw_game_over():
    GAME_OVER_SOUND.play()

    #Clear the screen
    SCREEN.fill((0, 0, 0))

    #Draw objects and buttons
    draw_text("Score: " + str(score), "center")
    quit_button.draw(SCREEN)
    continue_button.draw(SCREEN)

    #Drawing the game over image
    IMAGE_WIDTH = 300
    IMAGE_HEIGHT = 150
    image = pygame.image.load("game_over.png")
    scaled_image_rect = pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_HEIGHT)) #Scaling
    image_rect = scaled_image_rect.get_rect()
    # Set the initial position of the image
    x = (SCREEN_WIDTH - IMAGE_WIDTH / 2) / 2 - IMAGE_WIDTH / 8  #IF IMAGE WAS CENTERED EQUATION IS (SCREEN_WIDTH - IMAGE_WIDTH)/2
    y = (SCREEN_HEIGHT - IMAGE_HEIGHT - 235 - IMAGE_HEIGHT / 2)
    image_rect.topleft = (x, y)
    # Blit the image onto the screen
    SCREEN.blit(scaled_image_rect, image_rect)
    # Update the screen to make the changes visible
    pygame.display.flip() #Display

'''
Chooses a random color and appends to cpu_sequence.
Illuminates randomly chosen color.
'''

def cpu_turn():
    choice = random.choice(colors) #pick random color
    cpu_sequence.append(choice) #Update cpu sequence
    if choice == "green":
        green.update(SCREEN)
        #Check other three color options
    elif choice == "red":
        red.update(SCREEN)
    elif choice == "blue":
        blue.update(SCREEN)
    else:
        yellow.update(SCREEN)

'''
Plays pattern sequence that is being tracked by cpu_sequence
'''

def repeat_cpu_sequence():
    if(len(cpu_sequence) != 0):
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)

'''
After cpu sequence is repeated the player ust attempt to copy that 
pattern sequence
They player is given 3 seconds to select a color and checks if the 
color matches the cpu pattern sequence.
If player is unable to select a color within 3 seconds then the game is over and the pygame window closes. 
'''

def player_turn():
    turn_time = time.time()
    players_sequence = []
    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        draw_text(str(3 - round(time.time() - turn_time)),"left")
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        #button clock occured
                #Grab the current posisiton of mouse here
                pos = pygame.mouse.get_pos()
                if green.selected(pos): #green button was selected
                    green.update(SCREEN) #illuminate button
                    players_sequence.append("green") #add to player sequence
                    check_sequence(players_sequence) #check if the player choice was correct
                    turn_time = time.time() # reset timer
                    #Check other three options
                elif red.selected(pos):  # green button was selected
                    red.update(SCREEN)  # illuminate button
                    players_sequence.append("red")  # add to player sequence
                    check_sequence(players_sequence)  # check if the player choice was correct
                    turn_time = time.time()  # reset timer
                elif blue.selected(pos):  # green button was selected
                    blue.update(SCREEN)  # illuminate button
                    players_sequence.append("blue")  # add to player sequence
                    check_sequence(players_sequence)  # check if the player choice was correct
                    turn_time = time.time()  # reset timer
                elif yellow.selected(pos):  # green button was selected
                    yellow.update(SCREEN)  # illuminate button
                    players_sequence.append("yellow")  # add to player sequence
                    check_sequence(players_sequence)  # check if the player choice was correct
                    turn_time = time.time()  # reset timer

            # If player does not select a button within 3 seconds then the game closes
    if not time.time() <= turn_time + 3:
        game_over()

'''Check if the player's move matches the cpu pattern sequence'''

def check_sequence(players_sequence):
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()

'''
Reset the game
'''
def reset():
    SCREEN.fill((0, 0, 0))  # Draw over screen again
    pygame.display.flip()  # Display
    global cpu_sequence, choice, score
    cpu_sequence = []
    choice = ""
    score = 0

    reset_flag = True #Flag that keeps the user in the game over screen

    while reset_flag:
        #Check for button press and game over
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if continue_button.selected(pos):
                    reset_flag = False

        pygame.display.update()
        draw_board()
        repeat_cpu_sequence()
        cpu_turn()
        player_turn()
        pygame.time.wait(1000)
        score += 1

        clock.tick(60)

    game_over()

'''
Goes to game over screen with reset button and quit button
'''
def game_over():
    turn_time = time.time()
    draw_game_over()
    while time.time() <= turn_time + 20:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # button clock occured
                # Grab the current posisiton of mouse here
                pos = pygame.mouse.get_pos()
                if quit_button.selected(pos):  # quit button was selected
                    pygame.quit()
                    quit()
                elif continue_button.selected(pos):
                    reset()

    if not time.time() <= turn_time + 20:
        pygame.quit()
        quit()
'''
Quits game and closes pygame window
'''

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            quit()

        pygame.display.update()
        draw_board() #draws buttons onto pygame screen
        repeat_cpu_sequence() #repeats cpu sequence if it's not empty
        cpu_turn() #cpu randomly chooses a new color
        player_turn() #player tries to recreate cpu sequence
        pygame.time.wait(1000) #waits one second before repeating cpu sequence
        score += 1

        clock.tick(60)



