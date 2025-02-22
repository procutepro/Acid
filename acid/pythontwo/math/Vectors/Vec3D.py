import math as m
import pythontwo.Vectors.Vec2D as Vec2D

class Vect3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def returnvec(self):
        return f"({self.x}, {self.y}, {self.z})"

    def add(self, other):
        if isinstance(other, Vect3D):
            return Vect3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type(s) for +: 'Vec3D' and '{type(other).__name__}'")
    
    def sub(self, other):
        if isinstance(other, Vect3D):
            return Vect3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type(s) for -: 'Vec3D' and '{type(other).__name__}'")
    
    def mul(self, scalar):
        return Vect3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def div(self, scalar):
        if isinstance(scalar, (int, float)):
            return Vect3D(self.x / scalar, self.y / scalar, self.z / scalar)
        else:
            raise TypeError("Unsupported operand type(s) for /: 'Vec3D' and '{type(scalar).__name__}'")
    
    def dot(self, other):
        if isinstance(other, Vect3D):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vec3D' and '{type(other).__name__}'")
    
    def cross(self, other):
        if isinstance(other, Vect3D):
            return Vect3D(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
            )
        else:
            raise TypeError("Unsupported operand type(s) for ^: 'Vec3D' and '{type(other).__name__}'")
    
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
    
    def normalize(self):
        magnitude = self.magnitude()
        if magnitude != 0:
            return Vect3D(self.x / magnitude, self.y / magnitude, self.z / magnitude)
        else:
            raise ValueError("Cannot normalize a zero vector")
    
    def project(self):
        projected_Vec = Vec2D.Vect2D(self.x / self.z, self.y / self.z)
        return projected_Vec
    
    def angle_between(self, other):
        if isinstance(other, Vect3D):
            dot_product = self.dot(other)
            magnitude_product = self.magnitude() * other.magnitude()
            return m.acos(dot_product / magnitude_product)
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Vec3D' and '{type(other).__name__}'")
    
    def __repr__(self):
        return f"{(self.x, self.y, self.z)}"