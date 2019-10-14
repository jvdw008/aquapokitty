# Copyright Blackjet in 2019
# Graphics done using Aseprite
# Sfx done using BFXR and Audacity
# Code, music, sfx, graphics by Jaco van der Walt

# The source code in this file is released under the GNU GPL V3 license.
# Go to https://choosealicense.com/licenses/gpl-3.0/ for the full license details.

import upygame as pygame
import urandom as random
import umachine                             # For on-screen text
import graphics		                        # Graphics
import sounds
from audio import Audio                     # Audio class to play sounds
from player import Player                   # Player class
from animation import Animation as Anim     # Animation cass for fish, coins, player etc
from flashtext import Text                  # On-screen text for important messages in-game
from shake import Shake                     # Screen-shake, to be used for explosions etc
from enemy import Enemy                     # Normal enemy class
from bullets import Bullet                  # Bullet class
from explosion import Explosion             # Explodey bits
from kittens import Kitty                   # Station kitties

# Check RAM use
import gc
gc.collect()

# Setup the screen buffer
pygame.display.init(False)

# Set colours in RGB formatted tuples
pygame.display.set_palette_16bit([
    000000, 0xffff, 0x267b, 0x2516, 0x2391, 0x220c, 0xce40, 0xc940, 0x88a0, 0xc817, 0x8810, 0x8c91, 0x4228, 0x18e3, 0xd320, 0x9220
    
]);

# default mode of 110x88 @16 cols
screen = pygame.display.set_mode()

# Init audio
g_sound = pygame.mixer.Sound()

# Test for real h/w to prevent simulator from hanging
gpioPin = umachine.Pin ( umachine.Pin.EXT2, umachine.Pin.ANALOG_IN )
gpioPinValue = gpioPin.value()
if(gpioPinValue == 0):
    isThisRealHardware = False
    menuSong = ""
    gameSong = ""
    pauseSong = ""
else:
    isThisRealHardware = True
    menuSong = "folder/menuSong.wav"
    gameSong = "folder/gameSong.wav"

# Version number of current game build
version = 16

# Constants
STATE_MENU = 0
STATE_INSTRUCTIONS = 1
STATE_GAME = 2

# Variables
waitOnLoad = 50                                     # Use this to prevent A starting the game before player knopws when game just loaded
gameState = STATE_MENU                              # Menu or game
gameOver = False                                    # User to display everything but prevent player from moving
pauseGame = False                                   # Boolean for pausing the game
showInstructions = False                            # For showing instructions on menu screen
screenWidth = 110                                   # Width of screen mode
level = 0                                           # The level of the game
levelComplete = False
score = 0                                           # Player score
kittyScore = 10                                     # This is the amoutn of score being added by a kitty
kittyScoreTimerMax = 50                             # The timer value for scoring kitty
kittyScoreTimer = kittyScoreTimerMax                # The current timer value
lives = 5
logoX = 8
logoY = 10
logoDir = 1
logoPauseCtr = 1
logoPause = 0
playerPos = [50, 30]                                # Player start position
playerFlashing = False                              # If player took damage, gives some reprieve
playerFlashTimerMax = 20
playerFlashTimer = playerFlashTimerMax              # Duration of reprieve
upPressed = False                                   # Modifiers for dpad
downPressed = False                                 # As above
leftPressed = False                                 # As above
rightPressed = False                                # As above
aPressed = False                                    # As above
bPressed = False                                    # As above
cPressed = False                                    # As above
musicPlaying = False                                # Toggle for music
flashTextTimer = 60                                 # On-screen text timer
gameOverPlayed = False                              # Trigger to pay gameover sound when dead
getReadyPlayed = False
gameOVerTimer = 50
powerShots = 5                                      # replenish after waiting
powerShotsCounterMax = 10                           # Used to count down the build-up of powershots
powerShotsCounter = powerShotsCounterMax            # As above
screenXOffset = 0                                   # Used to immitate scrolling
mapPosition = 0                                     # Used to set where objects are in relation to the player and map
mapSize = 440                                       # 4 screens wide
enemyList = []                                      # List of enemies per level
explosionList = []                                  # List of explosions
popList = []                                        # List of bullet pop explosions
playerBullets = []                                  # List of bullets
momentumMax = 1                                     # Used to add inertia to player ship
currentMomentum = 0
currentY = 0
keySideways = True                                  # For checking keypresses
keyVertical = True                                  # As above
shipMoveSpeed = 3                                   # Playership moving speed
milkStations = []                                   # List of milk stations for levels
kittyList = []                                      # List of kitties
dropItem = []                                       # Value of a dropped item; 0 = nothing, 1 = bomb, 2 = bonus, 3 = left
sunPos = 50                                         # X position of sun
sunCountMax = 50
sunFrameSkipCounter = sunCountMax                   # The speed at which the sun moves
waveX = 0
cloudsPos = 0
cloudCountMax = 10
cloudFrameSkipCounter = cloudCountMax
kittyBoatX = 30
kittyBoatY = 6
instructions = ["      Move using D-Pad", "        Shoot with (A)", "    Power shoot with (B)", "", "   Collect dropped items:", "", "          extra life", "", "          bonus", "", "          explode enemies", "          on screen"]

