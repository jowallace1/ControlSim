import numpy as np
import math

# taken from code written as a part of the Spring 2022 PAVE project
class SimplePID:
    # MaxTurnSpeed is fastest turn speed in degrees/s, #dt is timestep in s
    def __init__(self, setPoint, Kp, Ki, Kd, Ks, maxCommand):
        self.setPoint = setPoint
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Ks = Ks
        self.error = self.lastError = 0
        self.derivativeError = self.integralError = self.saturationError = 0
        self.maxCommand = maxCommand

    def update_error(self, currentState, dt):  # update error and setpoint values
        self.error = currentState - self.setPoint  # get error
        self.integralError += (self.error - self.saturationError * self.Ks) * dt  # get cumulative error
        # get derivative of error
        self.derivativeError = (self.error - self.lastError) / dt
        self.lastError = self.error  # save current error

    def get_error(self):
        return self.error

    # maybe create a ramp to avoid integral windup
    def update_setpoint(self, newSetPoint):
        self.setPoint = newSetPoint

    def evaluate(self):  # return command value
        out = self.Kp * self.error + self.Ki * self.integralError + self.Kd * self.derivativeError

        if abs(out) > self.maxCommand:
            outSaturated = math.copysign(self.maxCommand, out)
        else:
            outSaturated = out

        self.saturationError = out - outSaturated

        return outSaturated
