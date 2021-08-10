from tkinter import Scale, Tk, Canvas, mainloop
from numpy import cos, pi, sin
from time import sleep
import random


WORLD_HEIGHT = 600
WORLD_WIDTH = 600
FRAME_RATE_MS = (1/144)
G = 0.1
DAMPENING = 0.9999
# Note the formulas will calculate with the anchor at 0,0.
# where the pendulum is anchored to the Drawing canvas.
PENDULUM_ANCHOR_X = WORLD_HEIGHT / 2
PENDULUM_ANCHOR_Y = WORLD_HEIGHT / 4
MAX_LINE_LEN = 5000

master = Tk()
master.title('Double Pendulum')
c = Canvas(master,
           height=WORLD_HEIGHT,
           width=WORLD_WIDTH,
           background='white')
c.pack()
s = Scale(master)
s.pack()


def draw_circle(world, x, y, r):
    return world.create_oval(x-r, y-r,
                             x+r, y+r,
                             fill='black')


class DoublePendulum:
    def __init__(self, colour='black'):
        # Double Pendulum variable
        self.l1 = 100
        self.l2 = 200
        self.m1 = 20
        self.m2 = 10
        self.a1 = random.uniform(0, 2*pi)
        self.a2 = random.uniform(0, 2*pi)
        self.a1_v = 0.00
        self.a2_v = 0.00
        self.a1_a = 0.0
        self.a2_a = 0.0
        self.trace_points = []
        self.colour = colour
        self.do_dampening = False

    def draw(self, world):
        # calculates from 0,0
        self.x1 = self.l1 * sin(self.a1)
        self.y1 = self.l1 * cos(self.a1)
        self.x2 = self.x1 + (self.l2 * sin(self.a2))
        self.y2 = self.y1 + (self.l2 * cos(self.a2))

        # positions translated to the canvas
        x1_draw = PENDULUM_ANCHOR_X + self.x1
        y1_draw = PENDULUM_ANCHOR_Y + self.y1
        x2_draw = PENDULUM_ANCHOR_X + self.x2
        y2_draw = PENDULUM_ANCHOR_Y + self.y2

        world.create_line(PENDULUM_ANCHOR_X, PENDULUM_ANCHOR_Y,
                          x1_draw, y1_draw)
        draw_circle(world, x1_draw, y1_draw, self.m1)

        world.create_line(x1_draw, y1_draw,
                          x2_draw, y2_draw)
        draw_circle(world, x2_draw, y2_draw, self.m2)

        trace_x = round(x2_draw, 4)
        trace_y = round(y2_draw, 4)
        new_trace_point = (trace_x, trace_y)

        if (len(self.trace_points) > MAX_LINE_LEN):
            del self.trace_points[0]
        if ((len(self.trace_points) < 2) or (new_trace_point != self.trace_points[-1])):
            self.trace_points.append(new_trace_point)

        if(len(self.trace_points) > 2):
            world.create_line(self.trace_points, fill=self.colour)

    def calculate(self):
        num1 = -G * (2*self.m1+self.m2) * sin(self.a1)
        num2 = -self.m2 * G * sin(self.a1 - 2*self.a2)
        num3 = -2*sin(self.a1-self.a2)*self.m2
        num4 = self.a2_v*self.a2_v*self.l2 + self.a1_v*self.a1_v*self.l1*cos(self.a1-self.a2)
        den = self.l1 * (2*self.m1+self.m2-self.m2*cos(2*self.a1-2*self.a2))
        a1_a = (num1+num2+num3*num4)/den

        num1 = 2*sin(self.a1-self.a2)
        num2 = self.a1_v*self.a1_v*self.l1*(self.m1+self.m2)
        num3 = G*(self.m1+self.m2)*cos(self.a1)
        num4 = self.a2_v*self.a2_v*self.l2*self.m2*cos(self.a1-self.a2)
        den = self.l2 * (2*self.m1+self.m2-self.m2*cos(2*self.a1-2*self.a2))
        a2_a = (num1*(num2+num3+num4)) / den

        self.a1_v = self.a1_v + a1_a
        self.a2_v = self.a2_v + a2_a
        self.a1 = self.a1 + self.a1_v
        self.a2 = self.a2 + self.a2_v
        if(self.do_dampening):
            self.a1_v = self.a1_v * DAMPENING
            self.a2_v = self.a2_v * DAMPENING


dp1 = DoublePendulum()
dp2 = DoublePendulum('green')
dp2.a1 = dp1.a1
dp2.a2 = dp1.a2
dp2.do_dampening = True

dp1.draw(c)
dp2.draw(c)
while(True):
    c.delete('all')
    dp1.calculate()
    dp2.calculate()
    dp1.draw(c)
    dp2.draw(c)
    c.update()
    sleep(FRAME_RATE_MS)

mainloop()
