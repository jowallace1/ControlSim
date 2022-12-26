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

body = Body(80, 80, window, [width / 2, height / 2])

body.velo = np.array([0.0, -100.0])

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
