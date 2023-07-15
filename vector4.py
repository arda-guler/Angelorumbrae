class vec4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2 + self.w**2)**0.5

    def normalized(self):
        m = self.mag()
        if not m == 0:
            return vec4(self.x/m, self.y/m, self.z/m, self.w/m)
        else:
            return vec4(0,0,0,0)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def tolist(self):
        return [self.x, self.y, self.z, self.w]

    def __neg__(self):
        return self * (-1)

    def __add__(self, other):
        return vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, other):
        return vec4(self.x * other, self.y * other, self.z * other, self.w * other)

    def __truediv__(self, other):
        if not other == 0:
            return vec4(self.x / other, self.y / other, self.z / other, self.w / other)
        else:
            print("Attempt to divide vec4 by 0!")
            return None

    def __repr__(self):
        return "Vector4(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w) + ")"

    def __getitem__(self, idx):
        if idx==0:
            return self.x
        elif idx==1:
            return self.y
        elif idx==2:
            return self.z
        elif idx==3:
            return self.w
        else:
            raise IndexError
