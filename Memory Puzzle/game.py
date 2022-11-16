import json
import pygame
from random import randint
import tkinter as tk
from datetime import datetime
from objects import Board, Button, message_box

### SETUP *********************************************************************
pygame.init()
SCREEN = WIDTH, HEIGHT = 1000, 580
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption('Memory Puzzle')

clock = pygame.time.Clock()
FPS = 30

ROWS, COLS = 8, 10
TILESIZE = 45


### TIMER ********************************************************************


### COLORS ********************************************************************
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 25, 25)
WHITE = (255, 255, 255)
secondsnew = 0
firstclickdone = False
secondsnewdiff = 0
### LOADING IMAGES ************************************************************
img_list = []
for img in range(1,21):
        image = pygame.image.load(f"Assets/icons/{img}.jpeg")
        image = pygame.transform.scale(image, (TILESIZE,TILESIZE))
        img_list.append(image)
bgs = pygame.image.load('Assets/background/bg.jpg')
bg=pygame.transform.scale(bgs, (WIDTH+500, HEIGHT+300))
game_won = pygame.image.load('Assets/won.png')
rightbar = pygame.image.load('Assets/image.jpg')
rightbar = pygame.transform.scale(rightbar, (370, HEIGHT - 47))
nextlevelimg = pygame.image.load('Assets/nextlevel.png')
nextlevel = pygame.transform.scale(nextlevelimg, (550, 220))

