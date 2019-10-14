# kittens.py

class Kitty:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.startY = y
        self.deathState = False
        self.abductedState = False
        self.walkMax = 20
        self.walkLimit = 0
        self.walkDir = 1
        self.walkSpeed = 1
        
    # Update stuff
    def update(self, mapSize, movement):
        self.x += movement
        
        # Make sure kitten "loops" on map
        if self.x > mapSize:
            self.x = 0
        
        if self.x < 0:
            self.x = mapSize
            
        # Move kitty if state is caught
        if self.abductedState:
            self.y -= 1
            if self.y < 0 and not self.deathState:
                self.deathState = True
        else:
            # Drop back down if abduction failed
            if self.y < self.startY:
                self.y += 1
                
            # Just walk around a bit
            if self.walkSpeed > 0:
                self.walkSpeed -= 1
            else:
                self.x += self.walkDir
                self.walkLimit += 1
                self.walkSpeed = 1
            
            if self.walkLimit > self.walkMax:
                self.walkDir = -self.walkDir    # Change dir
                self.walkLimit = 0
                
    # Draw kitteh
    def draw(self, screen, img):
        screen.blit(img, self.x, self.y)
        
    # Get state
    def getDeathState(self):
        return self.deathState
        
    def getAbductedState(self):
        return self.abductedState
        
    def setAbductedState(self, state):
        self.abductedState = state
        
    # Get pos
    def getPos(self):
        return [self.x, self.y]