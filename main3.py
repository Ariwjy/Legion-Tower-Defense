import pygame
import sys

pygame.init()

# Window
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font("assets/font/Pixeltype.ttf", 32)

# Difficulty default
enemySpeed = 2
spawnRate = 2000

# Load Images
background = pygame.image.load("assets/image/background.png")
title_img = pygame.image.load("assets/image/icons/title.png")

play_img = pygame.image.load("assets/image/icons/play.png")
easy_img = pygame.image.load("assets/image/icons/easymodebutton.png")
medium_img = pygame.image.load("assets/image/icons/mediummodebutton.png")
hard_img = pygame.image.load("assets/image/icons/hardmodebutton.png")

bridgeMap = pygame.image.load("assets/image/maps/bridge.jpg")
castleMap = pygame.image.load("assets/image/maps/castle map thing.jpg")
longMap = pygame.image.load("assets/image/maps/easy fodder baby map.jpg")
anotherBrickMap = pygame.image.load("assets/image/maps/literally another brick.jpg")
blonsMap = pygame.image.load("assets/image/maps/literally blons.jpg")

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

# =============================
# ENEMY DATA
# =============================

enemyRectList = []
enemyType = []
enemyPathIndex = []
enemyDistance = []
enemyDirection = []

spawnToggle = 0

# =============================
# PATH
# =============================

PATH = [
("up",100),
("right",410),
("up",230),
("left",80),
("up",75),
("left",330),
("down",75),
("left",180),
("down",75),
("left",100)
]

# =============================
# TIMER
# =============================

enemySpawnTimer = pygame.USEREVENT + 1
pygame.time.set_timer(enemySpawnTimer, spawnRate)

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
medium_button = Button(medium_img, 425, 350)
hard_button = Button(hard_img, 550, 350)

bridgeMapButton = Button(bridgeMap, 550, 100)
# =============================
# ENEMY SPAWNER
# =============================

def enemySpawner(event):
    print(hard_img.get_width())
    print(medium_img.get_width())
    print(hard_img.get_height())
    print(medium_img.get_height())
    global skullFrameIndex,reaperFrameIndex,skull,reaper,spawnToggle

    if event.type == enemySpawnTimer:

        if spawnToggle == 0:

            rect = skull.get_rect(midbottom=(320,600))
            enemyRectList.append(rect)
            enemyType.append("skull")
            enemyDirection.append("right")
            spawnToggle = 1

        else:

            rect = reaper.get_rect(midbottom=(320,600))
            enemyRectList.append(rect)
            enemyType.append("reaper")
            enemyDirection.append("right")
            spawnToggle = 0

        enemyPathIndex.append(0)
        enemyDistance.append(0)

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


# =============================
# ENEMY MOVEMENT
# =============================

def enemyMover(enemyList):

    speed = enemySpeed

    for i,enemy in enumerate(enemyList):

        path_index = enemyPathIndex[i]
        direction, distance = PATH[path_index]

        if direction == "left":
            enemy.x -= speed
            enemyDistance[i] += speed
            enemyDirection[i] = "right"

        if direction == "right":
            enemy.x += speed
            enemyDistance[i] += speed
            enemyDirection[i] = "left"

        if direction == "up":
            enemy.y -= speed
            enemyDistance[i] += speed

        if direction == "down":
            enemy.y += speed
            enemyDistance[i] += speed

        if enemyDistance[i] >= distance:

            enemyDistance[i] = 0

            if enemyPathIndex[i] < len(PATH)-1:
                enemyPathIndex[i] += 1

        # pilih sprite
        if enemyType[i] == "skull":
            sprite = skull
        else:
            sprite = reaper

        # flip jika menghadap kiri
        if enemyDirection[i] == "left":
            sprite = pygame.transform.flip(sprite, True, False)

        screen.blit(sprite,enemy)

    return enemyList


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
                if play_button.clicked(mouse_pos):
                    state = "map"

            elif state == "mode":

                if easy_button.clicked(mouse_pos):
                    enemySpeed = 2
                    spawnRate = 2000
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "game"

                if medium_button.clicked(mouse_pos):
                    enemySpeed = 3
                    spawnRate = 1400
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "game"

                if hard_button.clicked(mouse_pos):
                    enemySpeed = 4
                    spawnRate = 900
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "game"

    # MENU
    if state == "menu":

        title_rect = title_img.get_rect(center=(WIDTH//2,200))
        screen.blit(title_img,title_rect)

        play_button.draw()

    # MODE SELECT
    elif state == "mode":

        text = font.render("Please Select The Mode", True, (255,255,255))
        text_rect = text.get_rect(center=(WIDTH//2, 250))
        screen.blit(text, text_rect)

        easy_button.draw()
        medium_button.draw()
        hard_button.draw()

    elif state == "map":
        text = font.render("Please select a map", True, (255, 255, 255))
        screen.blit(text, (20,20))
    # GAME
    elif state == "game":

        text = font.render("Game Started!",True,(255,255,255))
        screen.blit(text,(20,20))

        enemyRectList = enemyMover(enemyRectList)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()