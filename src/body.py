import numpy as np
import pygame as pg


class Body:
    width = 10
    height = 10
    pos = np.array([0.0, 0.0])
    velo = np.array([0.0, 0.0])
    accel = np.array([0.0, 0.0])

    rect = pg.Rect(width, height, pos[0], pos[1])

    def __init__(self, width, height, window, pos):
        self.width = width
        self.height = height
        self.window = window
        self.pos = np.array(pos)

        self.rect = pg.Rect(pos[0] - width / 2, pos[1] - height / 2, width, height)

    def draw(self):
        self.rect.update(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2, self.width, self.height)
        pg.draw.rect(self.window, (255, 255, 255), self.rect)

    def kinematicsEvent(self, dt):
        self.pos += self.velo * dt
        self.velo += self.accel * dt

    def translate(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def move(self, x, y):
        self.pos[0] = x
        self.pos[1] = y
