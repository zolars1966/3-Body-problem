import random as rand
from body import *
from globals import *


class Environment:
    def __init__(self, *objects, dt=Decimal("0.005")):
        self.objects = objects
        self.objects_count = self.n = self.number = self.num = len(self.objects)
        self.sim_time = 0
        self.dt = dt

        for body in self.objects:
            body.dt = self.dt

    def __str__(self):
        s = "Environment(\n"

        for obj in self.objects:
            s = s + str(obj) + ",\n"

        return s + ")\n"

    @staticmethod
    def length(x, y, z):
        return Decimal.sqrt(x * x + y * y + z * z)

    def add(self, object):
        self.objects.append(object)
        self.objects_count += 1

    def update(self):
        self.sim_time += self.dt

        for i in range(self.objects_count):
            for j in range(i + 1, self.objects_count):
                d1, d2, d3 = (self.objects[i].posx - self.objects[j].posx), \
                             (self.objects[i].posy - self.objects[j].posy), \
                             (self.objects[i].posz - self.objects[j].posz)

                l = self.length(d1, d2, d3) ** 3

                d1 /= l
                d2 /= l
                d3 /= l

                # acceleration
                self.objects[i].a1 -= self.objects[j].mass * d1
                self.objects[i].a2 -= self.objects[j].mass * d2
                self.objects[i].a3 -= self.objects[j].mass * d3

                self.objects[j].a1 += self.objects[i].mass * d1
                self.objects[j].a2 += self.objects[i].mass * d2
                self.objects[j].a3 += self.objects[i].mass * d3

            self.objects[i].update()


def dec(n):
        z = 1

        while n != int(n):
            z *= 10
            n *= 10

        return Decimal(int(n)) / z


# presets

planet = Object(mass=398600.4418, vel=[dec(-0.0001), dec(0), dec(0)], pos=[dec(0.), dec(0.), dec(0.)], rad=6371, color=(100, 150, 255))
sputnik = Object(mass=82.61*6.6743*1e-20, vel=[dec(0), dec(8), dec(0)], pos=[dec(6659.), dec(0.), dec(0)], rad=400, color=(255, 100, 100))
# moon = Object(mass=4902.8695, vel=[0, 5], pos=[10000, 0], rad=1737, color=(100, 100, 100))
moon = Object(mass=4902.8695, vel=[dec(0), dec(1), dec(0)], pos=[dec(392208), dec(0.), dec(0)], rad=1737, color=(100, 100, 100))

# planet = Object(mass=1., vel=[dec(0.), dec(0.002), dec(0.003)], pos=[dec(0.), dec(0.), dec(0.)], rad=0.4, color=(100, 150, 255))
# sputnik = Object(mass=1., vel=[dec(0.002), dec(-0.001), dec(0.)], pos=[dec(10.), dec(0.), dec(2.)], rad=0.4, color=(255, 100, 100))
# moon = Object(mass=1., vel=[dec(0.), dec(-0.001), dec(0.)], pos=[dec(0.), dec(-10.), dec(-2.)], rad=0.4, color=(100, 100, 100))

envPSM = Environment(planet, sputnik, moon)

env_random = Environment(*[Object(mass=dec(rand.randint(500, 5000)), 
                          vel=[dec(rand.random() * 10 - 5), dec(rand.random() * 10 - 5), dec(rand.random() * 10 - 5)], 
                          pos=[dec(rand.randint(-1000, 1000) / 10), dec(rand.randint(-1000, 1000) / 10), dec(rand.randint(-1000, 1000) / 10)], 
                          rad=0.4, 
                          color=(rand.randint(92, 255) * (rand.randint(0, 2) > 0), rand.randint(92, 255) * (rand.randint(0, 2) > 0), rand.randint(92, 255) * (rand.randint(0, 2) > 0))) for _ in range(rand.randint(0, 32))])

