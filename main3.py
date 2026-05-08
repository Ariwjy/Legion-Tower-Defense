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

# Declaration part thingamajig
global mapChosen
mapChosen = None

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

wizard = pygame.image.load("assets/image/icons/witchguycopy.png")
wizardTower = pygame.transform.scale(wizard, (50, 50))
knight = pygame.image.load("assets/image/icons/knightcopy.png")
knightTower = pygame.transform.scale(knight, (50, 50))
shopIconTemp = pygame.image.load("assets/image/icons/shop icon.png")
shopIcon = pygame.transform.scale(shopIconTemp, (150, 96.47))
shopPanelTemp = pygame.image.load("assets/image/icons/shop panel.png")
shopPanel = pygame.transform.scale(shopPanelTemp, (200, 600))
bridgeMapButtonSizedDown = pygame.transform.scale(bridgeMap, (160, 90))
castleMapButtonSizedDown = pygame.transform.scale(castleMap, (160, 90))
longMapButtonSizedDown = pygame.transform.scale(longMap, (160, 90))
anotherBrickMapButtonSizedDown = pygame.transform.scale(anotherBrickMap, (160, 90))
blonsMapButtonSizedDown = pygame.transform.scale(blonsMap, (160, 90))

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
enemySpawnPosX = []
enemySpawnPosY = []
spawnToggle = 0

# =============================
# TOWER DATA
# =============================

towers = []
dragPos = (0, 0)
# =============================
# PATH
# =============================

PATH = [

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
isShopOpen = False
isDraggingATower = False
# =============================
# BUTTON CLASS
# =============================

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))

    def draw(self):
        screen.blit(self.image, self.rect)
        # print("shop drawn")

    def clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    # def moveShopButton(self):
    #     screen.blit(self.image, (630, 480))
    
class MapButton:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))

    def mapDraw(self):
        screen.blit(self.image, self.rect)

    def mapClicked(self,pos):
        return self.rect.collidepoint(pos)
    
class Tower:
    def __init__(self, x, y, tower, range):
        self.image = tower
        self.x = x
        self.y = y
        self.range = range
        # self.firerate = firerate
        # self.damage = damage
        self.rect = self.image.get_rect(center=(x, y))

    def drawTower(self):
        self.rect.center=(self.x, self.y)
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, (0, 0, 200), (self.x, self.y), self.range, 5)
    


# Buttons
play_button = Button(play_img, 375, 350)

easy_button = Button(easy_img, 300, 350)
medium_button = Button(medium_img, 425, 350)
hard_button = Button(hard_img, 550, 350)

wizardTowerButton = Button(wizardTower, 720, 80)
knightTowerButton = Button(knightTower, 710, 130)
# 
shopButton = Button(shopIcon, 10, 480)
# if isShopOpen:
#     shopButton.moveShopButton

bridgeMapButton = MapButton(bridgeMapButtonSizedDown, 200, 100)
castleMapButton = MapButton(castleMapButtonSizedDown, 400, 100)
longMapButton = MapButton(longMapButtonSizedDown, 600, 100)
anotherBrickMapButton = MapButton(longMapButtonSizedDown, 200, 230)
blonsMapButton = MapButton(blonsMapButtonSizedDown, 400, 230)
# =============================
# ENEMY SPAWNER
# =============================

