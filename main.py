import pygame
import sys
from random import randint

pygame.init()

# Window
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("assets/font/Pixeltype.ttf", 32)

# Load Images
background = pygame.image.load("assets/image/background.png")
title_img = pygame.image.load("assets/image/title.png")

play_img = pygame.image.load("assets/image/play.png")
easy_img = pygame.image.load("assets/image/easy.png")
medium_img = pygame.image.load("assets/image/medium.png")
hard_img = pygame.image.load("assets/image/hard.png")

background = pygame.transform.scale(background, (WIDTH, HEIGHT))
title_img = pygame.transform.scale(title_img, (1000,200))
play_img = pygame.transform.scale(play_img, (100,100))
easy_img = pygame.transform.scale(easy_img, (100,100))
medium_img = pygame.transform.scale(medium_img, (100,100))
hard_img = pygame.transform.scale(hard_img, (100,100))

# =============================
# ENEMY SPRITES
# =============================

skull_frame1 = pygame.image.load("assets/image/enemies/Enemy.png").convert_alpha()
skull_frame2 = pygame.image.load("assets/image/enemies/Enemy_2.png").convert_alpha()

reaper_frame1 = pygame.image.load("assets/image/enemies/Enemy2.png").convert_alpha()
reaper_frame2 = pygame.image.load("assets/image/enemies/Enemy2_2.png").convert_alpha()

skull_frame1 = pygame.transform.scale(skull_frame1,(60,60))
skull_frame2 = pygame.transform.scale(skull_frame2,(60,60))
reaper_frame1 = pygame.transform.scale(reaper_frame1,(80,80))
reaper_frame2 = pygame.transform.scale(reaper_frame2,(80,80))

skullFrames = [skull_frame1, skull_frame2]
reaperFrames = [reaper_frame1, reaper_frame2]

skullFrameIndex = 0
reaperFrameIndex = 0

skull = skullFrames[skullFrameIndex]
reaper = reaperFrames[reaperFrameIndex]

enemyRectList = []

# =============================
# TIMER
# =============================

enemySpawnTimer = pygame.USEREVENT + 1
pygame.time.set_timer(enemySpawnTimer, 2000)

skullAnimationTimer = pygame.USEREVENT + 2
pygame.time.set_timer(skullAnimationTimer, 200)

reaperAnimationTimer = pygame.USEREVENT + 3
pygame.time.set_timer(reaperAnimationTimer, 400)

# =============================
# GAME STATE
# =============================

state = "menu"

# =============================
# BUTTON CLASS
# =============================

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
play_button = Button(play_img, 375, 350)

easy_button = Button(easy_img, 300, 350)
medium_button = Button(medium_img, 400, 350)
hard_button = Button(hard_img, 500, 350)

# =============================
# ENEMY FUNCTIONS
# =============================

def enemySpawner(event):
    global skullFrameIndex,reaperFrameIndex,skull,reaper

    if event.type == enemySpawnTimer:

        if randint(0,2):
            enemyRectList.append(skull.get_rect(midbottom=(randint(950,1100),500)))
        else:
            enemyRectList.append(reaper.get_rect(midbottom=(randint(950,1100),420)))

    if event.type == skullAnimationTimer:
        skullFrameIndex += 1
        if skullFrameIndex >= len(skullFrames):
            skullFrameIndex = 0
        skull = skullFrames[skullFrameIndex]

    if event.type == reaperAnimationTimer:
        reaperFrameIndex += 1
        if reaperFrameIndex >= len(reaperFrames):
            reaperFrameIndex = 0
        reaper = reaperFrames[reaperFrameIndex]


def enemyMover(enemyList):

    if enemyList:

        for enemy in enemyList:

            enemy.x -= 3

            if enemy.bottom == 500:
                screen.blit(skull,enemy)
            else:
                screen.blit(reaper,enemy)

        enemyList = [enemy for enemy in enemyList if enemy.x > -100]

        return enemyList

    else:
        return []

# =============================
# MAIN LOOP
# =============================

running = True

while running:

    screen.blit(background,(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == "game":
            enemySpawner(event)

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if state == "menu":
                if play_button.clicked(mouse_pos):
                    state = "mode"

            elif state == "mode":

                if easy_button.clicked(mouse_pos):
                    print("Easy Mode")
                    state = "game"

                if medium_button.clicked(mouse_pos):
                    print("Medium Mode")
                    state = "game"

                if hard_button.clicked(mouse_pos):
                    print("Hard Mode")
                    state = "game"

    # =============================
    # MENU
    # =============================

    if state == "menu":

        title_rect = title_img.get_rect(center=(WIDTH//2,200))
        screen.blit(title_img,title_rect)

        play_button.draw()

    # =============================
    # MODE SELECT
    # =============================

    elif state == "mode":

        text = font.render("Please Select The Mode", True, (255,255,255))
        text_rect = text.get_rect(center=(WIDTH//2, 250))
        screen.blit(text, text_rect)

        easy_button.draw()
        medium_button.draw()
        hard_button.draw()

    # =============================
    # GAME
    # =============================

    elif state == "game":

        text = font.render("Game Started!",True,(255,255,255))
        screen.blit(text,(20,20))

        enemyRectList = enemyMover(enemyRectList)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()