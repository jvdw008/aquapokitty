# bullets.py

import upygame as pygame

class Bullet:
    def __init__(self, x, y, direction, speed, type, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.type = type        # 0/1 enemy, 2 = player bullet, 3 = power player bullet
        self.image = image
        self.distance = 14
    
    # Update position and state    
    def update(self, movement):
        if self.direction > 0:
            self.x += self.speed
            
        if self.direction < 0:
            self.x += -self.speed
        
        self.x += movement
        # Check distance travelled
        if self.distance > 0:
            self.distance -= 1
            return True
        else:
            return False
            
        # False means the bullet is still alive, True means it has reached its limit

    # Check collision
    def checkCollision(self, x, y, width, height):
        if self.direction > 0:
            if self.x + 8 > x and self.x + 8 < x + width:
                if self.y > y and self.y + 5 < y + height:
                    return True
        else:
            if self.x > x and self.x < x + width:
                if self.y > y and self.y + 5 < y + height:
                    return True
                
        return False
        
        # True means collision, False not
    
    # Draw bullet
    def draw(self, screen):
        if self.direction > 0:
            screen.blit(self.image, self.x, self.y)
        
        if self.direction < 0:
            screen.blit(self.image, self.x, self.y, 0, True)
            
    # Get type - used to determine damage amount
    def getType(self):
        return self.type
        
    # Get x/y pos
    def getPosition(self):
        return [self.x, self.y]