import numpy as np
import pygame as pg
import matplotlib as plt

import utils.utils as utils

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
    ang_velo = 0.0
    ang_accel = 0.0

    # thruster state
    thrust = 0.0
    thr_angle = 0.0
    max_angle = np.pi / 2

    def __init__(self, window, pixelScale, width, height, pos, angle, thrust, thr_angle, max_angle):

        self.window = window
        self.pixelScale = pixelScale
        self.width = width
        self.height = height

        self.pos = np.array(pos)
        self.angle = angle

        # thruster state
        self.thrust = thrust
        self.thr_angle = thr_angle
        self.max_angle = max_angle

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
                    [np.cos(self.thr_angle), -np.sin(self.thr_angle)],
                    [np.sin(self.thr_angle), np.cos(self.thr_angle)],
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

    def control_event(self, thrust, angle):
        self.thr_angle = utils.clamp(angle, -self.max_angle, self.max_angle)
        self.thrust = thrust

    def kinematics_event(self, dt):
        force = self.thrust * np.array([np.sin(self.thr_angle + self.angle), -np.cos(self.thr_angle + self.angle)])
        torque = -self.thrust * np.sin(self.thr_angle) * self.height / 2

        self.pos += self.velo * dt
        self.velo += self.accel * dt
        self.accel = force / self.mass

        self.angle += self.ang_velo * dt
        self.ang_velo += self.ang_accel * dt
        self.ang_accel = torque / self.inertia

    def translate(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def rotate(self, angle):
        self.angle += angle

    def move(self, x, y, angle):
        self.pos[0] = x
        self.pos[1] = y
        self.angle = angle
