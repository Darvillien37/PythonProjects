from tkinter import Tk, Canvas, mainloop
import numpy as np


master = Tk()

ANT_UP = 0
ANT_RIGHT = 1
ANT_DOWN = 2
ANT_LEFT = 3

CELL_SIZE = 5

interval = 100

world_width = 200
world_height = 200
ant_x = int(world_height / 2)
ant_y = int(world_width / 2)
ant_direction = ANT_UP

grid = np.zeros((world_width, world_height))

world = Canvas(master,
               width=(world_width * CELL_SIZE),
               height=(world_height * CELL_SIZE),
               background="white")
world.pack()


def turn_right():
    global ant_direction
    ant_direction = ant_direction + 1
    if (ant_direction > ANT_LEFT):
        ant_direction = ANT_UP


def turn_left():
    global ant_direction
    ant_direction = ant_direction - 1
    if (ant_direction < ANT_UP):
        ant_direction = ANT_LEFT


def move_forward():
    global ant_x
    global ant_y
    # print("ant_direction ", ant_direction)

    if(ant_direction == ANT_UP):
        ant_y = ant_y - 1
    elif(ant_direction == ANT_RIGHT):
        ant_x = ant_x + 1
    elif(ant_direction == ANT_DOWN):
        ant_y = ant_y + 1
    elif(ant_direction == ANT_LEFT):
        ant_x = ant_x - 1

    if(ant_x > world_width - 1):
        ant_x = 0
    elif (ant_x < 0):
        ant_x = world_width - 1

    if(ant_y > world_height - 1):
        ant_y = 0
    elif (ant_y < 0):
        ant_y = world_height - 1


def process():
    global grid
    state = grid[ant_x][ant_y]
    # print("ant_x ", ant_x, "  ant_y ", ant_y)
    # 0 = white
    # 1 = black
    # 2 = blue

    if(state == 0):
        turn_right()
        grid[ant_x][ant_y] = 1
    elif (state == 1):
        turn_left()
        grid[ant_x][ant_y] = 0
    move_forward()


def draw():
    global world
    world.delete("all")
    for x in range(world_width):
        for y in range(world_height):
            if (grid[x][y] == 1):
                world.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                       (x * CELL_SIZE) + CELL_SIZE, (y * CELL_SIZE) + CELL_SIZE,
                                       fill='black')
    master.update()


while True:
    for j in range(interval):
        process()
    draw()

print("Finished")
mainloop()
