import pygame as pg
import acid.pythontwo.window.window as ww
import time

class Button:
    def __init__(self, screen, pos=(0, 0), size=(1, 1), texture="example.png"):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.texture = texture

        self.original_image = pg.image.load(self.texture)
        self.image = pg.transform.scale(self.original_image, self.size)

        self.ans = False
        self.clicked = False  # initialize clicked here!

    def draw(self):
        self.screen.blit(self.image, self.pos)

    def resize(self, new_size):
        self.size = new_size
        self.image = pg.transform.scale(self.original_image, self.size)

    def move(self, new_pos):
        self.pos = new_pos

    def has_hovered(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x, y = self.pos
        w, h = self.size
        # Check if mouse is inside the button rectangle
        return x <= mouse_x <= x + w and y <= mouse_y <= y + h

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.has_hovered():
                self.clicked = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if self.clicked and self.has_hovered():
                self.clicked = False
                self.ans = not self.ans
                return True
            self.clicked = False
        return False


class Slider:
    def __init__(self, x, y, width, min_val, max_val, start_val):
        self.x = x
        self.y = y
        self.width = width
        self.height = 10  # Track height
        self.radius = 8   # Thumb radius
        self.min = min_val
        self.max = max_val
        self.value = start_val
        self.dragging = False

    def draw(self, surface):
        # Draw the track
        track_rect = pg.Rect(self.x, self.y - self.height // 2, self.width, self.height)
        pg.draw.rect(surface, (180, 180, 180), track_rect, border_radius=4)

        # Position of thumb based on value
        t = (self.value - self.min) / (self.max - self.min)
        thumb_x = self.x + t * self.width
        thumb_y = self.y
        pg.draw.circle(surface, (100, 200, 255), (int(thumb_x), int(thumb_y)), self.radius)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self._thumb_collide(event.pos):
                    self.dragging = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pg.MOUSEMOTION:
            if self.dragging:
                mouse_x = event.pos[0]
                t = max(0, min(1, (mouse_x - self.x) / self.width))
                self.value = self.min + t * (self.max - self.min)

    def _thumb_collide(self, pos):
        t = (self.value - self.min) / (self.max - self.min)
        thumb_x = self.x + t * self.width
        thumb_y = self.y
        dx = pos[0] - thumb_x
        dy = pos[1] - thumb_y
        return dx*dx + dy*dy <= self.radius * self.radius