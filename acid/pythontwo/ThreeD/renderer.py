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

# --- ACIDUI ---

class AcidUI:
    mouse_pos = (0, 0)
    mouse_down = False
    mouse_up = False

    @staticmethod
    def begin(width, height):
        AcidUI.mouse_pos = pygame.mouse.get_pos()
        AcidUI.mouse_pos = (AcidUI.mouse_pos[0], height - AcidUI.mouse_pos[1])
        AcidUI.mouse_down = pygame.mouse.get_pressed()[0]
        AcidUI.mouse_up = not AcidUI.mouse_down

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)

    @staticmethod
    def end():
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    @staticmethod
    def draw_quad(x, y, w, h, color=(1.0, 1.0, 1.0, 1.0)):
        glColor4f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()

    @staticmethod
    def is_hover(x, y, w, h):
        mx, my = AcidUI.mouse_pos
        return x <= mx <= x + w and y <= my <= y + h

    @staticmethod
    def button(label, x, y, w, h, func, color=(0.2, 0.7, 1.0, 1.0), hover_color=(0.3, 0.8, 1.0, 1.0), click_color=(0.1, 0.6, 0.9, 1.0)):
        hovered = AcidUI.is_hover(x, y, w, h)
        pressed = hovered and AcidUI.mouse_down

        # Choose color
        if pressed:
            AcidUI.draw_quad(x, y, w, h, click_color)
        elif hovered:
            AcidUI.draw_quad(x, y, w, h, hover_color)
        else:
            AcidUI.draw_quad(x, y, w, h, color)
        if pressed and AcidUI.mouse_up:
            func()

        # (Optional) Add text drawing here later with texture or bitmap

        return hovered and AcidUI.mouse_up

# --- BASIC OBJECT TO DRAW ---
class Object3D:
    def __init__(self):
        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.velocity = (0, 0, 0)
        self.mass = 1.0  # Default mass for physics calculations
        self.vertices = []
        self.uvs = []
        self.faces = []
        self.tex_id = None

    def set_texture(self, path):
        texture = pygame.image.load(path)
        texture = pygame.transform.flip(texture, False, True)
        texture_data = pygame.image.tostring(texture, "RGB", True)

        self.tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture.get_width(), texture.get_height(), 0,
                     GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw(self, ignore_colors=False, wireframe=False, ignore_texture=False):
        glPushMatrix()
    
        # 🐸 Apply Position
        glTranslatef(self.position[0], self.position[1], self.position[2])
    
        # 🐸 Apply Rotation (XYZ)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        # 🐸 Apply Scale
        glScalef(self.scale[0], self.scale[1], self.scale[2])

        # 🐸 Texture binding
        if self.tex_id and not ignore_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_id)
        else:
            glDisable(GL_TEXTURE_2D)
    
        # 🐸 Wireframe mode
        if wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
        # 🐸 Draw the triangles
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for v_idx, uv_idx in face:
                if self.tex_id and not ignore_texture:
                    glTexCoord2fv(self.uvs[uv_idx])
                glVertex3fv(self.vertices[v_idx])
        glEnd()
    
        # 🧼 Cleanup
        glDisable(GL_TEXTURE_2D)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
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
        self.position[1] += y
        self.position[2] += self.right[2] * x + self.up[2] * y + self.front[2] * z
    
    def move(self, x, y, z):
        self.position[0] += x
        self.position[1] += y
        self.position[2] += z

    def apply(self):
        self.update_vectors()
        target = [self.position[i] + self.front[i] for i in range(3)]
        glLoadIdentity()
        gluLookAt(*self.position, *target, 0, 1, 0)

# --- ENGINE / MAIN LOOP ---
class Engine3D:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF | OPENGL)
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

def load_obj_with_uv(path):
    vertices = []
    uvs = []
    faces = []

    with open(path, 'r') as file:
        for line in file:
            if line.startswith('v '):  # Vertex position
                parts = line.strip().split()
                vertex = list(map(float, parts[1:4]))
                vertices.append(vertex)

            elif line.startswith('vt '):  # Texture coordinate
                parts = line.strip().split()
                uv = list(map(float, parts[1:3]))
                uvs.append(uv)

            elif line.startswith('f '):  # Face line
                face = []
                parts = line.strip().split()[1:]
                for part in parts:
                    indices = part.split('/')
                    v_idx = int(indices[0]) - 1
                    uv_idx = int(indices[1]) - 1 if len(indices) > 1 and indices[1] != '' else 0
                    face.append((v_idx, uv_idx))
                faces.append(face)

    return vertices, uvs, faces

if __name__ == "__main__":
    main()