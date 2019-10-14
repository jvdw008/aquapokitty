# enemy.py
# Enemy class

class Enemy:
    def __init__(self, x, y, shooting, image, type, direction, directionY, width, height):
        self.x = x
        self.y = y
        self.shooting = shooting
        self.image = image
        self.type = type
        self.direction = direction
        self.directionY = directionY
        self.hitsTaken = type + 3
        self.abducting = False
        self.width = width      # Used to size hitbox
        self.height = height    # Used to size hitbox
        self.speedX = 1
        self.speedY = 1
        self.startX = 1         # Used for type 2
        
        # Bomb dude
        if type == 3:
            self.speedX = 0
        # Big dude
        elif type == 4:
            self.speedY = 0
            if self.y > 40:
                self.y = 40
        # Fast dude
        elif type == 5:
            self.speedX = 2
            
        self.maxBullets = 1    # To limit each enemy's ability to shoot too many bullets
        
    # Update position
    def update(self, playerX, playerY, mapSize, movement, screenWidth):
        
        if self.type == 1:
            if playerX - 1 > self.x:
                self.direction = 1
                self.x += self.speedX
            elif playerX + 1 < self.x:
                self.direction = -1
                self.x += -self.speedX
                
        # Jelly
        elif self.type == 2:
            if self.abducting:
                self.x += 0
                self.y -= 1
                self.speedX
            else:
                if self.direction > 0:
                    self.x += self.speedX
                else:
                    self.x += -self.speedX
        
        elif self.type == 3:
            if self.directionY > 0:
                self.y += self.speedY
            else:
                self.y += -self.speedY
        
        else:
            
            if self.direction > 0:
                self.x += self.speedX
            else:
                self.x += -self.speedX
            
        self.x += movement
        
        # Make sure enemy "loops" on map
        if self.x > mapSize - screenWidth:
            self.x = -screenWidth
        
        if self.x < -mapSize + screenWidth:
            self.x = screenWidth
            
        # Limit Y movement top and btm
        if self.y < 25:
            self.directionY = self.speedY
        elif self.y > 72:
            self.directionY = -self.speedY
    
    # Enemy moves toward kitteh
    def trackKitteh(self, x, y):
        if not self.abducting:
            
            if self.x + 8 > x and self.x + 8 < x + 16:
                self.speedX = 0
                self.x = x - 4
                    
                if self.y + 10 < y:
                    self.y += 1
                    
                else:
                    self.setAbductingState(True)
                    self.x = x - 4
                    return True
                    
            else:
                self.speedX = self.startX
                
        return False
    
    # Draw
    def draw(self, screen):
        if self.direction > 0:
            screen.blit(self.image, self.x, self.y)
        else:
            screen.blit(self.image, self.x, self.y, 0, True)
            
    # Get height for hitbox
    def getHeight(self):
        return self.height
        
    # Get width for hitbox
    def getWidth(self):
        return self.width
    
    # Get position
    def getPos(self):
        return [self.x, self.y]
    
    # Get direction
    def getDirection(self):
        return self.direction
        
    # Set direction
    def setDirection(self, dir):
        self.direction = dir
    
    # Is enemy shooting
    def getShooting(self):
        return self.shooting
        
    # Set abducted movement
    def setAbductingState(self, state):
        self.abducting = state
        
    # Get it
    def getAbductingState(self):
        return self.abducting
        
    # Set shooting
    def setShooting(self, val):
        self.shooting = val
        
    # Get type
    def getType(self):
        return self.type
        
    # Set hits taken for explosion drop
    def setHitsTaken(self):
        self.hitsTaken = 0
        
    # Adjust hits taken
    def getHitsTaken(self, bulletType):
        if self.hitsTaken > 0:
            if bulletType == 2:
                self.hitsTaken -= 1
            elif bulletType == 3:
                self.hitsTaken -= 3
        return self.hitsTaken
        