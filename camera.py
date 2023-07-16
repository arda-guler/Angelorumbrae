import numpy as np
import math

from vector3 import *
from matrix3x3 import *

class camera:
    def __init__(self):
        self.pos = vec3(0, 0, 0)
        self.orient = matrix3x3()

        self.vec_x = vec3(self.orient.m11, self.orient.m12, self.orient.m13)
        self.vec_y = vec3(self.orient.m21, self.orient.m22, self.orient.m23)
        self.vec_z = vec3(self.orient.m31, self.orient.m32, self.orient.m33)

    def project3D(self, pt):
        rel_pos = pt - self.pos
        zdot = rel_pos.dot(self.vec_z)
        if not zdot <= 0:
            xp = rel_pos.dot(self.vec_x)/zdot
            yp = rel_pos.dot(self.vec_y)/zdot

            return [xp, yp]

        else:
            return None

    def move(self, movement):
        self.pos += self.vec_x * movement.x + self.vec_y * movement.y + self.vec_z * movement.z

    def rotate(self, rotation):
        self.orient = self.orient.rotate_legacy(rotation)
        self.vec_x = vec3(self.orient.m11, self.orient.m12, self.orient.m13)
        self.vec_y = vec3(self.orient.m21, self.orient.m22, self.orient.m23)
        self.vec_z = vec3(self.orient.m31, self.orient.m32, self.orient.m33)
