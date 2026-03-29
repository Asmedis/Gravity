#imports
from random import randint
from tkinter import *
import math
import threading as thread
import time
import copy
from unittest import expectedFailure

fps = 120
time_delta = 1./fps

global follow_biggest_object
follow_biggest_object = False

#constants
G = 6.67408 * (10 ** -5)

#window
window = Tk()
window.title("Gravity")

#start
global running
def start():
    if start_button["text"] == "Start":
        start_button["text"] = "Stop"
        window_canvas.delete("all")
        window_canvas.unbind("<Button-1>")
        window_canvas.unbind("<Motion>")

    elif start_button["text"] == "Stop":
        start_button["text"] = "Start"
        window_canvas.bind("<Motion>", motion)
        window_canvas.bind("<Button-1>", press)
    
    while start_button["text"] == "Stop":

        time.sleep(time_delta)
        temp_objects = copy.deepcopy(all_objects)
        window.update()
        x=0
        while x < len(all_objects):
            all_objects[x].combine(window_canvas)
            x+=1
        
        for x in range(len(all_objects)):
            all_objects[x].update(temp_objects)     #calculate new positions of objects



        for x in range(len(all_objects)):
            window_canvas.delete(all_objects[x].object)
            
        
        if velocity_lines_button["bg"] == "green":
            for x in range(len(all_objects)):
                try:
                    window_canvas.delete(all_objects[x].vel_line)
                except:
                    pass
        


        for x in range(len(all_objects)):
            all_objects[x].render()                 #render all of the objects


        
        if follow_biggest_button["bg"] == "green":
            if len(all_objects)>0:
                biggest = all_objects[0]
                for x in range(len(all_objects)):
                    if biggest.mass < all_objects[x].mass:
                        biggest = all_objects[x]

                x_from_centre = biggest.location[0] - 450
                y_from_centre = biggest.location[1] - 450
                if x_from_centre < -0.1:
                    for x in range(len(all_objects)):
                        all_objects[x].location[0] = all_objects[x].location[0] + 0.00001 * abs(x_from_centre) * time_speed.get()
                elif x_from_centre > 0.1:
                    for x in range(len(all_objects)):
                        all_objects[x].location[0] = all_objects[x].location[0] - 0.00001 * abs(x_from_centre) * time_speed.get()

                if y_from_centre < -0.1:
                    for x in range(len(all_objects)):
                        all_objects[x].location[1] = all_objects[x].location[1] + 0.00001 * abs(y_from_centre) * time_speed.get()
                elif y_from_centre > 0.1:
                    for x in range(len(all_objects)):
                        all_objects[x].location[1] = all_objects[x].location[1] - 0.00001 * abs(y_from_centre) * time_speed.get()

def clear():
    global all_objects
    all_objects=[]
    window_canvas.delete("all")

def random():
    object_amount = 15
    import random

    for x in range(object_amount):
        x = random.uniform(5,895)
        y = random.uniform(5,895)
        mass = random.uniform(50,1000)
        vel_x = random.uniform(-0.001,0.001)
        vel_y = random.uniform(-0.001,0.001)

        all_objects.append(object([x,y],[vel_x,vel_y],mass))
        all_objects[len(all_objects)-1].render()

def follow_biggest():
    if follow_biggest_button["bg"] == "green":
        follow_biggest_button["bg"] = "red"
    else:
        follow_biggest_button["bg"] = "green"


def toggle_velocity_lines():
    if velocity_lines_button["bg"] == "green":
        velocity_lines_button["bg"] = "red"
    else:
        velocity_lines_button["bg"] = "green"


def toggle_tracer_lines():
    if tracer_lines_button["bg"] == "green":
        tracer_lines_button["bg"] = "red"
        window_canvas.delete("all")
    else:
        tracer_lines_button["bg"] = "green"

#ui
title_location = Label(window, text="Location").grid(row=1,column=0)
title_velocity = Label(window, text="Velocity").grid(row=1,column=3)
title_mass = Label(window, text="Mass").grid(row=1,column=6)