env3stable1 = Environment(Object(mass=9.5, vel=[Decimal(-1), Decimal(1), Decimal(0)], 
                                    pos=[Decimal(0), Decimal(0), Decimal(0)], rad=0.5, color=(255, 0, 0)),
                  Object(mass=9.5, vel=[Decimal(1), Decimal(-1), Decimal(0)], 
                                    pos=[Decimal(4), Decimal(1), Decimal(0)], rad=0.5, color=(0, 255, 0)),
                  Object(mass=9.5, vel=[Decimal(1), Decimal(-1), Decimal(0)], 
                                    pos=[Decimal(-4), Decimal(-1), Decimal(0)], rad=0.5, color=(0, 0, 255))
                  )

env3stableX = Environment(Object(mass=100, rad=1, vel=[Decimal(0), Decimal(1), Decimal(0)], 
                                    pos=[Decimal.sqrt(Decimal(30000)) / 3, Decimal(0), Decimal(0)], color=(255, 0, 0)),
                  Object(mass=100, rad=1, vel=[-Decimal.sqrt(Decimal(3)) / 2, Decimal(-1) / 2, Decimal(0)], 
                                    pos=[-Decimal.sqrt(Decimal(30000)) / 6, Decimal(1) / 2 * 100, Decimal(0)], color=(0, 255, 0)),
                  Object(mass=100, rad=1, vel=[Decimal.sqrt(Decimal(3)) / 2, Decimal(-1) / 2, Decimal(0)], 
                                    pos=[-Decimal.sqrt(Decimal(30000)) / 6, Decimal(-1) / 2 * 100, Decimal(0)], color=(0, 0, 255))
                  )

env3stable2 = Environment(Object(mass=4, rad=0.3, vel=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(0), Decimal(Decimal.sqrt(Decimal(2)))], 
                                    pos=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(0), Decimal(-Decimal.sqrt(Decimal(2)))], color=(255, 0, 0)),
                  Object(mass=4, rad=0.3,vel=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2))), Decimal(0)], 
                                    pos=[Decimal(Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2))), Decimal(0)], color=(0, 255, 0)),
                  Object(mass=4, rad=0.3, vel=[Decimal(0), Decimal(Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2)))], 
                                    pos=[Decimal(0), Decimal(-Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2)))], color=(0, 0, 255))
                  )

env3stable3 = Environment(Object(mass=Decimal(10000), rad=20, vel=[Decimal(0.01), Decimal(0), Decimal(0)], pos=[Decimal(0), Decimal(0), Decimal(0)], color=(255, 0, 0)),
                  Object(mass=Decimal(1), rad=2, vel=[Decimal(0), Decimal(0),  Decimal(17)], pos=[Decimal(33), Decimal(0), Decimal(0)], color=(0, 255, 0)),
                  Object(mass=Decimal(10), rad=7, vel=[Decimal(-10), Decimal(0),  Decimal(0)], pos=[Decimal(0), Decimal(-80), Decimal(-60)], color=(0, 0, 255), dt=dt)
        )

