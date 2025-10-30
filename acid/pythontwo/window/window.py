import pygame as pg

rect_shape = [(0, 0), (2, 0), (2, 2), (0, 2)]

class window:
    def __init__(self, size, name):
        self.brorunning = True
        self.size = size
        self.name = name
    
    def init(self):
        pg.init()
        x = int(self.size[0])
        y = int(self.size[1])
        self.playground = pg.display.set_mode((x, y))
        pg.display.set_caption(self.name)

    def makepixel(self, pos, color):
        if self.brorunning:
            x, y = map(int, pos)
            pg.draw.rect(self.playground, color, pg.Rect(x, y, 1, 1))
            pg.display.update()

    def MakeRect(self, pos, size, color):
        if self.brorunning:
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

    def MakeImage(self, pos, size, img_path):
        if self.brorunning:
            image = pg.image.load(img_path)
            image = pg.transform.scale(image, size)
            self.playground.blit(image, pos)
            pg.display.update()
    
    def MakeCircle(self, pos, radius, color):
        if self.brorunning:
            x, y = map(int, pos)
            pg.draw.circle(self.playground, color, (x, y), radius)
            pg.display.update()  # Update display
    
    def makeline(self, point1, point2, color="#FFFFFF"):
        if self.brorunning:
            pg.draw.line(self.playground, color, point1, point2)
            pg.display.update()
    
    def draw_triangle(self, color, position, points):
        # points are relative to position
        abs_points = [(position[0] + x, position[1] + y) for x, y in points]
        pg.draw.polygon(self.playground, color, abs_points)
    
    def draw_shape(self, color, pos, points):
        abs_points = [(pos[0] + x, pos[1] + y) for x, y in points]
        pg.draw.polygon(self.playground, color, abs_points)
        return {
            "color": color,
            "pos": pos,
            "points": points
        }
            
    def fill(self, colour):
        if self.brorunning:
            self.playground.fill(colour)
        
    def get_mouse_pos(self):
        if self.brorunning:
            return pg.mouse.get_pos()
        else:
            return (0, 0)
    
    def makesound(self, file, mode=0, volume=0.5):
        if self.brorunning:
            pg.mixer.init()
            pg.mixer.music.set_volume(volume)
            sound = pg.mixer.Sound(file)
            sound.play(loops=mode)
    
    def closesound(self):
        pg.mixer.stop()
    
    def mupdate(self):
        pg.display.update()
        
    def loop(self):
        if self.brorunning:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.brorunning = False
                    pg.quit()