location_x_var = IntVar()
location_y_var = IntVar()
velocity_x_var = IntVar()
velocity_y_var = IntVar()
mass_var = IntVar()
time_speed = IntVar()

input_location_x = Entry(window, width=5, textvariable=location_x_var).grid(row=1,column=1)
input_location_y = Entry(window, width=5, textvariable=location_y_var).grid(row=1,column=2)
input_velocity_x = Scale(window, from_=-10, to=10, orient=HORIZONTAL, length=100, variable=velocity_x_var).grid(row=1,column=4)
input_velocity_y = Scale(window, from_=-10, to=10, orient=HORIZONTAL, length=100, variable=velocity_y_var).grid(row=1,column=5)
input_mass = Scale(window, from_=10, to=10000, orient=HORIZONTAL, length=200, variable=mass_var)
input_mass.set(1000)
input_mass.grid(row=1,column=7)

start_button = Button(text="Start", height=2, width=10,command=start)
start_button.grid(row=2, column=0)

clear_button = Button(text="Clear", height=2, width=10,command=clear)
clear_button.grid(row=2, column=1)

random_button = Button(text="Random", height=2, width=10,command=random)
random_button.grid(row=2, column=2)

follow_biggest_button = Button(text="Follow biggest", height=2, width=10,command=follow_biggest, bg="red")
follow_biggest_button.grid(row=2, column=3)

velocity_lines_button = Button(text="Velocity lines", height=2, width=10,command=toggle_velocity_lines, bg="red")
velocity_lines_button.grid(row=2, column=4)

tracer_lines_button = Button(text="Tracing lines", height=2, width=10,command=toggle_tracer_lines, bg="red")
tracer_lines_button.grid(row=2, column=5)

input_time_speed = Scale(window, from_=1, to=10000, orient=HORIZONTAL, length=200, variable=time_speed)
input_time_speed.set(1)
input_time_speed.grid(row=2,column=7,columnspan=2)
#canvas
window_canvas = Canvas(window, bg="#222222",width=900,height=900,bd=2)
window_canvas.grid(row=3,columnspan=8)


def iliustrate(x,y):
    global temp_oval
    mass = int(input_mass.get())
    r = round(math.sqrt(mass/3.141)/5)
    try:
        window_canvas.delete(temp_oval)
    except:
        pass
    temp_oval = window_canvas.create_oval(x-r,y-r,x+r,y+r, fill="#222222", outline="white")


def motion(event):
    x, y = event.x, event.y
    location_x_var.set(str(x))
    location_y_var.set(str(y))
    iliustrate(x,y)
window_canvas.bind("<Motion>", motion)


zoom_amount = 1
def zoom(event):
    global zoom_amount
    zoom_amount = zoom_amount + float(event.delta) / 120 / 20

    if zoom_amount < 0.05:
        zoom_amount = 0.05

    if start_button["text"] == "Start":
        window_canvas.delete("all")
        for x in range(len(all_objects)):
            all_objects[x].render()

window_canvas.bind("<MouseWheel>", zoom)

