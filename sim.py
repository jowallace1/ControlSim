import numpy as np
import pygame as pg
import matplotlib.pyplot as plt

from src.body import Body
from utils.data import Data

run = True
plot = False

# Set window
width, height = 800, 800
pxScale = width / 10
window = pg.display.set_mode((width, height))
pg.display.set_caption("Simulation")
time = 0

# Create clock
clock = pg.time.Clock()

# Initialize body
start = [5.0, 5.0]
body = Body(window, pxScale, 1, 1, start, np.pi / 4, 0.1, np.pi / 8)

# Initialize data
data = Data(10000, 3, labels=["x", "y", "angle"])

while run:
    dt = clock.tick(60) / 1000
    time += dt

    window.fill((0, 0, 0))

    body.kinematicsEvent(dt)
    body.draw()

    data.addSeries(time, [body.pos[0], body.pos[1], body.angle])

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
                plot = True

    pg.display.flip()

pg.quit()

if plot:
    dataArray = data.getData()

    # create time-series plot
    timeFig, timeAx = plt.subplots()
    timeAx.plot(dataArray[0, :], dataArray[1, :], label="x")
    timeAx.plot(dataArray[0, :], dataArray[2, :], label="y")
    timeAx.plot(dataArray[0, :], dataArray[3, :], label="angle")
    timeAx.legend()

    # create top-down plot
    topFig, topAx = plt.subplots()
    # need to translate coords to start at 0,0 and reflect to match window
    topAx.plot(dataArray[1, :], -(dataArray[2, :] - start[1]) + start[1])
    topAx.set_xlim([0, width / pxScale])
    topAx.set_ylim([0, height / pxScale])

    plt.show()
