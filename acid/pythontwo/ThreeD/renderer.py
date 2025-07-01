import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import OpenGL

print("[ACID BOOST] Accelerate loaded?", OpenGL.USE_ACCELERATE)

# --- CONFIGURATION ---
SCREEN_SIZE       = (800, 600)
FOV               = 60
MOVE_SPEED        = 0.1
MOUSE_SENSITIVITY = 0.15

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
            (1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1)
        ]

    def draw(self, pos=(0, 0, 0), scale=(1, 1, 1), rotation=(0, 0, 0), ignore_colors=False):
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(*scale)
        glRotatef(rotation[0], 1, 0, 0)
        glRotatef(rotation[1], 0, 1, 0)
        glRotatef(rotation[2], 0, 0, 1)

        glBegin(GL_QUADS)
        for idx, face in enumerate(self.faces):
            glColor3fv((0.5, 0.5, 0.9) if ignore_colors else self.colors[idx % len(self.colors)])
            for vert in face:
                glVertex3fv(self.vertices[vert])
        glEnd()

        glPopMatrix()

# --- CAMERA HANDLING ---
class Camera:
    def __init__(self, pos=[0, 0, 5]):
        self.position = list(pos)
        self.yaw = 0.0
        self.pitch = 0.0
        self.speed = MOVE_SPEED
        self.sensitivity = MOUSE_SENSITIVITY
        self.front = [0, 0, -1]
        self.right = [1, 0, 0]
        self.up = [0, 1, 0]

    def _normalize(self, vec):
        length = math.sqrt(sum(i * i for i in vec))
        return [i / length for i in vec]

    def _cross(self, a, b):
        return [
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        ]

    def update_vectors(self):
        x = math.cos(math.radians(self.pitch)) * math.cos(math.radians(self.yaw))
        y = math.sin(math.radians(self.pitch))
        z = math.cos(math.radians(self.pitch)) * math.sin(math.radians(self.yaw))
        self.front = self._normalize([x, y, z])
        self.right = self._normalize(self._cross(self.front, [0, 1, 0]))
        self.up = self._cross(self.right, self.front)

    def bettermove(self, x, y, z):
        self.update_vectors()
        self.position[0] += self.right[0] * x + self.up[0] * y + self.front[0] * z
        self.position[1] += self.right[1] * x + self.up[1] * y + self.front[1] * z
        self.position[2] += self.right[2] * x + self.up[2] * y + self.front[2] * z

    def apply(self):
        self.update_vectors()
        target = [self.position[i] + self.front[i] for i in range(3)]
        glLoadIdentity()
        gluLookAt(*self.position, *target, 0, 1, 0)

# --- ENGINE / MAIN LOOP ---
class Engine3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | OPENGL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(FOV, SCREEN_SIZE[0] / SCREEN_SIZE[1], 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.get_rel()

        self.running = True
        self.camera = Camera()
        self.clock = pygame.time.Clock()
        self.len = len(pygame.key.get_pressed())

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                self.running = False

    def get_mouse(self):
        return pygame.mouse.get_pos() if self.running else (0, 0)

    def set_mouse(self, x, y):
        if self.running:
            pygame.mouse.set_pos((x, y))

    def get_key(self):
        return pygame.key.get_pressed() if self.running else [0] * self.len

    def clear(self):
        if self.running:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update(self):
        if self.running:
            pygame.display.flip()

# --- MAIN FUNCTION ---
def main():
    engine = Engine3D()
    camera = engine.camera
    cube = Object3D()
    angle = 0

    while engine.running:
        engine.loop()

        keys = engine.get_key()
        if keys[pygame.K_w]: camera.bettermove(0, 0, -camera.speed)
        if keys[pygame.K_s]: camera.bettermove(0, 0, camera.speed)
        if keys[pygame.K_a]: camera.bettermove(-camera.speed, 0, 0)
        if keys[pygame.K_d]: camera.bettermove(camera.speed, 0, 0)

        dx, dy = pygame.mouse.get_rel()
        camera.yaw += dx * camera.sensitivity
        camera.pitch -= dy * camera.sensitivity
        camera.pitch = max(-89.9, min(89.9, camera.pitch))

        camera.apply()
        engine.clear()
        cube.draw(pos=(0, 0, 0), rotation=(angle, angle, angle))
        engine.set_mouse(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
        engine.update()
        engine.clock.tick(60)
        angle += 1

# --- Helper Functions ---

def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.strip().split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(tuple(face))

    vertices = np.array(vertices, dtype=np.float32)
    return vertices, faces


if __name__ == "__main__":
    main()