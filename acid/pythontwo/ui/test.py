import acid.pythontwo.window.window as ww
from ui import Button, Slider

#### -- TESTING CODE -- ####
if __name__ == "__main__":
    ui = ww.window((800, 600), "ui")
    ui.init()

    # Your existing UI elements
    main = Button(ui.playground, pos=(400 - 32, 300 - 32), size=(64, 64), texture="example.png")
    slider = Slider(200, 500, 400, 0, 255, 0)  # slider at bottom

    is_there = 0

    while ui.brorunning:
        ui.loop()
        ui.fill((255, 255, 255))  # clear screen first

        # Handle events
        slider.handle_event(ui.event)

        if main.is_clicked(ui.event):
            is_there = 1 - is_there

        # Draw everything
        main.draw()
        if is_there == 1:
            ui.MakeRect((0, 0), (64, 64), (slider.value, 0, 255))
        slider.draw(ui.playground)

        ui.mupdate()
