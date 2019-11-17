import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import matplotlib
import matplotlib.animation as animation
import tkinter
import cv2
# fig = plt.figure()
# ax = plt.axes(xlim=(0, 2), ylim=(0, 100))
#
# N = 4
# lines = [plt.plot([], [])[0] for _ in range(N)] #lines to animate
#
# rectangles = plt.bar([0.5,1,1.5],[50,40,90],width=0.1) #rectangles to animate
#
# patches = lines + list(rectangles) #things to animate
#
# def init():
#     #init lines
#     for line in lines:
#         line.set_data([], [])
#
#     #init rectangles
#     for rectangle in rectangles:
#         rectangle.set_height(0)
#
#     return patches #return everything that must be updated
#
# def animate(i):
#     #animate lines
#     for j,line in enumerate(lines):
#         line.set_data([0, 2], [10 * j,i])
#
#     #animate rectangles
#     for j,rectangle in enumerate(rectangles):
#         rectangle.set_height(i/(j+1))
#
#     return patches #return everything that must be updated
#
# anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                frames=100, interval=20, blit=True)
#
# # plt.show()

#figure
# fig = plt.figure(1)
# # subplot for current
# ax1 = fig.add_subplot(131, xlim = (0,100), ylim = (0,500))
# line, = ax1.plot([],[])
# ax1.set_ylabel('Current (A)')
#
# #subplot for voltage
# ax2 = fig.add_subplot(132)
# rects1 = ax2.bar(ind1, voltV, width1)
# ax2.grid(True)
# ax2.set_ylim([0,6])
# ax2.set_xlabel('Cell Number')
# ax2.set_ylabel('Voltage (V)')
# ax2.set_title('Real Time Voltage Data')
# ax2.set_xticks(ind1)
#
# #subplot for temperature
# ax3 = fig.add_subplot(133)
# rects2 = ax3.bar(ind2, tempC, width2)
# ax3.grid(True)
# ax3.set_ylim([0,101])
# ax3.set_xlabel('Sensor Number')
# ax3.set_ylabel('temperature (C)')
# ax3.set_title('Real Time Temperature Data')
# ax3.set_xticks(ind2)
#
# def updateAmps(frameNum):
#
#     try:
#     #error check for bad serial data
#         serialString = serialData.readline()
#         serialLine = [float(val) for val in serialString.split()]
#         print (serialLine)
#     finally:
#         print("a")

#
# fig = plt.figure()
# ax1 = fig.add_subplot(2, 1, 1)
# ax2 = fig.add_subplot(2, 1, 2)
#
# ax1.set_ylabel(u'cos(2\u03c0t)')
# ax1.set_xlim(0, 10)
# ax1.set_ylim(-1, 1)
# plt.setp(ax1.get_xticklabels(),visible=False)
#
# ax2.set_xlabel('t')
# ax2.set_ylabel(u'sin(2\u03c0t)')
# ax2.set_xlim(0, 10)
# ax2.set_ylim(-1, 1)

lines = []

#
fig, axs = plt.subplots(1, 3, figsize=(10, 3))
for ax, interp in zip(axs, ['nearest', 'bilinear', 'bicubic']):
    A = np.random.rand(5, 5)
    t = ax.imshow(A, interpolation=interp)
    ax.set_title(interp.capitalize())
    ax.grid(True)
    lines.append(t)

ani = animation.ArtistAnimation(fig,lines,interval=50,blit=True)
plt.show()
# for i in range(10):
#     line1 = ax1.imshow(A)
#     line2 = ax2.imshow(A)
#     print(line1)
#     # line1,  = ax1.plot(t[:i], x[:i], color='black')
#     # line2,  = ax2.plot(t[:i], y[:i], color='black')
#     lines.append([line1, line2])


# Build the animation using ArtistAnimation function

# ani = animation.ArtistAnimation(fig,lines,interval=50,blit=True)
# plt.show()