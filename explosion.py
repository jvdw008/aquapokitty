# explosion.py

class Explosion:
    def __init__(self, x, y, maxFrames):
        self.x = x
        self.y = y
        self.currentFrame = 0
        self.maxFrames = maxFrames
        
    # Update frame
    def update(self, movement):
        self.x += movement
        
        if self.currentFrame <= self.maxFrames:
            self.currentFrame += 1
            
    # Draw frame
    def draw (self, screen, img):
        screen.blit(img[self.currentFrame - 1], self.x, self.y)
        
    # Get frame state
    def getFrame(self):
        return self.currentFrame
        