env16r1 = Environment(
            Object(pos=[Decimal('-33.3'), Decimal('-12.5'), Decimal('-74.2')], vel=[Decimal('3.771453977868634'), Decimal('0.8664209658798098'), Decimal('-2.2190536102057404')], mass=3923, rad=9.8075, color=(173, 112, 141), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('59.4'), Decimal('-68.6'), Decimal('-47.9')], vel=[Decimal('1.507607190926868'), Decimal('0.6354575350990272'), Decimal('2.753377682987071')], mass=3742, rad=9.355, color=(83, 162, 162), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('44.8'), Decimal('17.5'), Decimal('20.4')], vel=[Decimal('-2.885198536485182'), Decimal('-0.2554423015247326'), Decimal('2.0810116549327564')], mass=533, rad=1.3325, color=(246, 17, 185), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('85.8'), Decimal('-64.9'), Decimal('15.2')], vel=[Decimal('-1.0360955444243116'), Decimal('1.1147698367029228'), Decimal('-2.941000510766889')], mass=875, rad=2.1875, color=(114, 160, 100), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-29.1'), Decimal('-29.3'), Decimal('-99.5')], vel=[Decimal('-0.8107635747044631'), Decimal('4.161754146417981'), Decimal('0.1302179543934221')], mass=4265, rad=10.6625, color=(243, 218, 98), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('5.2'), Decimal('-22.7'), Decimal('49.1')], vel=[Decimal('-2.1964531499509888'), Decimal('-0.96647750165637'), Decimal('0.33542630965336256')], mass=1942, rad=4.855, color=(0, 191, 184), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-8.4'), Decimal('55.1'), Decimal('72.1')], vel=[Decimal('-3.003655245630295'), Decimal('-3.4566349215641476'), Decimal('-4.2972879710872424')], mass=2012, rad=5.03, color=(232, 42, 143), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-84.7'), Decimal('-42.6'), Decimal('-95.2')], vel=[Decimal('-2.0518070063922624'), Decimal('4.6862157812406'), Decimal('1.3459528714003488')], mass=2711, rad=6.7775, color=(56, 155, 55), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-66.9'), Decimal('2.9'), Decimal('-1')], vel=[Decimal('-0.763764465973007'), Decimal('3.8865858618429424'), Decimal('1.8649638151175484')], mass=2999, rad=7.4975, color=(163, 237, 6), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-2.2'), Decimal('-78.3'), Decimal('-76.3')], vel=[Decimal('-2.091663667841348'), Decimal('-2.2458151402064704'), Decimal('-1.5862961230628422')], mass=4997, rad=12.4925, color=(71, 163, 23), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('71.1'), Decimal('27.6'), Decimal('-83.6')], vel=[Decimal('3.107687114467957'), Decimal('-2.0230607473842544'), Decimal('-3.381248975439456')], mass=1896, rad=4.74, color=(221, 62, 213), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-4.2'), Decimal('0.9'), Decimal('60.7')], vel=[Decimal('0.9987880436627262'), Decimal('1.2326779868511896'), Decimal('-2.2738387930237')], mass=4631, rad=11.5775, color=(120, 192, 14), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('27.3'), Decimal('54.4'), Decimal('65.8')], vel=[Decimal('0.3030065883894394'), Decimal('-3.735274048342836'), Decimal('-1.5317262756905244')], mass=801, rad=2.0025, color=(39, 210, 246), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-73.1'), Decimal('-15.2'), Decimal('61.9')], vel=[Decimal('-3.456507726511911'), Decimal('-4.958673988193928'), Decimal('3.2403461478732756')], mass=2919, rad=7.2975, color=(12, 240, 144), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-23.4'), Decimal('-5.9'), Decimal('33.6')], vel=[Decimal('-4.355568434642154'), Decimal('0.5431340973433043'), Decimal('0.05305653047606106')], mass=2283, rad=5.7075, color=(224, 225, 232), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
            Object(pos=[Decimal('-63.5'), Decimal('-27.6'), Decimal('-43.4')], vel=[Decimal('1.264601227865459'), Decimal('-4.22460731683138'), Decimal('2.3942717516074476')], mass=4758, rad=11.895, color=(250, 131, 95), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
                  )

env3r = Environment(Object(pos=[Decimal('84.1'), Decimal('3.8'), Decimal('48.9')], vel=[Decimal('-1.5336438366505148'), Decimal('-4.0148328120435672'), Decimal('-0.9910259716514032')], mass=3021, rad=7.5525, color=(171, 17, 19)),
                  Object(pos=[Decimal('13.9'), Decimal('48.8'), Decimal('-61.5')], vel=[Decimal('2.0747237980108596'), Decimal('2.588222705359718'), Decimal('0.15846378684418916')], mass=3114, rad=7.785, color=(83, 134, 229)),
                  Object(pos=[Decimal('-67.6'), Decimal('-25.8'), Decimal('64.6')], vel=[Decimal('0.8753519863137872'), Decimal('-1.719653053512831'), Decimal('0.6774411642492842')], mass=2800, rad=7.0, color=(186, 151, 83)))

