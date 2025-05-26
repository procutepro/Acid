import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

# --- CONFIGURATION ---
SCREEN_SIZE       = (800, 600)
FOV               = 60
MOVE_SPEED        = 0.01    # units per second
MOUSE_SENSITIVITY = 0.1   # tweak to taste
COLOR_TRANSLATION = {
    "red": (1, 0, 0),
    "green": (0, 1, 0),
    "blue": (0, 0, 1),
    "white": (1, 1, 1),
    "black": (0, 0, 0),
    "yellow": (1, 1, 0),
    "cyan": (0, 1, 1),
    "magenta": (1, 0, 1),
    "orange": (1, 0.5, 0),
    "purple": (0.5, 0, 0.5),
    "gray": (0.5, 0.5, 0.5),
    "pink": (1, 0.75, 0.8),
    "lime": (0.75, 1, 0),
    "teal": (0, 0.5, 0.5),
    "navy": (0, 0, 0.5),
    "brown": (0.4, 0.26, 0.13)
}

# --- BASIC OBJECT TO DRAW ---


class Object3D:
    def __init__(self):
        self.vertices = np.array([
            [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
            [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
        ], dtype=np.float32)

        self.faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (3, 2, 6, 7),
            (0, 1, 5, 4), (3, 0, 4, 7), (1, 2, 6, 5)
        ]

        self.colors = [
            (0.6, 0.3, 0), (0.6, 0.3, 0), (0.6, 0.3, 0),
            (0.6, 0.3, 0), (0, 1, 0), (0.6, 0.3, 0)
        ]

    def draw(self, pos=(0, 0, 0), scale=(1, 1, 1), rotation=(0, 0, 0), ignore_colors=False):
        glPushMatrix()

        # Rotation matrices
        rx, ry, rz = np.radians(rotation)

        # X rotation
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(rx), -np.sin(rx)],
            [0, np.sin(rx), np.cos(rx)]
        ])

        # Y rotation
        Ry = np.array([
            [np.cos(ry), 0, np.sin(ry)],
            [0, 1, 0],
            [-np.sin(ry), 0, np.cos(ry)]
        ])

        # Z rotation
        Rz = np.array([
            [np.cos(rz), -np.sin(rz), 0],
            [np.sin(rz), np.cos(rz), 0],
            [0, 0, 1]
        ])

        # Combined rotation
        R = Rz @ Ry @ Rx

        # Apply rotation, scale, and position
        transformed = (self.vertices @ R.T) * scale + pos

        glBegin(GL_QUADS)
        for idx, face in enumerate(self.faces):
            glColor3fv(self.colors[idx] if not ignore_colors else ignore_colors)
            for vert in face:
                glVertex3fv(transformed[vert])
        glEnd()

        glPopMatrix()

# --- CAMERA HANDLING ---
class Camera:
    def __init__(self, pos=[0,0,5]):
        self.position = pos
        self.sensitivity = MOUSE_SENSITIVITY
        self.speed = MOVE_SPEED
        self.yaw   = 0.0  # left/right
        self.pitch = 0.0  # up/down

        # Initialize vectors
        self.front = [0, 0, -1]
        self.right = [1, 0, 0]
        self.up = [0, 1, 0]
    
    def _normalize(self, vec):
        length = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
        return [vec[0]/length, vec[1]/length, vec[2]/length]

    def _cross(self, vec1, vec2):
        return [
            vec1[1]*vec2[2] - vec1[2]*vec2[1],
            vec1[2]*vec2[0] - vec1[0]*vec2[2],
            vec1[0]*vec2[1] - vec1[1]*vec2[0]
        ]
    
    def update_vectors(self):
        # Calculate front vector from yaw & pitch
        x = math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
        y = math.sin(math.radians(self.pitch))
        z = math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
        length = math.sqrt(x*x + y*y + z*z)
        self.front = [x/length, y/length, z/length]

        # Right vector (cross product of front and world-up [0, 1, 0])
        self.right = self._normalize(self._cross(self.front, [0, 1, 0]))

        # Up vector (cross product of right and front)
        self.up = self._cross(self.right, self.front)
    
    def move(self, x, y, z):
        self.position = [
            self.position[0] + x,
            self.position[1] + y,
            self.position[2] + z
        ]
    def bettermove(self, x, y, z):
        # Move camera along its local axes (front, right, up)
        self.update_vectors()  # Update the vectors first

        # Update position based on the front, right, and up vectors
        self.position[0] += self.right[0] * x + self.up[0] * y + self.front[0] * z
        self.position[1] += y
        self.position[2] += self.right[2] * x + self.up[2] * y + self.front[2] * z

    def apply(self):
        glLoadIdentity()
        cx = math.cos(math.radians(self.pitch))
        dir_x = cx * math.sin(math.radians(self.yaw))
        dir_y = math.sin(math.radians(self.pitch))
        dir_z = -cx * math.cos(math.radians(self.yaw))
        target = [
            self.position[0] + dir_x,
            self.position[1] + dir_y,
            self.position[2] + dir_z
        ]
        gluLookAt(*(self.position), *target, 0,1,0)

# --- ENGINE / MAIN LOOP ---
class Engine3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | OPENGL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, SCREEN_SIZE[0]/SCREEN_SIZE[1], 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        # Hide cursor and grab for relative movement
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.get_rel()   # flush initial movement

        self.running = True
        self.len = len(pygame.key.get_pressed())
        self.camera = Camera()
        self.clock  = pygame.time.Clock()
        self.cube   = Object3D()
    
    def get_mouse(self):
        if self.running: return pygame.mouse.get_pos()
        else: return (0, 0)

    def set_mouse(self, x, y):
        if self.running: pygame.mouse.set_pos((x, y))
    
    def get_key(self):
        if self.running: return pygame.key.get_pressed()
        else: return [0] * 323
    
    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                self.running = False
                return
    
    def clear(self):
        if self.running: glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    def update(self):
        if self.running: pygame.display.flip()

# MAKE A EXPLAMPLE CODE
# AND MAKE IT SPIN

def main():
    engine = Engine3D()
    camera = engine.camera
    clock = engine.clock

    # Create a cube object
    cube = Object3D()

    # Main loop
    while engine.running:
        # Handle events
        engine.loop()

        # Handle camera movement
        keys = engine.get_key()
        if keys[pygame.K_w]: camera.bettermove(0, 0, -camera.speed)
        if keys[pygame.K_s]: camera.bettermove(0, 0, camera.speed)
        if keys[pygame.K_a]: camera.bettermove(-camera.speed, 0, 0)
        if keys[pygame.K_d]: camera.bettermove(camera.speed, 0, 0)

        # Handle mouse movement for looking around
        mouse_x, mouse_y = engine.get_mouse()
        camera.yaw += mouse_x * MOUSE_SENSITIVITY
        camera.pitch -= mouse_y * MOUSE_SENSITIVITY

        # Update the camera view
        camera.apply()

        # Clear the screen and draw the cube
        engine.clear()
        cube.draw(pos=cube.vertices[0], scale=(1, 1, 1), rotation=(45, 90, 45))
        
        # Update the display and tick the clock
        engine.set_mouse(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        engine.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
