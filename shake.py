# shake.py
# This class is used to shake the whole screen.

class Shake:
    def __init__(self):
        self.shake = False
        self.x = 0
        self.direction = 1
        self.shakeMax = 10
        self.shakeAmount = self.shakeMax
    
    def update(self):
        if self.shakeAmount > 0:
            self.shakeAmount -= 1
            self.shake = True
        else:
            self.shakeAmount == self.shakeMax
            self.shake = False
        
        if self.shake:
            if self.direction == 1:
                self.direction = -self.direction
                return self.shakeAmount
            else:
                self.direction = -self.direction
                return -self.shakeAmount
        else:
            return 0