env16r2 = Environment(
        Object(pos=[Decimal('87.3'), Decimal('30.8'), Decimal('-12.5')], vel=[Decimal('2.4944519278206484'), Decimal('4.353920923871897'), Decimal('1.8908690233474524')], mass=4696, rad=11.74, color=(56, 109, 248), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-52.4'), Decimal('98.5'), Decimal('-59.2')], vel=[Decimal('-2.9051709717720056'), Decimal('1.8279141088964044'), Decimal('4.905282809119186')], mass=2387, rad=5.9675, color=(99, 60, 16), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-95.3'), Decimal('47.4'), Decimal('-3.5')], vel=[Decimal('4.364935466978657'), Decimal('-4.693332392829144'), Decimal('-1.118758367381382')], mass=4333, rad=10.8325, color=(155, 33, 123), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-80.4'), Decimal('-65'), Decimal('-99.9')], vel=[Decimal('-3.4748587971669196'), Decimal('3.51211580584141'), Decimal('4.679708629315152')], mass=1251, rad=3.1275, color=(26, 32, 43), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('11.8'), Decimal('-51.2'), Decimal('-15.3')], vel=[Decimal('1.0065967768682862'), Decimal('1.7582005671795928'), Decimal('4.095040979711795')], mass=1825, rad=4.5625, color=(118, 149, 1), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-29.1'), Decimal('95.6'), Decimal('32.8')], vel=[Decimal('-1.665089444609885'), Decimal('-4.871444548897205'), Decimal('2.210113619867781')], mass=2251, rad=5.6275, color=(244, 231, 182), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('88.8'), Decimal('-13'), Decimal('-72.8')], vel=[Decimal('1.4469031293468672'), Decimal('-0.8761877567589939'), Decimal('-1.400023516374671')], mass=4936, rad=12.34, color=(247, 0, 74), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-14'), Decimal('-99.1'), Decimal('32.8')], vel=[Decimal('-2.925956054508438'), Decimal('3.952889808018931'), Decimal('3.80498719085587')], mass=2905, rad=7.2625, color=(199, 84, 168), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('73.9'), Decimal('94.3'), Decimal('-12.7')], vel=[Decimal('1.4143814862177138'), Decimal('-2.0543090017185476'), Decimal('4.988600243251922')], mass=1051, rad=2.6275, color=(225, 151, 165), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('89.6'), Decimal('51.3'), Decimal('65.9')], vel=[Decimal('-1.9209038193601204'), Decimal('-2.470812373828866'), Decimal('-4.612492953097718')], mass=4893, rad=12.2325, color=(77, 27, 20), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('11.9'), Decimal('-46.1'), Decimal('-27.3')], vel=[Decimal('0.23852142844015044'), Decimal('-2.1813159188230456'), Decimal('-4.291869482542249')], mass=2005, rad=5.0125, color=(183, 67, 198), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('10.1'), Decimal('4.8'), Decimal('84.2')], vel=[Decimal('-1.908403236034462'), Decimal('-0.6712516355367465'), Decimal('4.950320393365876')], mass=3471, rad=8.6775, color=(145, 198, 37), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-67.4'), Decimal('6'), Decimal('5.1')], vel=[Decimal('0.015698788454933778'), Decimal('-1.2627302020763798'), Decimal('-4.484984254780249')], mass=771, rad=1.9275, color=(239, 206, 204), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-37.3'), Decimal('94.6'), Decimal('0.3')], vel=[Decimal('-3.505887285639287'), Decimal('0.06736878247153655'), Decimal('0.7974922809709112')], mass=4905, rad=12.2625, color=(52, 159, 23), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('96.4'), Decimal('-34.1'), Decimal('-35.7')], vel=[Decimal('2.472413810173454'), Decimal('-4.165733817465799'), Decimal('-2.851775175678637')], mass=2042, rad=5.105, color=(208, 122, 228), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
        Object(pos=[Decimal('-95.6'), Decimal('69.8'), Decimal('7.7')], vel=[Decimal('-1.92609484479831'), Decimal('-2.813492358047061'), Decimal('-1.4223720476056956')], mass=836, rad=2.09, color=(75, 255, 2), acl=[Decimal('0'), Decimal('0'), Decimal('0')]),
)

