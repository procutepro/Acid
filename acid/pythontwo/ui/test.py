import acid.pythontwo.window.window as ww
from ui import Button, Slider
import random as r

def change_background(screen):
    screen.fill((r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)))

#### -- TESTING CODE -- ####
if __name__ == "__main__":
    ui = ww.window((800, 600), "ui")
    ui.init()

    # Your existing UI elements
    main = Button(ui, pos=(400 - 32, 300 - 32), size=(64, 64), texture="example.png")

    while ui.brorunning:
        ui.loop()
        main.tick(change_background(ui))
        main.draw()
        ui.mupdate()
