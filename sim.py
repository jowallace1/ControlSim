import numpy as np
import pygame as pg
from src.body import Body

# Set window
width, height = 800, 800
window = pg.display.set_mode((width, height))
pg.display.set_caption("Simulation")

# Create rectangle
rect = pg.Rect(width / 2, height / 2, width / 10, height / 10)

run = True
clock = pg.time.Clock()

body = Body(window, width / 10, 1, 1, [5.0, 5.0], 0, 1, np.pi / 4)

body.rotate(np.pi / 4)

while run:
    dt = clock.tick(60) / 1000
    window.fill((0, 0, 0))

    body.kinematicsEvent(dt)
    body.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()
