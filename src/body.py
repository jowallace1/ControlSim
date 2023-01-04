import numpy as np
import pygame as pg
import matplotlib as plt

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
        # body vertices
        bodyVerts = 0.125 * np.array(
            [[-self.width, self.width, self.width, -self.width], [-self.height, -self.height, self.height, self.height]]
        )

        # thruster vertices
        thrusterVerts = 0.0625 * np.array(
            [
                [-self.width / 2, self.width / 2, self.width / 2, -self.width / 2],
                [-self.height, -self.height, self.height, self.height],
            ]
        )

        # rotate thruster
        thrusterVerts = (
            np.array(
                [
                    [np.cos(self.thrAngle), -np.sin(self.thrAngle)],
                    [np.sin(self.thrAngle), np.cos(self.thrAngle)],
                ]
            )
            @ thrusterVerts
        )

        # translate thruster relative to body
        thrusterVerts += 0.25 * np.array(
            [
                [0, 0, 0, 0],
                [
                    self.height / 2 + self.height / 4,
                    self.height / 2 + self.height / 4,
                    self.height / 2 + self.height / 4,
                    self.height / 2 + self.height / 4,
                ],
            ]
        )

        # rotate everything to body angle
        thrusterVerts = (
            np.array(
                [
                    [np.cos(self.angle), -np.sin(self.angle)],
                    [np.sin(self.angle), np.cos(self.angle)],
                ]
            )
            @ thrusterVerts
        )
        bodyVerts = (
            np.array(
                [
                    [np.cos(self.angle), -np.sin(self.angle)],
                    [np.sin(self.angle), np.cos(self.angle)],
                ]
            )
            @ bodyVerts
        )

        # translate everything to body position
        thrusterVerts[:, 0] += self.pos
        thrusterVerts[:, 1] += self.pos
        thrusterVerts[:, 2] += self.pos
        thrusterVerts[:, 3] += self.pos
        bodyVerts[:, 0] += self.pos
        bodyVerts[:, 1] += self.pos
        bodyVerts[:, 2] += self.pos
        bodyVerts[:, 3] += self.pos

        # draw polygons

        pg.draw.polygon(  # thruster
            self.window,
            (255, 255, 255),
            [
                (thrusterVerts[0, 0] * self.pixelScale, thrusterVerts[1, 0] * self.pixelScale),
                (thrusterVerts[0, 1] * self.pixelScale, thrusterVerts[1, 1] * self.pixelScale),
                (thrusterVerts[0, 2] * self.pixelScale, thrusterVerts[1, 2] * self.pixelScale),
                (thrusterVerts[0, 3] * self.pixelScale, thrusterVerts[1, 3] * self.pixelScale),
            ],
        )

        pg.draw.polygon(  # body
            self.window,
            (255, 255, 255),
            [
                (bodyVerts[0, 0] * self.pixelScale, bodyVerts[1, 0] * self.pixelScale),
                (bodyVerts[0, 1] * self.pixelScale, bodyVerts[1, 1] * self.pixelScale),
                (bodyVerts[0, 2] * self.pixelScale, bodyVerts[1, 2] * self.pixelScale),
                (bodyVerts[0, 3] * self.pixelScale, bodyVerts[1, 3] * self.pixelScale),
            ],
        )

    def kinematicsEvent(self, dt):
        force = self.thrust * np.array([np.sin(self.thrAngle + self.angle), -np.cos(self.thrAngle + self.angle)])
        torque = -self.thrust * np.sin(self.thrAngle) * self.height / 2

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