# Graphics
gameBg = graphics.g_background.bg01
sun = graphics.g_background.sun
mountains = graphics.g_background.mountains
clouds = graphics.g_background.clouds
playerShip = graphics.g_player.playerShip
playerNormalBullet = graphics.g_bullets.playerBullet
playerFastBullet = graphics.g_bullets.playerPowerBullet
powerBulletBar = [graphics.g_interface.powerbar_full, graphics.g_interface.powerbar_empty]
life = [graphics.g_interface.heart_empty, graphics.g_interface.heart_full]
interface = graphics.g_interface.interface
logo = graphics.g_interface.logo
gameoverBG = graphics.g_background.gameover
levelCompleteBG = graphics.g_background.levelcomplete
oceanWaves = [graphics.g_background.wave01, graphics.g_background.wave02, graphics.g_background.wave03]
milkStation = graphics.g_milkstation.milkStation
kittyboat = graphics.g_background.boat
kitty = graphics.g_milkstation.kitty
enemy01 = graphics.g_enemies.enemy01
enemy02 = graphics.g_enemies.enemy02
enemy03 = graphics.g_enemies.enemy03
enemy04 = graphics.g_enemies.enemy04
enemy05 = graphics.g_enemies.enemy05
enemy06 = graphics.g_enemies.enemy06
enemyShips = [enemy01, enemy02, enemy03, enemy04, enemy05, enemy06]
bulletImages = [graphics.g_bullets.enemyBullet, graphics.g_bullets.enemyBullet02, graphics.g_bullets.playerBullet, graphics.g_bullets.playerPowerBullet]
dropImages = [graphics.g_drops.drop_bomb, graphics.g_drops.drop_bonus, graphics.g_drops.drop_life]
explosionFrames = [graphics.g_explosion.explode01, graphics.g_explosion.explode02, graphics.g_explosion.explode03, graphics.g_explosion.explode04, graphics.g_explosion.explode05, graphics.g_explosion.explode06, graphics.g_explosion.explode07, graphics.g_explosion.explode08, graphics.g_explosion.explode09]
popFrames = [graphics.g_explosion.pop01, graphics.g_explosion.pop02, graphics.g_explosion.pop03, graphics.g_explosion.pop04, graphics.g_explosion.pop05]

# Init classes
player = Player(playerPos[0], playerPos[1], 20, 75, 1)
audio = Audio(g_sound)

waves = Anim(oceanWaves, 8)
# Animation setup - Array of graphic images and the speed of the animation (lower = faster)
#playerAnimTurnLeft = Anim([graphics.g_player., graphics.g_player., graphics.g_player.], 4)
#playerAnimTurnRight = Anim([graphics.g_player., graphics.g_player., graphics.g_player.], 4)

print ("free",gc.mem_free())

#################################################################################################################
# Init Game
#################################################################################################################
def startLevel(level):
    global enemyList, enemyShips, milkStations, kittyList, dropItem, kittyBoatX, levelComplete
    
    enemyList = []
    milkStations = []
    kittyList = []
    dropItem = []
    levelComplete = False
    gc.collect()
    
    # Enemy type sizes:
    # 1 - 12 x 14
    # 2 - 12 x 12
    # 3 - 20 x 17
    # 4 - 18 x 18
    # 5 - 20 x 47
    # 6 - 24 x 23
    sizeType = [[12,14], [12,12], [20,17], [18,18], [20,47], [24,23]]
    
    if level == 0:
        enemyTypes = [2,3,4,5]
        milkStations = [50] # x, y, kitties  (if 0, you lose this station)
        
    elif level == 1:
        enemyTypes = [0,0,0,1,1,1,0]
        milkStations = [50, 200]
        
    elif level == 2:
        enemyTypes = [0,1,0,1,0,1,0,1,0,1]
        milkStations = [80, 250, 350]
        
    elif level == 3:
        enemyTypes = [0,0,0,1,1,1,0,0,2,2]
        milkStations = [100, 200, 300]
        
    elif level == 4:
        enemyTypes = [0,0,1,1,2,2,0,3,2,1]
        milkStations = [50, 100, 350]
        
    elif level == 5:
        enemyTypes = [0,1,2,3,4,3,2,1,0,0]
        milkStations = [100, 150, 250]
        
    else:
        enemyTypes = [0,1,2,3,4,5,4,3,2,1]
        milkStations = [random.getrandbits(7) + 50, random.getrandbits(7) + 150, random.getrandbits(7) + 250]
    
    # Set boat above first pump
    kittyBoatX = milkStations[0]
    
    for i in range(len(enemyTypes)):
        # x, y, shooting, image, type, direction, directionY
        tmpX = random.getrandbits(7) + 200
        tmpY = random.getrandbits(5) + 20
        tmpDirX = random.getrandbits(1)
        if tmpDirX != 1:
            tmpDirX = -1
        tmpDirY = random.getrandbits(1)
        if enemyTypes[i] == 3:
            tmpDirY = 1
        
        enemyList.append(Enemy(tmpX, tmpY, False, enemyShips[enemyTypes[i]], enemyTypes[i], tmpDirX, tmpDirY, sizeType[enemyTypes[i]][0], sizeType[enemyTypes[i]][1]))
        
    for i in range(len(milkStations)):
        kittyList.append(Kitty(milkStations[i], 74)) #x, y

