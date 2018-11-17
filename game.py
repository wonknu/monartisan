import pygame, sys, random
from pygame.locals import *

BLACK=(0, 0, 0)
BROWN=(153, 76, 0)
GREEN=(0, 255, 0)
BLUE=(0, 0, 255)
WHITE=(255, 255, 255)

DIRT=0
GRASS=1
WATER=2
COAL=3
CLOUD=4

textures =   {
  DIRT: pygame.image.load('images/dirt.jpg'),
  GRASS: pygame.image.load('images/grass.jpg'),
  WATER: pygame.image.load('images/water.jpg'),
  COAL: pygame.image.load('images/coal.jpg'),
  CLOUD: pygame.image.load('images/cloud.png')
}

inventory = {
  DIRT: 0,
  GRASS: 0,
  WATER: 0,
  COAL: 0
}

TILESIZE=40
MAPWIDTH=15
MAPHEIGHT=10

cloudx=-200
cloudy=random.randint(0, MAPHEIGHT*TILESIZE)
cloudyCount=random.randint(100, 200)
cloudyDirection=0

resources = [DIRT,GRASS,WATER,COAL]

tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

for rw in range(MAPHEIGHT):
  for cl in range(MAPWIDTH):
    randomNumber = random.randint(0,15)
    if randomNumber == 0: tile = COAL
    elif randomNumber == 1 or randomNumber == 2: tile = WATER
    elif randomNumber >= 3 and randomNumber <= 7: tile = GRASS
    else: tile = DIRT
    tilemap[rw][cl] = tile

pygame.init()
pygame.display.set_caption('M I N E C R A F T -- 2 D')
pygame.display.set_icon(pygame.image.load('images/player.png'))

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50))
PLAYER = pygame.image.load('images/player.png').convert_alpha()
playerPos = [0, 0]

INVFONT = pygame.font.Font('fonts/FreeSansBold.ttf', 18)

controls = {
  DIRT: 304,
  GRASS: 38,
  WATER: 160,
  COAL: 34
}

fpsClock = pygame.time.Clock()

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == KEYDOWN:
      print(event)
      if (event.key == K_RIGHT): playerPos[0] += 1
      if (event.key == K_LEFT): playerPos[0] -= 1
      if (event.key == K_DOWN): playerPos[1] += 1
      if (event.key == K_UP): playerPos[1] -= 1
      if event.key == K_SPACE:
        currentTile = tilemap[playerPos[1]][playerPos[0]] # what resource is the player standing on?
        inventory[currentTile] += 1 # player now has 1 more of this resource
        tilemap[playerPos[1]][playerPos[0]] = DIRT # the player is now standing on dirt
      if (event.key == K_w):
        currentTile = tilemap[playerPos[1]][playerPos[0]]
        if inventory[DIRT] > 0:
          inventory[DIRT] -= 1
          tilemap[playerPos[1]][playerPos[0]] = DIRT
          inventory[currentTile] += 1
      if (event.key == K_x):
        currentTile = tilemap[playerPos[1]][playerPos[0]]
        if inventory[GRASS] > 0:
          inventory[GRASS] -= 1
          tilemap[playerPos[1]][playerPos[0]] = GRASS
          inventory[currentTile] += 1
      if (event.key == K_c):
        currentTile = tilemap[playerPos[1]][playerPos[0]]
        if inventory[WATER] > 0:
          inventory[WATER] -= 1
          tilemap[playerPos[1]][playerPos[0]] = WATER
          inventory[currentTile] += 1
      if (event.key == K_v):
        currentTile = tilemap[playerPos[1]][playerPos[0]]
        if inventory[COAL] > 0:
          inventory[COAL] -= 1
          tilemap[playerPos[1]][playerPos[0]] = COAL
          inventory[currentTile] += 1

  for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
      DISPLAYSURF.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

  DISPLAYSURF.blit(PLAYER, (playerPos[0]*TILESIZE, playerPos[1]*TILESIZE))

  # display the cloud
  DISPLAYSURF.blit(textures[CLOUD].convert_alpha(),(cloudx,cloudy))
  # move the cloud to the left slightly
  if cloudyCount <= 0: 
    cloudyCount=random.randint(100, 200)
    if random.randint(0, 1) == 0: cloudyDirection=-0.1
    else: cloudyDirection=0.1
  cloudx+=1
  cloudy+=cloudyDirection
  cloudyCount -= 1
  # if the cloud has moved past the map
  if cloudx > MAPWIDTH*TILESIZE: # pick a new position to place the cloud
    cloudy = random.randint(0, MAPHEIGHT*TILESIZE)
    cloudx = -200

  placePosition = 10 # display the inventory, starting 10 pixels in
  for item in resources:
    DISPLAYSURF.blit(textures[item], (placePosition, MAPHEIGHT*TILESIZE+20)) # add the image
    placePosition += 30
    # add the text showing the amount in the inventory
    textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
    DISPLAYSURF.blit(textObj, (placePosition, MAPHEIGHT*TILESIZE+20)) 
    placePosition += 50

  pygame.display.update()
  fpsClock.tick(24)
