from pygame_markdown import MarkdownRenderer
import pygame as pg
import pygame_gui as pgu

class Button:
    def __init__(self, screen, pos=(0, 0), size=(1, 1), texture="ucol", text="hello", color=(0, 0, 255)):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.texture = texture
        self.text = text
        self.color = color

        if not self.texture == "ucol":
            self.original_image = pg.image.load(self.texture)
            self.image = pg.transform.scale(self.original_image, self.size)

            self.ans = False
            self.clicked = False  # initialize clicked here!

    def draw(self):
        if self.texture == "ucol":
            my_rect = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pg.draw.rect(self.screen, self.color, my_rect)
        else:
            self.screen.blit(self.image, self.pos)
        #self.screen = screen
        #self.pos = pos
        #self.size = size
        #self.texture = texture
        #self.text = text
        #self.color = color

        return {
            "object": ["quad", {
                "pos": self.pos,
                "screen": self.screen,
                "size": self.size,
                "color": self.color,
                "text": self.text,
                "texture": self.texture
            }]
        }
    

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
                return True
            self.clicked = False
        return False

    def tick(self, func):
        if self.clicked:
            func()
        return None

    def update(self, func, event):
        if self.is_clicked(event=event):
            func()

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
    
class TextBox:
    def __init__(self, rect, font, text_color=(0,0,0), bg_color=(255,255,255), text="hi"):
        self.rect = pg.Rect(rect)
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.text = text
        self.active = True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # Toggle active if clicked inside
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pg.K_RETURN:
                return self.text  # Return text when Enter pressed
            else:
                self.text += event.unicode
        return None

    def draw(self, surface):
        # Draw background
        pg.draw.rect(surface, self.bg_color, self.rect)
        # Draw border
        pg.draw.rect(surface, (0,0,0), self.rect, 2)
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surf, (self.rect.x+5, self.rect.y+5))


class MarkdownLabel:
    def __init__(self, screen, pos=(0,0), md_text="", width=-1, height=-1):
        """
        screen  : Pygame surface to draw on
        pos     : top-left position (x, y)
        md_text : Markdown text to render
        width   : width of the Markdown area (-1 = full width of surface)
        height  : height of the Markdown area (-1 = full height of surface)
        """
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.md_text = md_text

        # Create renderer
        self.renderer = MarkdownRenderer()
        if md_text:
            self.renderer.set_markdown_from_string(md_text)
        self.renderer.set_area(screen, pos[0], pos[1], width, height)

    def set_text(self, md_text):
        """Update the Markdown text."""
        self.md_text = md_text
        self.renderer.set_markdown_from_string(md_text)

    def draw(self, pygame_events, mouse_pos, mouse_pressed):
        """Render the Markdown onto the screen. Call this every frame."""
        self.renderer.display(pygame_events, *mouse_pos, mouse_pressed)

### ----HELPER FUCKTIONS---- ###

def calculate_grid_positions(grid, index, cell_size=None, padding=None):
    """
    grid      : ThumbnailGrid object
    index     : index of the item
    cell_size : optional override
    padding   : optional override
    Returns: (x, y) position for this index
    """
    if cell_size is None:
        cell_size = grid.cell_size
    if padding is None:
        padding = grid.padding

    col = index % grid.columns
    row = index // grid.columns

    x = grid.pos[0] + col * (cell_size[0] + padding)
    y = grid.pos[1] + row * (cell_size[1] + padding)
    return (x, y)