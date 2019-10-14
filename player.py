# player.py
# Handle player control and management

import upygame as pygame
import graphics

class Player:
    def __init__(self, startX, startY, minY, maxY, speed):
        self.playerX = startX		# Start X
        self.playerY = startY		# Start Y
        self.min = minY				# Left clamp
        self.max = maxY				# Right clamp
        self.direction = 1	# 1 for right, 0 for left
        self.speed = speed
        self.playerHitTimer = 0

    # Draw player
    def draw(self, screen, image):
        if self.direction > 0:
            screen.blit(image, self.playerX, self.playerY)
        else:
            screen.blit(image, self.playerX, self.playerY, 0, True)

    # Get current direction
    def getDirection(self):
        return self.direction

    # Set direction
    def setDirection(self, dir):
        self.direction = dir
        
    # Move player
    def movePlayer(self, y):
        self.playerY += y
        
        if (self.playerY > self.max):
            self.playerY = self.max

        if (self.playerY < self.min):
            self.playerY = self.min

    # Return x/y pos
    def getPlayerPos(self):
        return [self.playerX, self.playerY]
        
    # Set player pos
    def setPlayerPos(self, x, y):
        self.playerX = x
        self.playerY = y

    # Update timer
    def updateTimer(self):
        if self.playerHitTimer > 0:
            self.playerHitTimer -= 1
    
    # Get player hit timer
    def getHitTimer(self):
        return self.playerHitTimer
        
    # Set it
    def setHitTimer(self, time):
        self.playerHitTimer = time