### Loading Sounds ************************************************************
pygame.mixer.music.load('Sounds/Puzzle-Game-3_Looping.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

card_click = pygame.mixer.Sound("Sounds/card click.wav")
woosh = pygame.mixer.Sound("Sounds/woosh.mp3")

### Buttons *******************************************************************
restart_img = pygame.image.load('Assets/restart.png')
restart_btn = Button(restart_img, (40,40), 755, 280)

info_img = pygame.image.load('Assets/info.png')
info_btn = Button(info_img, (40,40), 755, 330)

close_img = pygame.image.load('Assets/close.png')
close_btn = Button(close_img, (40,40), 755, 380)

nextlevel_img = pygame.image.load('Assets/next.png')
next_btn = Button(nextlevel_img, (80,80), 455, 430)

### LOADING FRUITS INFORMATION ************************************************
with open('Info/info.json') as f:
        dct = json.load(f)

### LOADING FONTS *************************************************************
sys_font = pygame.font.SysFont(("Times New Roman"),20)
clicks_font = pygame.font.SysFont(("Algerian"),30)

### CREATING BOARD ************************************************************
board = Board(img_list)
board.randomize_images()

animated_boxes = [(randint(0,7), randint(0,9)) for i in range(20)]

### GAME VARIABLES ************************************************************
game_screen = True
first_card = None
second_card = None
first_click_time = None
second_click_time = None
numCards = 80
isLoading = True
animation_on = True
animation_count = 0
prev_count = 0
level = 0
gameWon = False
numClicks = 0
numSec = 0
prevCards = numCards
levelreqscores = [2,3,4,5]
running = True

start_ticks=pygame.time.get_ticks()

while running:
        win.blit(bg, (0,0), (400, 100,WIDTH,HEIGHT))
        win.blit(rightbar, (595, 20))
        pygame.draw.rect(win, BLUE, (5, 10, 585, HEIGHT - 20), 2)
        pygame.draw.rect(win, BLUE, (585, 10, 390, HEIGHT - 20), 2)

        if restart_btn.draw(win):
                game_screen = True
                show_text = False
                first_card = None
                second_card = None
                first_click_time = None
                second_click_time = None

                board.randomize_images()

                isLoading = True
                animation_on = True
                animation_count = 0
                numClicks = 0
                numSec = 0
                numCards = 80
                prevCards = numCards
                gameWon = False
                firstclickdone = False
                secondsnew = 0

                start_ticks=pygame.time.get_ticks()

        if info_btn.draw(win):
                game_screen = False
                show_text = False

        if close_btn.draw(win):
                running = False

        seconds=(pygame.time.get_ticks()-start_ticks)/1000
        if firstclickdone:
                secondsnew = (pygame.time.get_ticks()-start_ticks)/1000-secondsnewdiff
        else:
                secondsnewdiff = (pygame.time.get_ticks()-start_ticks)/1000
        if seconds>500:
                board.randomize_images()

        clicked = False

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                                running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                                clicked = True
                                x, y = pygame.mouse.get_pos()
 

        if game_screen:
                ### Game is on
                if numCards == 80-levelreqscores[3]*2-levelreqscores[2]*2-levelreqscores[1]*2-levelreqscores[0]*2-6:
                        gameWon = True
                        level=0
                if numCards == 80-levelreqscores[0]*2:
                        gameWon = True
                        level = 1
                if numCards == 80-levelreqscores[0]*2-levelreqscores[1]*2-2:
                        gameWon = True
                        level = 2
                if numCards == 80-levelreqscores[2]*2-levelreqscores[1]*2-levelreqscores[0]*2-4:
                        gameWon = True
                        level = 3

                if isLoading:
                        ### Preview card animation
                        clicked = False

                        if animation_count < 80:
                                for index, pos in enumerate(animated_boxes):
                                        card = board.board[pos[0]][pos[1]]
                                        if card.cover_x >= TILESIZE:
                                                card.visible = True
                                                card.animate = True
                                                card.slide_left = True

                                        if card.cover_x <= 0:
                                                card.animate = True
                                                card.slide_left = False

                                if card.animation_complete:
                                        for pos in animated_boxes:
                                                card = board.board[pos[0]][pos[1]]
                                                card.visible = False
                                                card.animate = False
                                        animated_boxes = [(randint(0,7), randint(0,9)) for i in range(len(img_list))]
                                        animation_count += 1
                        else:
                                isLoading = False
                                animation_on = False
                                animation_count = 0


                if not gameWon:
                        ### Polling time to hide cards
                        if second_click_time:
                                current_time = pygame.time.get_ticks()

                                delta = current_time - second_click_time
                                if delta >= 1000:
                                        if first_card.value == second_card.value:
                                                first_card.is_alive = False
                                                second_card.is_alive = False
                                                numCards -= 2
                                                woosh.play()

                                        index = first_card.index
                                        fcard = board.board[index[0]][index[1]]
                                        fcard.animate = True
                                        fcard.slide_left = False
                                        first_card = None

                                        index = second_card.index
                                        scard = board.board[index[0]][index[1]]
                                        scard.animate = True
                                        scard.slide_left = False
                                        second_card = None

                                        first_click_time = None
                                        second_click_time = None
                                else:
                                        clicked = False
                        win.blit(clicks_font.render("Clicks: " + str(numClicks), True, WHITE), (600, 50))
                        win.blit(clicks_font.render("Time: " + str(int(numSec)), True, WHITE), (600, 75))
                        win.blit(clicks_font.render("Timer: " + str(int(secondsnew)), True, WHITE), (600, 125))
                        win.blit(clicks_font.render("Matches: " + str(int((prevCards-numCards)/2))+"/"+str(levelreqscores[level]), True, WHITE), (600, 100))


                        ### Displaying cards
                        for r in range(ROWS):
                                for c in range(COLS):
                                        border = False
                                        card = board.board[r][c]
                                        if card.is_alive:
                                                xcord = card.rect.x
                                                ycord = card.rect.y

                                                if not isLoading:
                                                        if card.rect.collidepoint((x,y)):
                                                                border = True
                                                                if clicked:
                                                                        card_click.play()
                                                                        numClicks += 1
                                                                        numSec=(pygame.time.get_ticks()-start_ticks)/1000
                                                                        firstclickdone = True
                                                                        card.visible = True
                                                                        card.animate = True
                                                                        card.slide_left = True

                                                                        if not first_card:
                                                                                first_card = card
                                                                        else:
                                                                                second_card = card
                                                                                if second_card != first_card:
                                                                                        second_click_time = pygame.time.get_ticks()
                                                                                else:
                                                                                        second_card = None

                                                pygame.draw.rect(win, BLACK, (xcord+5, ycord+5,TILESIZE, TILESIZE))

                                                if not card.animate:
                                                        if card.visible:
                                                                win.blit(card.image, card.rect)
                                                        else:
                                                                pygame.draw.rect(win, WHITE, (xcord, ycord,TILESIZE, TILESIZE))

                                                        if border and not isLoading:
                                                                pygame.draw.rect(win, RED, (xcord, ycord,TILESIZE, TILESIZE), 2)
                                                else:
                                                        if isLoading:
                                                                speed = 2
                                                        else:
                                                                speed = 2
                                                        card.on_click(win, speed)
                elif level ==1:
                        ### display next level
                        win.blit(nextlevel, (20,100))
                        # win.blit("Level 2", (WIDTH/2, HEIGHT/2))
                        
                        #display button
                        if next_btn.draw(win):
                                game_screen = True
                                show_text = False
                                first_card = None
                                second_card = None
                                first_click_time = None
                                second_click_time = None

                                board.randomize_images()
                                
                                isLoading = True
                                animation_on = True
                                animation_count = 0
                                bgs =pygame.image.load('Assets/background/bg2.jpg')
                                bg=pygame.transform.scale(bgs, (WIDTH+500, HEIGHT+300))
                                # bg=pygame.transform.scale(bg,SCREEN_SIZE)
                                numCards = 80-levelreqscores[0]*2-2
                                prevCards = numCards
                                gameWon = False

                                start_ticks=pygame.time.get_ticks()
                elif level ==2:
                        ### display next level
                        win.blit(nextlevel, (20,100))
                        # win.blit("Level 2", (WIDTH/2, HEIGHT/2))
                        #display button
                        if next_btn.draw(win):
                                game_screen = True
                                show_text = False
                                first_card = None
                                second_card = None
                                first_click_time = None
                                second_click_time = None

                                board.randomize_images()

                                isLoading = True
                                animation_on = True
                                animation_count = 0
                                numCards = 80-levelreqscores[0]*2-levelreqscores[1]*2-4
                                bgs =pygame.image.load('Assets/background/bg3.jpg')
                                bg=pygame.transform.scale(bgs, (WIDTH+500, HEIGHT+300))
                                gameWon = False
                                prevCards = numCards

                                start_ticks=pygame.time.get_ticks()

                elif level ==3:
                        ### display next level
                        win.blit(nextlevel, (20,100))
                        # win.blit("Level 2", (WIDTH/2, HEIGHT/2))

                        #display button
                        if next_btn.draw(win):
                                game_screen = True
                                show_text = False
                                first_card = None
                                second_card = None
                                first_click_time = None
                                second_click_time = None

                                board.randomize_images()

                                isLoading = True
                                animation_on = True
                                animation_count = 0
                                bgs =pygame.image.load('Assets/background/bg4.jfif')
                                bg=pygame.transform.scale(bgs, (WIDTH+500, HEIGHT+300))
                                numCards = 80-levelreqscores[2]*2-levelreqscores[1]*2-levelreqscores[0]*2-6
                                prevCards = numCards
                                gameWon = False


                else:
                        win.blit(game_won, (0,100))
                        image = clicks_font.render(f'Number of Clicks : {numClicks}', 0, (255, 255, 255))
                        image1 = clicks_font.render(f'Total time in seconds: {numSec}',0,(255, 255, 255))
                        win.blit(image, (150, 350))
                        win.blit(image1, (150, 400))
        else:
                for r in range(2):
                        for c in range(COLS):
                                card = board.info_board[r][c]
                                xcord = card.rect.x
                                ycord = card.rect.y

                                pygame.draw.rect(win, BLACK, (xcord+5, ycord+5,TILESIZE, TILESIZE))
                                win.blit(card.image, card.rect)

                                if card.rect.collidepoint((x,y)):
                                        pygame.draw.rect(win, RED, (xcord, ycord,TILESIZE, TILESIZE), 2)

                                        if clicked:
                                                card_click.play()
                                                show_text = True
                                                data = dct[str(card.value)]
                                                name = data['Name']
                                                info = data['Info']

                                                border = True
                                                pos = (xcord, ycord)

                if border:
                        pygame.draw.rect(win, BLUE, (pos[0], pos[1],TILESIZE, TILESIZE), 2)
                if show_text:
                        message_box(win, sys_font, name, info)


        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
