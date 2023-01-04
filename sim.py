import numpy as np
import pygame as pg
import matplotlib.pyplot as plt

from src.body import Body
from utils.data import Data

run = True

# Set window
width, height = 800, 800
window = pg.display.set_mode((width, height))
pg.display.set_caption("Simulation")
time = 0

# Create clock
clock = pg.time.Clock()

# Initialize body
body = Body(window, width / 10, 1, 1, [5.0, 5.0], np.pi / 4, 0.1, np.pi / 8)

# Initialize data
data = Data(10000, 4)

while run:
    dt = clock.tick(60) / 1000
    time += dt

    window.fill((0, 0, 0))

    body.kinematicsEvent(dt)
    body.draw()

    data.addSeries(time, body.pos[0], body.pos[1], body.angle)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.display.flip()

pg.quit()