env6stable1 = Environment(
                        Object(mass=Decimal(20) / 3, vel=[dec(1), dec(0), dec(0)], pos=[dec(0), dec(0), dec(10)], rad=1, color=(255, 0, 0)),
                        Object(mass=Decimal(20) / 3, vel=[dec(-1), dec(0), dec(0)], pos=[dec(0), dec(0), dec(-10)], rad=1, color=(0, 255, 0)),
                        Object(mass=Decimal(20) / 3, vel=[dec(0), dec(1), dec(0)], pos=[dec(10), dec(0), dec(0)], rad=1, color=(0, 0, 255)),
                        Object(mass=Decimal(20) / 3, vel=[dec(0), dec(-1), dec(0)], pos=[dec(-10), dec(0), dec(0)], rad=1, color=(255, 0, 255)),
                        Object(mass=Decimal(20) / 3, vel=[dec(0), dec(0), dec(1)], pos=[dec(0), dec(10), dec(0)], rad=1, color=(255, 255, 0)),
                        Object(mass=Decimal(20) / 3, vel=[dec(0), dec(0), dec(-1)], pos=[dec(0), dec(-10), dec(0)], rad=1, color=(0, 255, 255))
                )

env6stable2 = Environment(
                        Object(mass=Decimal(6300), vel=[dec(0), dec(10), dec(0)], pos=[dec(0), dec(0), dec(100)], rad=1, color=(255, 0, 0)),
                        Object(mass=Decimal(6300), vel=[dec(0), dec(-10), dec(0)], pos=[dec(0), dec(0), dec(-100)], rad=1, color=(0, 255, 0)),
                        Object(mass=Decimal(6300), vel=[dec(0), dec(0), dec(10)], pos=[dec(100), dec(0), dec(0)], rad=1, color=(0, 0, 255)),
                        Object(mass=Decimal(6300), vel=[dec(0), dec(0), dec(-10)], pos=[dec(-100), dec(0), dec(0)], rad=1, color=(255, 0, 255)),
                        Object(mass=Decimal(6300), vel=[dec(10), dec(0), dec(0)], pos=[dec(0), dec(100), dec(0)], rad=1, color=(255, 255, 0)),
                        Object(mass=Decimal(6300), vel=[dec(-10), dec(0), dec(0)], pos=[dec(0), dec(-100), dec(0)], rad=1, color=(0, 255, 255)),
                        Object(mass=Decimal(0), vel=[dec(0), dec(0), dec(0)], pos=[dec(0), dec(0), dec(0)], rad=1, color=(255, 255, 255)),
                        dt=dt
                )

env4stable = Environment(
            Object(mass=47, vel=[-2, -2, 0], pos=[-4, 4, 5], rad=0.1, color=(255, 0, 0)),
            Object(mass=47, vel=[-2, 2, 0], pos=[4, 4, 5], rad=0.1, color=(255, 0, 0)),
            Object(mass=47, vel=[2, -2, 0], pos=[-4, -4, 5], rad=0.1, color=(255, 0, 0)),
            Object(mass=47, vel=[2, 2, 0], pos=[4, -4, 5], rad=0.1, color=(255, 0, 0)),
        dt=dt)

env4stable1 = Environment(Object(mass=4, rad=0.3, vel=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(0), Decimal(Decimal.sqrt(Decimal(2)))], 
                                    pos=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(0), Decimal(-Decimal.sqrt(Decimal(2)))], color=(255, 0, 0)),
                  Object(mass=4, rad=0.3,vel=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2))), Decimal(0)], 
                                    pos=[Decimal(Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2))), Decimal(0)], color=(0, 255, 0)),
                  Object(mass=4, rad=0.3, vel=[Decimal(0), Decimal(Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2)))], 
                                    pos=[Decimal(0), Decimal(-Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2)))], color=(0, 0, 255)),
                  Object(mass=4, rad=0.3, vel=[Decimal(-Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2))), Decimal(Decimal.sqrt(Decimal(2)))],
                                    pos=[Decimal(Decimal.sqrt(Decimal(2))), Decimal(-Decimal.sqrt(Decimal(2))), Decimal(-Decimal.sqrt(Decimal(2)))], color=(255, 0, 255))
                  )

# env = Environment(Object(mass=1000, pos=[100, -0.001, 10], vel=[0, -0.0000001, 0], color=(0, 0, 0), rad=2.), Object(mass=1000, pos=[-100, 0.001, 10], vel=[0, 0.0000001, 0], color=(0, 0, 0), rad=2.))
env = env_random

# for body in env.objects:
#     body.mass = 10