def enemySpawner(event):
    # print(hard_img.get_width())
    # print(medium_img.get_width())
    # print(hard_img.get_height())
    # print(medium_img.get_height())
    global skullFrameIndex,reaperFrameIndex,skull,reaper,spawnToggle, enemySpawnPosX, enemySpawnPosY, spawnPosX, spawnPosY

    spawnPosX = enemySpawnPosX[0]
    spawnPosY = enemySpawnPosY[0]
    
    if event.type == enemySpawnTimer:

        if spawnToggle == 0:

            rect = skull.get_rect(midbottom=(spawnPosX, spawnPosY))
            enemyRectList.append(rect)
            enemyType.append("skull")
            enemyDirection.append("right")
            spawnToggle = 1

        else:

            rect = reaper.get_rect(midbottom=(spawnPosX, spawnPosY))
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
    
    if mapChosen == None:
        screen.blit(background,(0,0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == "game":
            screen.blit(mapChosen, (0, 0))
            enemySpawner(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if shopButton.clicked(mouse_pos):
                    isShopOpen = not isShopOpen
                
                elif isShopOpen and wizardTowerButton.clicked(mouse_pos):
                    isDraggingATower = True
                    towerDragged = "wizard"
                
                elif isShopOpen and knightTowerButton.clicked(mouse_pos):
                    isDraggingATower = True
                    towerDragged = "knight"
                
            elif event.type == pygame.MOUSEMOTION:
                dragPos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                if isDraggingATower and towerDragged == "knight":
                    towers.append(Tower(dragPos[0], dragPos[1], knightTower, 50))
                    isDraggingATower = False
                
                elif isDraggingATower and towerDragged == "wizard":
                    towers.append(Tower(dragPos[0], dragPos[1], wizardTower, 300))
                    isDraggingATower = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if state == "menu":
                if play_button.clicked(mouse_pos):
                    state = "mode"

            elif state == "mode":
                if easy_button.clicked(mouse_pos) or medium_button.clicked(mouse_pos) or hard_button.clicked(mouse_pos):
                    state = "map"

            elif state == "mode":

                if easy_button.clicked(mouse_pos):
                    enemySpeed = 2
                    spawnRate = 2000
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "map"

                if medium_button.clicked(mouse_pos):
                    enemySpeed = 3
                    spawnRate = 1400
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "map"

                if hard_button.clicked(mouse_pos):
                    enemySpeed = 4
                    spawnRate = 900
                    pygame.time.set_timer(enemySpawnTimer, spawnRate)
                    state = "map"

            elif state == "map":

                if bridgeMapButton.mapClicked(mouse_pos):
                    PATH.append(("up", 100))
                    PATH.append(("right", 200))
                    enemySpawnPosX.append(100)
                    enemySpawnPosY.append(200)
                    state = "game"
                    mapChosen = bridgeMap
                

                elif castleMapButton.mapClicked(mouse_pos):
                    PATH.append(("up", 150))
                    PATH.append(("left", 300))
                    enemySpawnPosX.append(460)
                    enemySpawnPosY.append(600)
                    state = "game"
                    mapChosen = castleMap
                
                elif longMapButton.mapClicked(mouse_pos):
                    PATH.append(("up", 100))
                    enemySpawnPosX.append(700)
                    enemySpawnPosY.append(350)
                    state = "game"
                    mapChosen = longMap
                
                elif anotherBrickMapButton.mapClicked(mouse_pos):
                    PATH.append(("up", 100))
                    enemySpawnPosX.append(100)
                    enemySpawnPosY.append(100)
                    state = "game"
                    mapChosen = anotherBrickMap
                
                elif blonsMapButton.mapClicked(mouse_pos):
                    PATH.append(("up", 100))
                    enemySpawnPosX.append(100)
                    enemySpawnPosY.append(100)
                    state = "game"
                    mapChosen = blonsMap



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
    #map select
    elif state == "map":
        text = font.render("Please select a map", True, (255, 255, 255))
        screen.blit(text, (20,20))

        bridgeMapButton.mapDraw()
        castleMapButton.mapDraw()
        longMapButton.mapDraw()
        anotherBrickMapButton.mapDraw()
        blonsMapButton.mapDraw()
    # GAME
    elif state == "game":
        # print("<>")
        text = font.render("Game Started!",True,(255,255,255))
        screen.blit(text,(20,20))

        enemyRectList = enemyMover(enemyRectList)
    
        shopButton.draw()

        if isShopOpen:
            screen.blit(shopPanel, (700, 0))
            wizardTowerButton.draw()
            knightTowerButton.draw()
        
        for tower in towers:
            tower.drawTower()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
