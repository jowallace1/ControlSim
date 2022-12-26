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
    inertia = 1

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

    def draw(self):

        # create standard polygon (centered at origin, unrotated)
        vertices = 0.5 * np.array(
            [[-self.width, self.width, self.width, -self.width], [-self.height, -self.height, self.height, self.height]]
        )

        # rotate standard polygon
        R = np.array([[np.cos(self.angle), -np.sin(self.angle)], [np.sin(self.angle), np.cos(self.angle)]])
        vertices = R @ vertices

        # translate standard polygon
        vertices[:, 0] += self.pos
        vertices[:, 1] += self.pos
        vertices[:, 2] += self.pos
        vertices[:, 3] += self.pos

        pg.draw.polygon(
            self.window,
            (255, 255, 255),
            [
                (vertices[0, 0] * self.pixelScale, vertices[1, 0] * self.pixelScale),
                (vertices[0, 1] * self.pixelScale, vertices[1, 1] * self.pixelScale),
                (vertices[0, 2] * self.pixelScale, vertices[1, 2] * self.pixelScale),
                (vertices[0, 3] * self.pixelScale, vertices[1, 3] * self.pixelScale),
            ],
        )

    def kinematicsEvent(self, dt):
        force = self.thrust * np.array([np.sin(self.thrAngle + self.angle), np.cos(self.thrAngle + self.angle)])
        torque = self.thrust * np.sin(self.thrAngle) * self.height / 2

        self.pos += self.velo * dt
        self.velo += self.accel * dt
        self.accel = force / self.mass

        self.angle += self.angVelo * dt
        self.angVelo += self.angAccel * dt
        self.angAccel = torque / self.inertia

    def translate(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def rotate(self, angle):
        self.angle += angle

    def move(self, x, y, angle):
        self.pos[0] = x
        self.pos[1] = y
        self.angle = angle