#################################################################################################################
# Reset for new game
#################################################################################################################
def resetGame():
    global gameOver, lives, score, playerPos, level, player, dropItem, playerFlashing, screenXOffset, gameOVerTimer, getReadyPlayed, gameOverPlayed
    
    getReadyPlayed = False
    gameOverPlayed = False
    gameOver = False
    gameOVerTimer = 50
    lives = 5
    score = 0
    playerPos = [50, 30]
    player.setPlayerPos(playerPos[0], playerPos[1])
    level = 0
    dropItem = []
    playerFlashing = False
    screenXOffset = 0
    
    startLevel(level)

#################################################################################################################
# Update method
#################################################################################################################
def update():
    global sunPos, sunFrameSkipCounter, sunCountMax, powerShots, powerShotsCounter, powerShotsCounterMax, logoX, logoY, logoDir, logoPauseCtr, logoPause, cloudsPos, cloudCountMax, cloudFrameSkipCounter, waveX, gameOVerTimer
    global keySideways, keyVertical, screenXOffset, screenWidth, playerBullets, currentMomentum, currentY, mapPosition, mapSize, milkStations, score, kittyScore, kittyScoreTimerMax, kittyScoreTimer, level, levelComplete, getReadyPlayed
    global aPressed, bPressed, cPressed, bulletImages, explosionList, explosionFrames, popList, popFrames, lives, playerFlashing, playerFlashTimer, playerFlashTimerMax, dropItem, kittyBoatX, kittyBoatY, gameOver, waitOnLoad, gameOverPlayed

    if gameState == STATE_MENU:
        if logoPauseCtr > 0:
            if logoPause > 0:
                logoPause -= 1
            else:
                logoPause = 3
                logoPauseCtr -= 1
                if logoDir > 0:
                    logoY += logoDir - logoPauseCtr
                else:
                    logoY += logoDir + logoPauseCtr
        else:
            logoPauseCtr = 5
            logoDir = -logoDir
            
    elif gameState == STATE_GAME:
        # Horizontal momentum
        if keySideways:
            if currentMomentum != 0:
                if currentMomentum > 0:
                    currentMomentum -= 1
                else:
                    currentMomentum += 1
                    
        # Vertical momentum
        if keyVertical:
            if currentY != 0:
                if currentY > 0:
                    currentY -= 1
                else:
                    currentY += 1
    
        # Player updates
        if not gameOver:
            player.movePlayer(currentY)
            player.updateTimer()
            
        # BG offset
        screenXOffset += currentMomentum
        
        # Map offset
        if currentMomentum != 0:
            mapPosition -= currentMomentum
            if mapPosition > mapSize:
                mapPosition = 0
                
            if mapPosition < 0:
                mapPosition = mapSize
    
        # Udate bg position
        if screenXOffset > screenWidth:
            screenXOffset = 0
        elif screenXOffset < -screenWidth:
            screenXOffset = 0
        
        playerPos = player.getPlayerPos()
        playerX = playerPos[0]
        playerY = playerPos[1]
        
        # Sun offset
        if sunFrameSkipCounter > 0:
            sunFrameSkipCounter -= 1
        else:
            sunPos += 1
            sunFrameSkipCounter = sunCountMax
        sunPos += currentMomentum
        if sunPos > mapSize - screenWidth:
            sunPos = -screenWidth
        
        if sunPos < -mapSize + screenWidth:
            sunPos = screenWidth
            
        # Cloud offset
        if cloudFrameSkipCounter > 0:
            cloudFrameSkipCounter -= 1
        else:
            cloudsPos -= 1
            cloudFrameSkipCounter = cloudCountMax
        cloudsPos += currentMomentum
        if cloudsPos > mapSize - screenWidth:
            cloudsPos = -screenWidth
        
        if cloudsPos < -mapSize + screenWidth:
            cloudsPos = screenWidth
        
        # Update waves
        waves.update()
        waveX += currentMomentum
        if waveX > screenWidth:
            waveX = -screenWidth
        
        if waveX < -screenWidth:
            waveX = screenWidth
            
        # Update kitty boat
        kittyBoatX += currentMomentum
        if kittyBoatX > mapSize - screenWidth:
            kittyBoatX = -screenWidth
        
        if kittyBoatX < -mapSize + screenWidth:
            kittyBoatX = screenWidth
        
        ######################################
        # Update milkstation positions
        ######################################
        for i in range(len(milkStations)):
            if currentMomentum != 0:
                milkStations[i] += currentMomentum
                if milkStations[i] > mapSize - screenWidth:
                    milkStations[i] = -screenWidth
                    
                if milkStations[i] < -mapSize + screenWidth:
                    milkStations[i] = screenWidth
                    
        ######################################
        # Check if bullet needs to be made
        ######################################
        if aPressed:
            aPressed = False
                
            if not gameOver and not levelComplete:
                if len(playerBullets) < 5:
                    tmpPlayDir = player.getDirection()
                    if tmpPlayDir > 0:
                        tmpBulX = 15
                    else:
                        tmpBulX = -1
                    tmpBylY = 5
                    playerBullets.append(Bullet(playerX + tmpBulX, playerY + tmpBylY, tmpPlayDir, 5, 2, bulletImages[2])) # x, y, direction, speed, type, image
                    if not getReadyPlayed:
                        getReadyPlayed = True
                        audio.playSfx(sounds.getready8b)
                    else:
                        audio.playSfx(sounds.playerShoot8b)
        
        ######################################
        # Check if powershot needs to be made
        ######################################
        if bPressed:
            bPressed = False
            if powerShots > 0:
                tmpPlayDir = player.getDirection()
                if tmpPlayDir > 0:
                    tmpBulX = 15
                else:
                    tmpBulX = -1
                tmpBylY = 5
                playerBullets.append(Bullet(playerX + tmpBulX, playerY + tmpBylY, tmpPlayDir, 5, 3, bulletImages[3]))
                audio.playSfx(sounds.powerShot8b)
                
        else:
            # Otherwise, build it back up
            if powerShots < 5:
                if powerShotsCounter > 0:
                    powerShotsCounter -= 1
                else:
                    # Reset counter
                    powerShotsCounter = powerShotsCounterMax
                    powerShots += 1
                    if powerShots > 5:
                        powerShots = 5
                        
        ######################################
        # Update explosion
        ######################################
        tmpId = 0
        tmpCtr = 0
        for explody in explosionList:
            tmpId += 1
            if explody.getFrame() >= len(explosionFrames):
                tmpCtr = tmpId
                break
            
            explody.update(currentMomentum)
    
        # Delete explosion object
        if tmpCtr > 0:
            del explosionList[tmpCtr - 1]
            gc.collect()
        
        ######################################
        # Has bullet reached its limit?
        ######################################
        tmpId = 0
        tmpCtr = 0
        for playerBullet in playerBullets:
            tmpId += 1
            if not playerBullet.update(currentMomentum):
                tmpCtr = tmpId
                break
        
        # Delete bullet
        if tmpCtr > 0:
            # Create pop explosion
            popPos = playerBullets[tmpCtr - 1].getPosition()
            popList.append(Explosion(popPos[0], popPos[1], len(popFrames)))
            del playerBullets[tmpCtr - 1]
            gc.collect()
        
        ######################################
        # Update pops
        ######################################
        tmpId = 0
        tmpCtr = 0
        for pops in popList:
            tmpId += 1
            if pops.getFrame() >= len(popFrames):
                tmpCtr = tmpId
                break
            
            pops.update(currentMomentum)
    
        # Delete pop object
        if tmpCtr > 0:
            del popList[tmpCtr - 1]
            gc.collect()
            
        ######################################
        # Enemy updates
        ######################################
        tmpEnemyId = 0
        tmpBullet = 0
        bulDir = 0
        for enemy in enemyList:
            tmpEnemyId += 1
            
            # Get enemy pos
            tmpEnemyPos = enemy.getPos()
            # Get enemy direction
            tmpDir = enemy.getDirection()
            
            # Update movements - pass in the player momentum to adjust the enemy x pos
            enemy.update(playerX, playerY, mapSize, currentMomentum, screenWidth)
            
            # Chase kittehs
            if enemy.getType() == 2:
                for kitteh in kittyList:
                    kittehPos = kitteh.getPos()
                    if enemy.trackKitteh(kittehPos[0], kittehPos[1]):
                        kitteh.setAbductedState(True)
                        break
            
            # Update enemy shooting if relevant
            if abs(tmpEnemyPos[0] - playerX) < 40:
                if not enemy.getShooting():
                    tmpBylY = enemy.getHeight() // 2
                    if playerX < tmpEnemyPos[0]:
                        bulDir = -1
                        tmpBulX = -1
                    else:
                        bulDir = 1
                        tmpBulX = 15
                    # x, y, direction, speed, type, image
                    playerBullets.append(Bullet(tmpEnemyPos[0] + tmpBulX, tmpEnemyPos[1] + tmpBylY, bulDir, 3, 0, bulletImages[0]))
                    enemy.setShooting(True)
                    audio.playSfx(sounds.enemyShoot8b)
                    
            else:
                # Reset shooting
                enemy.setShooting(False)
        
            # Has player bullet hit enemy?
            tmpId = 0
            for playerBullet in playerBullets:
                tmpId += 1
                tmpHeight = enemy.getHeight()
                tmpWidth = enemy.getWidth()
                if playerBullet.getType() != 0 and playerBullet.getType() != 1: # Ignore enemy to enemy collision
                    if playerBullet.checkCollision(tmpEnemyPos[0], tmpEnemyPos[1], tmpWidth, tmpHeight):
                        tmpBullet = tmpId
                        tmpEn = tmpEnemyId
                        tmpBullPos = playerBullet.getPosition()
                        explosionList.append(Explosion(tmpBullPos[0], tmpBullPos[1], len(explosionFrames)))
                        audio.playSfx(sounds.takeHit8b)
                        # Change enemy direction if player shot it and it's type 4 (large one)
                        if enemy.getType() == 4:
                            if playerX < tmpEnemyPos[0] and tmpDir == 1 or playerX > tmpEnemyPos[0] and tmpDir == -1:
                                enemy.setDirection(-enemy.getDirection())
                        break
                    
                else:
                    # Has enemy bullet hit player?
                    if player.getHitTimer() == 0:
                        if playerBullet.checkCollision(playerX, playerY, 18, 11):
                            tmpBullet = tmpId
                            tmpEn = tmpEnemyId
                            tmpBullPos = playerBullet.getPosition()
                            if lives > 1:
                                lives -= 1
                                # Create explosion for player ship
                                explosionList.append(Explosion(playerX + 6, playerY + 3, len(explosionFrames)))
                                player.setHitTimer(playerFlashTimerMax)  # Reset hit timer
                                playerFlashing = True
                                audio.playSfx(sounds.explode8b)
                                
                            else:
                                gameOver = True
                                lives = 0
                                currentMomentum = 0
                                
                            break
                
        ######################################
        # Delete enemy
        ######################################
        dropVal = random.getrandbits(2) # run random all the time
        if tmpBullet > 0:
            # Remove hit point off enemy and only delete if empty
            bulType = playerBullets[tmpBullet - 1].getType()
            if enemyList[tmpEn - 1].getHitsTaken(bulType) <= 0:
                # Set kitteh abductee state if relevant, ie drop back down
                if enemyList[tmpEn - 1].getAbductingState():
                    for kitteh in kittyList:
                        if kitteh.getAbductedState():
                            kitteh.setAbductedState(False)
                            break
                del enemyList[tmpEn - 1]
                # Drop an item if random is high enough
                dropChance = random.getrandbits(7)
                #print (str(dropChance))
                if dropChance > 50:
                    if dropVal > 2:
                        dropVal = 2
                    if len(dropItem) == 0:
                        dropItem = [[tmpBullPos[0], tmpBullPos[1] - 5, dropVal]]
                    else:
                        dropItem.append([tmpBullPos[0], tmpBullPos[1] - 5, dropVal])
                
                # Create explosion
                explosionList.append(Explosion(tmpBullPos[0], tmpBullPos[1], len(explosionFrames)))
                audio.playSfx(sounds.explode8b)
                
            del playerBullets[tmpBullet - 1]
            gc.collect()
            
        ######################################
        # Check if there are type 2 jellies on level, and if not, spawn one
        ######################################
        if len(enemyList) > 0:
            jellyOnLevel = False
            for enemy in enemyList:
                if enemy.getType() == 2:
                    jellyOnLevel = True
                
            if not jellyOnLevel:
                enemyList.append(Enemy(random.getrandbits(7) + 200, random.getrandbits(5) + 20, False, enemyShips[2], 2, 1, random.getrandbits(1), 20, 17))
                
            # Check for final jelly not in the sky
            if len(enemyList) == 1 and enemyList[0].getType() == 2:
                if enemyList[0].getPos()[1] < 25:
                    del enemyList[0]
                    gc.collect()
            
        else:
            levelComplete = True
            if cPressed:
                cPressed = False
                # Apply bonus of kitties saved
                score += len(kittyList) * 2000
                level += 1
                startLevel(level)
        
        ######################################
        # Update kitteh state
        ######################################
        tmpId = 0
        kittyCtr = 0
        for kitteh in kittyList:
            kittyCtr += 1
            # Has kitteh been abducted?
            kitteh.update(mapSize, currentMomentum)
            if kitteh.getAbductedState():
                if kitteh.getDeathState():
                    # Delete kitteh
                    tmpId = kittyCtr
                    lives -= 1
                    break
    
        if tmpId > 0:
            # Create explosion for player ship
            explosionList.append(Explosion(playerX + 6, playerY + 3, len(explosionFrames)))
            player.setHitTimer(playerFlashTimerMax)  # Reset hit timer
            playerFlashing = True
            audio.playSfx(sounds.explode8b)
                
            # Delete abducted kitteh
            del kittyList[tmpId - 1]
            # Now delete enemy
            tmpId = 0
            tmpCtr = 0
            for enemy in enemyList:
                tmpCtr += 1
                if enemy.getPos()[1] < 1:
                    tmpId = tmpCtr
                    break
                
            if len(enemyList) > 0:
                del enemyList[tmpCtr - 1]
            gc.collect()
        
        if len(kittyList) > 0:
            if not levelComplete and not gameOver:
                if kittyScoreTimer > 0:
                    kittyScoreTimer -= 1
                else:
                    kittyScoreTimer = kittyScoreTimerMax
                    score += kittyScore * len(kittyList)
        
        else:
            gameOver = True
            lives = 0
            currentMomentum = 0
            
        # Play game over sfx
        if lives == 0:
            if not gameOverPlayed:
                audio.playSfx(sounds.gameover8b)
                gameOverPlayed = True
        ######################################
        # Update drops states
        ######################################
        ctr = 0
        tmpId = -1
        dropType = -1
        for i in range(len(dropItem)):
            ctr += 1
            dropX = dropItem[i][0]
            dropY = dropItem[i][1]
            dropItem[i][0] += currentMomentum
            if dropX > mapSize - 16:
                dropItem[i][0] = -15
            if dropX < -15:
                dropItem[i][0] = mapSize - 16
            
            # Is player over it?
            if player.getDirection() > 0:
                if playerX + 8 >= dropX and playerX + 8 <= dropX + 12:
                    if playerY >= dropY and playerY + 6 <= dropY + 12:
                        dropType = dropItem[i][2]
                        tmpId = ctr
                        break
            else:
                if playerX >= dropX and playerX <= dropX + 12:
                    if playerY >= dropY and playerY + 6 <= dropY + 12:
                        dropType = dropItem[i][2]
                        tmpId = ctr
                        break
                
        if tmpId > -1:
            explodyShips = False
            
            # Bomb
            if dropType == 0:
                # Explode enemies in viewport only
                tmpCtr = 0
                for enemy in enemyList:
                    tmpCtr += 1
                    tmpEnemyPos = enemy.getPos()
                    if abs(tmpEnemyPos[0] - playerX) < screenWidth:
                        explosionList.append(Explosion(tmpEnemyPos[0], tmpEnemyPos[1], len(explosionFrames)))
                        explodyShips = True
                        enemy.setHitsTaken()
                        score += 100
                        audio.playSfx(sounds.explode8b)
                        
                        # Check if this enemy is busy abducting, and if so, to reset kitteh
                        if enemy.getAbductingState():
                            for kitteh in kittyList:
                                if kitteh.getAbductedState():
                                    kitteh.setAbductedState(False)
                                    break
                
            # Bonus
            elif dropType == 1:
                score += 100
                audio.playSfx(sounds.bonus8b)
                
            # Life
            elif dropType == 2:
                if lives < 5:
                    lives += 1
                
                audio.playSfx(sounds.extralife8b)
                    
            del dropItem[tmpId - 1]
            
            # Delete enemies on screen
            if explodyShips:
                tmpCtr = 0
                for enemy in enemyList:
                    tmpCtr += 1
                    if enemy.getHitsTaken(0) <= 0:
                        del enemyList[tmpCtr - 1]
                
            gc.collect()

