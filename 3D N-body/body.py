from decimal import Decimal


class Object:
    def __init__(self, pos=[0, 0, 0], vel=[1, 0, 0], mass=1., rad=1, color=(255, 255, 255), dt=Decimal("0.005"), acl=[0, 0, 0], fps=60):
        self.posx, self.posy, self.posz = list(map(Decimal, pos))
        self.fpos = list(map(float, pos))
        self.velx, self.vely, self.velz = list(map(Decimal, vel))
        self.mass = Decimal(mass)
        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)
        self.rad = rad
        self.color = color
        self.traj = [list(map(float, pos))] * 500
        self.dt = dt

    def __str__(self):
        return "Object(pos=" + str((self.posx, self.posy, self.posz)) + ", vel=" + str((self.velx, self.vely, self.velz)) + ", mass=" + str(self.mass) + ", rad=" + str(self.rad) + ", color=" + str(self.color) + ", acl=" + str((self.a1, self.a2, self.a3)) + ")"

    def update(self):
        self.velx += self.a1 * self.dt
        self.vely += self.a2 * self.dt
        self.velz += self.a3 * self.dt

        self.posx += self.velx * self.dt
        self.posy += self.vely * self.dt
        self.posz += self.velz * self.dt

        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)

        self.fpos = float(self.posx), float(self.posy), float(self.posz)

    def update_trajectory(self):
        self.traj = self.traj[1:] + [self.fpos]


class SpoilerTool(Object):
    def update(self):
        self.a1, self.a2, self.a3 = Decimal(0), Decimal(0), Decimal(0)
        self.fpos = float(self.posx), float(self.posy), float(self.posz)

    # def update_trajectory(self):
    #     pass
