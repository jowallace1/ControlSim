import numpy as np
import pygame as pg

# units in meters, seconds, kilograms, radians


class Body:

    # VISUALIZATION VARIABLES
    pixelScale = 1  # pixels per meter

    # OBJECT VARIABLES
    width = 1
    height = 1
    mass = 1

    # translational motion
    pos = np.array([0.0, 0.0])
    velo = np.array([0.0, 0.0])
    accel = np.array([0.0, 0.0])

    # rotational motion
    angle = 0.0
    angVelo = 0.0
    angAccel = 0.0

    # thruster state
    thrust = 0.0
    thrAngle = 0.0

    rect = pg.Rect(width, height, pos[0], pos[1])

    def __init__(self, window, pixelScale, width, height, pos, angle, thrust, thrAngle):

        self.window = window
        self.pixelScale = pixelScale
        self.width = width
        self.height = height

        self.pos = np.array(pos)
        self.angle = angle

        # thruster state
        self.thrust = thrust
        self.thrAngle = thrAngle

        self.rect = pg.Rect(pos[0] - width / 2, pos[1] - height / 2, width, height)

    def draw(self):
        xPos = (self.pos[0] - self.width / 2) * self.pixelScale
        yPos = (self.pos[1] - self.height / 2) * self.pixelScale
        self.rect.update(
            xPos,
            yPos,
            self.width * self.pixelScale,
            self.height * self.pixelScale,
        )
        pg.draw.rect(self.window, (255, 255, 255), self.rect)

    def kinematicsEvent(self, dt):
        self.pos += self.velo * dt
        self.velo += self.accel * dt
        self.accel = self.thrust * np.array([np.sin(self.thrAngle), np.cos(self.thrAngle)]) / self.mass

    def translate(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def move(self, x, y):
        self.pos[0] = x
        self.pos[1] = y
