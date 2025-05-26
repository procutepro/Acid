import pygame as pg

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

    def MakeImage(self, pos, size, img_path):
        if self.brorunning:
            image = pg.image.load(img_path)
            image = pg.transform.scale(image, size)
            self.playground.blit(image, pos)
    
    def MakeCircle(self, pos, radius, color):
        if self.brorunning:
            x, y = map(int, pos)
            pg.draw.circle(self.playground, color, (x, y), radius)
    
    def makeline(self, point1, point2, color="#FFFFFF"):
        if self.brorunning:
            pg.draw.line(self.playground, color, point1, point2)
            
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
        
    def loop(self):
        if self.brorunning:
            for self.event in pg.event.get():
                if self.event.type == pg.QUIT:
                    self.brorunning = False
                    pg.quit()
    
    def mupdate(self):
        pg.display.update()