import numpy as np
import math

from vector3 import *

class camera:
    def __init__(self):
        self.pos = vec3(0, 0, 0)
        self.vec_x = vec3(1, 0, 0)
        self.vec_y = vec3(0, 1, 0)
        self.vec_z = vec3(0, 0, 1)

    def project3D(self, pt):
        rel_pos = pt - self.pos
        zdot = rel_pos.dot(self.vec_z)
        if not zdot <= 0:
            xp = rel_pos.dot(self.vec_x)/zdot
            yp = rel_pos.dot(self.vec_y)/zdot

            return [xp, yp]

        else:
            return None