#object
class object:
    def __init__(self, location, velocity, mass):
        self.location = location
        self.velocity = velocity
        self.mass = mass
        self.tracers = []
    
    def render(self):
        try:
            #window_canvas.delete(self.object)
            pass
        except:
            pass

        r = round(math.sqrt(self.mass/3.141)/5) * zoom_amount

        offset = 450 - 450 * zoom_amount

        self.object = window_canvas.create_oval(self.location[0] * zoom_amount - r + offset, self.location[1] * zoom_amount + r + offset, self.location[0] * zoom_amount + r + offset, self.location[1] * zoom_amount - r + offset, fill="white", outline="white")
        if velocity_lines_button["bg"] == "green":
            self.vel_line = window_canvas.create_line(self.location[0] * zoom_amount + offset,self.location[1] * zoom_amount + offset, self.location[0]* zoom_amount + offset + self.velocity[0]*15000, self.location[1]* zoom_amount + offset + self.velocity[1]*15000, fill="blue")
        
        if tracer_lines_button["bg"] == "green":
            self.tracer = window_canvas.create_line(self.location[0] * zoom_amount + offset,self.location[1] * zoom_amount + offset, self.location[0]* zoom_amount + offset - self.velocity[0]*5000, self.location[1]* zoom_amount + offset - self.velocity[1]*5000, fill="red")
            self.tracers.append(self.tracer)
  
    def update(self, all):
        for y in range(len(all)):
            distance = math.sqrt(abs(self.location[0] - all[y].location[0]) + abs(self.location[1] - all[y].location[1]))
            if distance > 0:
                force = ((G*self.mass*all[y].mass) / (distance ** 2)) * time_speed.get()
                if force > 0:
                
                    relative_distance = [abs(self.location[0] - all[y].location[0]) *1000000, abs(self.location[1] - all[y].location[1])* 1000000]

                    force_distribution = [relative_distance[0] / (relative_distance[0] + relative_distance[1]), relative_distance[1] / (relative_distance[0] + relative_distance[1])]
                    if self.location[0] > all[y].location[0]:
                        force_distribution[0] = force_distribution[0] * -1
                    if self.location[1] > all[y].location[1]:
                        force_distribution[1] = force_distribution[1] * -1
                    self.velocity[0] += force_distribution[0] * force / self.mass /1000000
                    self.velocity[1] += force_distribution[1] * force / self.mass /1000000
     
        self.location[0] += self.velocity[0]*time_speed.get()
        self.location[1] += self.velocity[1]*time_speed.get()

    def combine(self, window_canvas):
        r1 = round(math.sqrt(self.mass/3.141)/5)
        y = -1
        while y < len(all_objects)-1:
            y += 1
            r2 = round(math.sqrt(all_objects[y].mass/3.141)/5)

            if self != all_objects[y]:
                if abs(self.location[0] - all_objects[y].location[0]) <= r1 and abs(self.location[1] - all_objects[y].location[1]) <= r1:
                    if r1 > r2:
                        all_objects[y].location[0] = self.location[0]
                        all_objects[y].location[1] = self.location[1]                                         
                        all_objects[y].velocity[0] = self.velocity[0] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[0] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].velocity[1] = self.velocity[1] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[1] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].mass = self.mass + all_objects[y].mass
                        
                        
                        window_canvas.delete(self.object)
                        try:
                            all_objects.remove(self)
                        except:
                            pass

                    elif r2 > r1:
                        #all_objects[x].location[0] = (self.location[0] + all_objects[x].location[0]) / 2
                        #all_objects[x].location[1] = (self.location[1] + all_objects[x].location[1]) / 2       #set the position as an average of both positions
                        all_objects[y].velocity[0] = self.velocity[0] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[0] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].velocity[1] = self.velocity[1] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[1] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].mass = self.mass + all_objects[y].mass

                        window_canvas.delete(self.object)
                        try:
                            all_objects.remove(self)
                        except:
                            pass
                    
                    else:
                        all_objects[y].location[0] = (self.location[0] + all_objects[y].location[0]) / 2
                        all_objects[y].location[1] = (self.location[1] + all_objects[y].location[1]) / 2                                 
                        all_objects[y].velocity[0] = self.velocity[0] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[0] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].velocity[1] = self.velocity[1] * self.mass / (self.mass + all_objects[y].mass) + all_objects[y].velocity[1] * all_objects[y].mass / (self.mass + all_objects[y].mass)
                        all_objects[y].mass = self.mass + all_objects[y].mass
            
            

global all_objects
all_objects = []
def press(event):
    all_objects.append(object([float(location_x_var.get()), float(location_y_var.get())], [float(velocity_x_var.get()), float(velocity_y_var.get())], float(mass_var.get())))
    all_objects[len(all_objects)-1].render()


window_canvas.bind("<Button-1>", press)


#close mainloop
window.mainloop()
    