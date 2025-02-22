import pygame as pg

class window:
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.running = True  # Window running state
    
    def init(self):
        pg.init()
        x = int(self.size[0])
        y = int(self.size[1])
        self.playground = pg.display.set_mode((x, y))
        pg.display.set_caption(self.name)

    def makepixel(self, pos, color):
        x, y = map(int, pos)
        pg.draw.rect(self.playground, color, pg.Rect(x, y, 1, 1))
        pg.display.update()

    def MakeRect(self, pos, size, color):
        x, y = map(int, pos)
        w, h = map(int, size)
        # Convert and validate color components
        r, g, b = color
        r, g, b = int(r), int(g), int(b)
        for comp in (r, g, b):
            if comp < 0 or comp > 255:
                raise ValueError(f"Color component {comp} out of range (0-255)")
        pg.draw.rect(self.playground, (r, g, b), pg.Rect(x, y, w, h))
        pg.display.update()


    
    def MakeCircle(self, pos, radius, color):
        x, y = map(int, pos)
        pg.draw.circle(self.playground, color, (x, y), radius)
        pg.display.update()  # Update display

    def loop(self):
        self.playground.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print(event.type)
                pg.quit()

