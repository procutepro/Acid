import acid.pythontwo.ThreeD.renderer as TR
import pygame

# --- Main Usage ---
def example_usage():
    center_X, center_Y = 400, 300
    engine = TR.Engine3D()
    camera = engine.camera

    frog = TR.Object3D()
    frog.vertices, frog.faces = TR.load_obj("untitled.obj")

    engine.set_mouse(center_X, center_Y)
    pygame.mouse.get_rel()

    while engine.running:
        engine.loop()
        engine.clear()
        keys = engine.get_key()

        dx, dy = pygame.mouse.get_rel()
        camera.pitch += dy * camera.sensitivity
        camera.yaw   -= dx * camera.sensitivity
        camera.pitch = max(-89.9, min(89.9, camera.pitch))

        if keys[pygame.K_d]:
            camera.bettermove(0.1, 0, 0)
        if keys[pygame.K_a]:
            camera.bettermove(-0.1, 0, 0)
        if keys[pygame.K_w]:
            camera.bettermove(0, 0, 0.1)
        if keys[pygame.K_s]:
            camera.bettermove(0, 0, -0.1)
        if keys[pygame.K_SPACE]:
            camera.bettermove(0, 0.1, 0)
        if keys[pygame.K_LSHIFT]:
            camera.bettermove(0, -0.1, 0)

        camera.apply()
        frog.draw(ignore_colors=True)
        engine.update()

        engine.set_mouse(center_X, center_Y)

    pygame.quit()

if __name__ == "__main__":
    example_usage()

