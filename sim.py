import numpy as np
import pygame as pg
import matplotlib.pyplot as plt

from src.body import Body
from utils.data import Data
from controllers.simple_pid import SimplePID

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
start = [width / pxScale / 2, height / pxScale / 2]
thrust = 0.1
max_steer = np.pi / 2
body = Body(window, pxScale, 1, 1, start, np.pi / 4, thrust, 0, max_steer)

# Initialize controller
controller = SimplePID(0, 10, 1, 2, 1, max_steer)

# Initialize data
data = Data(10000, 3, labels=["x", "y", "angle"])

while run:
    dt = clock.tick(60) / 1000
    time += dt

    window.fill((0, 0, 0))

    body.kinematics_event(dt)
    controller.update_error(body.angle, dt)

    body.control_event(thrust, controller.evaluate())

    body.draw()

    data.add_series(time, [body.pos[0], body.pos[1], body.angle])

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
    dataArray = data.get_data()

    # create time-series plot
    timeFig, timeAx = plt.subplots()
    timeAx.plot(dataArray[0, :], dataArray[1, :], label="x")
    timeAx.plot(dataArray[0, :], dataArray[2, :], label="y")
    timeAx.plot(dataArray[0, :], dataArray[3, :], label="angle")
    timeAx.legend()

    # create top-down plot
    topFig, topAx = plt.subplots()
    topAx.plot(dataArray[1, :], -(dataArray[2, :] - start[1]) + start[1])  # need to perform some transformations
    topAx.set_xlim([0, width / pxScale])
    topAx.set_ylim([0, height / pxScale])

    plt.show()
