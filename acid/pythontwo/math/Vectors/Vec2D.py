import math as m

class Vect2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
    
    def returnvect(self):
        return (self.x, self.y)
    
    def add(self, other):
        if isinstance(other, Vect2D):
            return Vect2D(self.x + other.x, self.y + other.y)
        else:
            raise TypeError('Can only add a Vec2D to another Vec2D')
    
    def sub(self, other):
        if isinstance(other, Vect2D):
            return Vect2D(self.x - other.x, self.y - other.y)
        else:
            raise TypeError('Can only subtract a Vec2D from another Vec2D')
    
    def mul(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vect2D(self.x * scalar, self.y * scalar)
        else:
            raise TypeError('Can only multiply a Vec2D by a scalar')
    def div(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError('Cannot divide by zero')
            return Vect2D(self.x // scalar, self.y // scalar)
        else:
            raise TypeError('Can only divide a Vec2D by a scalar')
    
    def __truediv__(self, scalar):
        if isinstance(scalar, (int, float)):
            if scalar == 0:
                raise ValueError('Cannot divide by zero')
            return Vect2D(self.x / scalar, self.y / scalar)
        else:
            raise TypeError('Can only divide a Vec2D by a scalar')
    
    def eq(self, other):
        if isinstance(other, Vect2D):
            return self.x == other.x and self.y == other.y
        else:
            return False
    
    
    def mag(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def norm(self):
        mag = self.mag()
        if mag == 0:
            return Vect2D(0, 0)
        return Vect2D(self.x / mag, self.y / mag)
    
    def dot(self, other):
        if isinstance(other, Vect2D):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError('Can only dot a Vec2D with another Vec2D')
    
    def cross(self, other):
        if isinstance(other, Vect2D):
            return self.x * other.y - self.y * other.x
        else:
            raise TypeError('Can only cross a Vec2D with another Vec2D')
    
    def angle(self, other):
        if isinstance(other, Vect2D):
            dot_product = self.dot(other)
            magnitudes = self.mag() * other.mag()
            if magnitudes == 0:
                return 0
            return m.acos(dot_product / magnitudes)
        else:
            raise TypeError('Can only calculate the angle between a Vec2D and another Vec2D')
    
    def __repr__(self):
        return f"{(self.x, self.y)}"