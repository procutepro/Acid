import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# --- CONFIGURATION ---
SCREEN_SIZE       = (800, 600)
FOV               = 60
MOVE_SPEED        = 5.0    # units per second
MOUSE_SENSITIVITY = 0.2    # tweak to taste

# --- BASIC OBJECT TO DRAW ---
class Cube:
    def __init__(self):
        self.vertices = [
            (1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1),
            (1,1,1),(1,-1,1),(-1,-1,1),(-1,1,1)
        ]
        self.faces = [
            (0,1,2,3),(4,5,6,7),(3,2,6,7),
            (0,1,5,4),(3,0,4,7),(1,2,6,5)
        ]
        self.colors = [(0.6,0.3,0)]*4 + [(0,1,0)] + [(0.6,0.3,0)]

    def draw(self, x, y, z):
        glBegin(GL_QUADS)
        for idx, face in enumerate(self.faces):
            glColor3fv(self.colors[idx])
            for vert in face:
                glVertex3fv((self.vertices[vert][0] + x,
                             self.vertices[vert][1] + y,
                             self.vertices[vert][2] + z))
        glEnd()

# --- CAMERA HANDLING ---
class Camera:
    def __init__(self, pos=(0,0,5)):
        self.position = pos
        self.sensitivity = 0.1
        self.speed = 0.1
        self.yaw   = 0.0  # left/right
        self.pitch = 0.0  # up/down
    
    def move(self, x, y, z):
        self.position = (
            self.position[0] + x,
            self.position[1] + y,
            self.position[2] + z
        )

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
        self.cube   = Cube()
    
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