#################################################################################################################
# Render method
#################################################################################################################
def render():
    global playerFlashing, playerFlashTimer, playerFlashTimerMax, dropImages
    global playerX, playerY
    
    if gameState == STATE_MENU:
        screen.blit(gameBg, 0, 0)
        screen.blit(logo, logoX, logoY)
        umachine.draw_text(42, 70, "A: START", 1)
        umachine.draw_text(45, 78, "B: INFO", 1)
        umachine.draw_text(88, 82, "v0." + str(version), 2)
        
    elif gameState == STATE_INSTRUCTIONS:
        screen.blit(dropImages[2], 10, 43)
        screen.blit(dropImages[1], 10, 58)
        screen.blit(dropImages[0], 10, 73)
        
        textY = 0
        for i in range(len(instructions)):
            umachine.draw_text(0, textY, instructions[i], 1)
            if i < 4:
                textY += 8
            else:
                textY += 7
        
    elif gameState == STATE_GAME:
        #######################
        # Background
        #######################
        drawBackground(gameBg, screenXOffset, screenWidth)
        #######################
        # Sun
        #######################
        screen.blit(sun, sunPos, 0)
        #######################
        # Clouds
        #######################
        drawClouds(clouds, cloudsPos, screenWidth)
        #######################
        # Mountains
        #######################
        drawMountains(mountains, screenXOffset, screenWidth)
        #######################
        # Kitteh boat
        #######################
        screen.blit(kittyboat, kittyBoatX, kittyBoatY)
        #######################
        # Waves
        #######################
        waves.draw(screen, waveX - screenWidth, 19)
        waves.draw(screen, waveX, 19)
        waves.draw(screen, waveX + screenWidth, 19)
        #######################
        # Interface
        #######################
        screen.blit(interface, 0, 0)
        #######################
        # Score
        #######################
        rightOffset = 6 * len(str(score))
        umachine.draw_text(40 - rightOffset, 0, str(score), 1)
        #######################
        # Draw Lives
        #######################
        heartX = 70
        heartY = 1
        for i in range(6):
            if i < lives:
                screen.blit(life[1], heartX, heartY)
            else:
                screen.blit(life[0], heartX, heartY)
                
            heartX += 8
        ####################### 
        # Draw powershots bar
        #######################
        tmpPsLoop = powerShots #int(powerShots // 2)
        tmpPsX = 13
        tmpPsY = 9
        for i in range(5):
            if i < tmpPsLoop:
                screen.blit(powerBulletBar[0], tmpPsX, tmpPsY)
            else:
                screen.blit(powerBulletBar[1], tmpPsX, tmpPsY)
            tmpPsX += 3
            
        ######################~
        # Draw milk stations
        #######################
        for i in range(len(milkStations)):
            screen.blit(milkStation, milkStations[i], 63)
            
        #######################
        # Draw kitteh if alive
        #######################
        for kitteh in kittyList:
            kitteh.draw(screen, kitty)
            
        #######################
        # Draw enemies
        #######################
        for enemy in enemyList:
            tmpEnemyPos = enemy.getPos()
            enemy.draw(screen)

        #######################
        # Draw player
        #######################
        if playerFlashing:
            if playerFlashTimer > 0:
                playerFlashTimer -= 1
                if playerFlashTimer % 2 == 0:
                    player.draw(screen, playerShip)
            else:
                # Reset flash timer
                playerFlashing = False
                playerFlashTimer = playerFlashTimerMax
        else:
            player.draw(screen, playerShip)
        
        playerPos = player.getPlayerPos()
        playerY = playerPos[1]
        
        #######################
        # Draw enemy bullets
        #######################
        for playerBullet in playerBullets:
            playerBullet.draw(screen)
            
        #######################
        # Draw dropped item
        #######################
        for i in range(len(dropItem)):
            screen.blit(dropImages[dropItem[i][2]], dropItem[i][0], dropItem[i][1])
                
        #######################
        # Draw explosion
        #######################
        for explody in explosionList:
            explody.draw(screen, explosionFrames)
            
        #######################
        # Draw pops
        #######################
        for pops in popList:
            pops.draw(screen, popFrames)
            
        #######################
        # Enemies on screen
        umachine.draw_text(56, 1, str(len(enemyList)), 1)
        
        #######################
        # Draw cat-nav radar
        #######################
        catnavX = 0
        catnavY = 74
        catnavWidth = 44
        catnavHeight = 13
        aspectRatioX = mapSize // catnavWidth
        aspectRatioY = 70 // catnavHeight
        pygame.draw.rect(pygame.Rect(catnavX, catnavY, catnavWidth, catnavHeight), False, 1)
        tmpEnCtr = 0
        tmpPlyX = (playerPos[0] // aspectRatioX) + (catnavWidth // 2 - 4)
        tmpPlyY = catnavY + (playerPos[1] // aspectRatioY) - 3
        pygame.draw.pixel(catnavX + tmpPlyX, tmpPlyY, 6)
        for enemy in enemyList:
            
            tmpEnemyPos = enemy.getPos()
            tmpX = (tmpEnemyPos[0] // aspectRatioX) + (catnavWidth // 2 - 4)
            if tmpX < 0:
                tmpX += catnavWidth
                
            if tmpX > catnavWidth:
                tmpX += -catnavWidth
                
            tmpY = catnavY + (tmpEnemyPos[1] // aspectRatioY) - 3
            if tmpY > catnavY:
                pygame.draw.pixel(catnavX + tmpX, tmpY, 1)
                
            if enemy.getType() == 2:
                if tmpY > catnavY:
                    pygame.draw.pixel(catnavX + tmpX, tmpY, 7)
                    
                    if enemy.getAbductingState():
                        pygame.draw.circle(catnavX + tmpX, tmpY, 2, False, 1)
            else:
                pygame.draw.pixel(catnavX + tmpX, tmpY, 1)
                
            tmpEnCtr += 1
        
        #######################
        # Game over
        #######################
        if gameOver:
            screen.blit(gameoverBG, 14, 20)
            umachine.draw_text(22, 34, "OH NOES...", 13)
            umachine.draw_text(22, 41, "FISH THAT", 13)
            umachine.draw_text(22, 48, "KITTY OUT,", 13)
            umachine.draw_text(22, 55, "TRY AGAIN", 13)
            
        #######################
        # Level complete?
        #######################
        if levelComplete and not gameOver:
            screen.blit(levelCompleteBG, 14, 20)
            umachine.draw_text(22, 34, "Miners saved:", 1)
            startKittyX = 25
            startKittyY = 44
            for i in range(len(kittyList)):
                screen.blit(kitty, startKittyX, startKittyY)
                startKittyX += 18
                
            umachine.draw_text(32, 60, "Bonus: " + str(len(kittyList) * 2000), 1)

# Additional functions
def drawBackground(bg, screenXOffset, screenWidth):
    screen.blit(bg, screenXOffset - screenWidth, 0)
    screen.blit(bg, screenXOffset, 0)
    screen.blit(bg, screenXOffset + screenWidth, 0)

def drawMountains(mountains, screenXOffset, screenWidth):
    screen.blit(mountains, screenXOffset - screenWidth, 12)
    screen.blit(mountains, screenXOffset, 12)
    screen.blit(mountains, screenXOffset + screenWidth, 12)

def drawClouds(clouds, cloudsPos, screenWidth):
    screen.blit(clouds, cloudsPos, 4)
    
# Main loop
while True:
    # Pause game over before goign to menu
    if gameOver and gameOVerTimer > 0:
        gameOVerTimer -= 1

    # Read keys
    eventtype = pygame.event.poll()
    if waitOnLoad > 0:
        waitOnLoad -= 1
    else:
        if eventtype != pygame.NOEVENT:
    
    		# Keydown events
            if eventtype.type == pygame.KEYDOWN:
                
                if (eventtype.key == pygame.K_UP):
                    if not gameOver and not levelComplete:
                        keyVertical = False
                        currentY = -shipMoveSpeed
                
                if (eventtype.key == pygame.K_RIGHT):
        		    if not gameOver and not levelComplete:
        		        player.setDirection(1)
        		        keySideways = False
        		        # Instantly stop momentum
        		        if currentMomentum > 0:
        		            currentMomentum = 0
        		            
        		        if currentMomentum > -momentumMax:
        		            currentMomentum -= shipMoveSpeed
    
                if (eventtype.key == pygame.K_DOWN):
                    if not gameOver and not levelComplete:
                        keyVertical = False
                        currentY = shipMoveSpeed
    
                if (eventtype.key == pygame.K_LEFT):
        		    if not gameOver and not levelComplete:
        		        player.setDirection(-1)
        		        keySideways = False
        		        # Instantly stop momentum
        		        if currentMomentum < 0:
        		            currentMomentum = 0
        		            
        		        if currentMomentum < momentumMax:
        		            currentMomentum += shipMoveSpeed
    
    
                if (eventtype.key == pygame.BUT_C):
                    if not cPressed:
        		        cPressed = True
        		        if gameState == STATE_GAME:
        		            if not pauseGame:
        		                pauseGame = True
        		                #print ("game=>pause")
    
    
                if (eventtype.key == pygame.BUT_B):
                    if not bPressed:
        		        bPressed = True
        		        if gameState == STATE_MENU:
        		            #print ("menu=>instructions")
        		            gameState = STATE_INSTRUCTIONS
        		            audio.playSfx(sounds.select8b)
        		            
        		        if gameState == STATE_GAME:
        		            if not gameOver:
        		                #print ("not game over - game=>powershot")
        		                if powerShots > 0:
        		                    powerShots -= 1
        		            else:
        		                #print (str(gameOVerTimer))
        		                if gameOVerTimer <= 0:
        		                    gameOver = False
        		                    gameState = STATE_MENU
        		                    audio.playSfx(sounds.select8b)
    
                if (eventtype.key == pygame.BUT_A):
                    if not aPressed:
                        aPressed = True
                        
                    if gameState == STATE_MENU:
    		            #print ("menu=>game")
    		            resetGame()
    		            gameState = STATE_GAME
    		            
                    elif gameState == STATE_INSTRUCTIONS:
    		            #print("instructions=>menu")
    		            gameState = STATE_MENU
    		            audio.playSfx(sounds.select8b)
        		                
                
            # Keyup events
            if eventtype.type == pygame.KEYUP:
                if (eventtype.key == pygame.K_UP):
                    keyVertical = True
                    
                if (eventtype.key == pygame.K_RIGHT):
                    keySideways = True
                    
                if (eventtype.key == pygame.K_DOWN):
                    keyVertical = True
                    
                if (eventtype.key == pygame.K_LEFT):
                    keySideways = True
                    
                if (eventtype.key == pygame.BUT_C):
                    cPressed = False
                    
                if (eventtype.key == pygame.BUT_B):
                    #if gameState == STATE_INSTRUCTIONS:
                    bPressed = False
                        
                if (eventtype.key == pygame.BUT_A):
                    #if gameState == STATE_MENU:
                    aPressed = False
	
	# Update classes/objects
    update()
    # Render classes/objects
    screen.fill(0)  # Clear screen
    render()
    
    #print (str(gameState))
	# Sync screen
    pygame.display.flip()
