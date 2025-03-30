import tkinter 
from tkinter import ttk
import sv_ttk
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sgp4.api import Satrec
from sgp4.api import jday


root = tkinter.Tk()
root.title("Satellite Trajectory Analysis")
root.geometry('1200x800')

# Set the theme to dark mode!
sv_ttk.set_theme("dark")
plt.style.use('dark_background')

# Create a Style instance to make custom styles!
style = ttk.Style()

style.configure('Margin.TLabel', padding=(0, 20, 0, 5))
style.configure('TButton', padding=(10, 10), background="#000")

 # Create frames
left_frame = tkinter.Frame(root, width=500, height=600)
right_frame = tkinter.Frame(root, width=300, height=600)

# Pack frames side by side
left_frame.pack(side="left", fill="both", expand=True)
right_frame.pack(side="left", fill="both", expand=True)

semi_major_axis_label = ttk.Label(right_frame, text="Semi-Major Axis: ", style='Margin.TLabel')
semi_major_axis_label.pack()
semi_major_axis_slider = tkinter.Scale(right_frame, from_=2000, to=50000, tickinterval=10000, orient=tkinter.HORIZONTAL, length=400)
semi_major_axis_slider.pack()

eccentricity_label = ttk.Label(right_frame, text="Eccentricity: ", style='Margin.TLabel')
eccentricity_label.pack()
eccentricity_slider = tkinter.Scale(right_frame, from_=0, to=1, resolution=0.01, tickinterval=0.1, orient=tkinter.HORIZONTAL, length=400)
eccentricity_slider.pack()

inclination_label = ttk.Label(right_frame, text="Inclination: ", style='Margin.TLabel')
inclination_label.pack()
inclination_slider = tkinter.Scale(right_frame, from_=0, to=360, tickinterval=40, orient=tkinter.HORIZONTAL, length=400)
inclination_slider.pack()

raan_label = ttk.Label(right_frame, text="Right Ascension of Ascending Node: ", style='Margin.TLabel')
raan_label.pack()
raan_slider = tkinter.Scale(right_frame, from_=0, to=360, tickinterval=40, orient=tkinter.HORIZONTAL, length=400)
raan_slider.pack()

argument_periapsis_label = ttk.Label(right_frame, text="Argument of Perigee: ", style='Margin.TLabel')
argument_periapsis_label.pack()
argument_periapsis_slider = tkinter.Scale(right_frame, from_=1, to=360, tickinterval=40, orient=tkinter.HORIZONTAL, length=400)
argument_periapsis_slider.pack()

mean_anamoly_label = ttk.Label(right_frame, text="Mean Anomaly: ", style='Margin.TLabel')
mean_anamoly_label.pack()
mean_anamoly_slider = tkinter.Scale(right_frame, from_=1, to=360, tickinterval=40, orient=tkinter.HORIZONTAL, length=400)
mean_anamoly_slider.pack()

# Takes in six Keplarian Elements as parameters and sets the value to the sliders in the GUI
def display_sliders(a, e, i, o, w, v):
    semi_major_axis_slider.set(a)
    eccentricity_slider.set(e)
    inclination_slider.set(i)
    raan_slider.set(o)
    argument_periapsis_slider.set(w)
    mean_anamoly_slider.set(v)

# Default:
# Semi-Major Axis: 10000
# Eccentricity: 0.1
# Inclination: 90
# RAAN: 40
# Argument of Periapsis: 1
# Mean Anamoly: 1
display_sliders(10000, 0.1, 90, 40, 1, 1)

def trace_altitude_graph(tle_one, tle_two):
    satellite = Satrec.twoline2rv(
    tle_one, tle_two
    )

    # Defining the time range
    start_time = 0
    end_time = 24 * 3600  # 1 day
    step = 60  # 1 minute
    times = np.arange(start_time, end_time, step)
    times = np.linspace(start_time, end_time, step)
    
    # Calculate the altitude at each time step
    altitudes = []
    for t in times:
        jd, fr = jday(2024, 4, 1, 0, 0, t)
        # Use SPG4 to get the position details of a satellite
        e, r, v = satellite.sgp4(jd, fr)
        # r represents the position vector of the satellite where:
        # [x, y, z]
        # Calculates the altitude of the satellite above the Earth's surface
        altitude = (r[0]**2 + r[1]**2 + r[2]**2)**0.5 - 6378.135  # Earth's mean radius in kilometers
        altitudes.append(altitude)

    # Intialize a figure and embed it within a canvas
    fig = Figure(figsize = (6, 3), dpi = 100) 
    canvas = FigureCanvasTkAgg(fig, master = left_frame) 
    canvas.get_tk_widget().pack(pady=15)
    plot = fig.add_subplot(111)

    # Plot timestamps and altitude
    plot.plot(times, altitudes)
    plot.grid(True)

    # Draw the plot
    canvas.draw() 

# Default TLE:
# 1 25544U 98067A   21257.91276829  .00000825  00000-0  24323-4 0  9990
# 2 25544  51.6461  89.6503 0003031 120.4862 259.0942 15.4888108230711
trace_altitude_graph("1 25544U 98067A   21257.91276829  .00000825  00000-0  24323-4 0  9990", "2 25544  51.6461  89.6503 0003031 120.4862 259.0942 15.48881082307117")


# Intialize the second figure and canvas and place it within the left frame
fig2 = Figure(figsize = (6, 3), dpi = 100) 
canvas2 = FigureCanvasTkAgg(fig2, master = left_frame) 

# This method takes the six Keplarian Elements and plots them in a 3D graph
def visualize_3d_orbit(a, p, e, o, i, w, fig_vis):
    orbit = pyasl.KeplerEllipse(a=a, per=p, e=e, Omega=o, i=i, w=w)
    t = np.linspace(0, 4, 300)
    pos = orbit.xyzPos(t)

    # Clear the figure if it already exists (allows us to refresh / redraw updated plots)
    if fig_vis:
        fig_vis.clear()
    
    canvas2.get_tk_widget().pack(pady=15)
    plot2 = fig_vis.add_subplot(111, projection='3d')

    # Plots the Earth, trajectory path, and periapsis point of trajectory
    plot2.plot(0, 0, 'bo', markersize=9, label="Earth")
    plot2.plot(pos[::, 1], pos[::, 0], 'k-', label="Satellite Trajectory")
    plot2.plot(pos[0, 1], pos[0, 0], 'g*', label="Periapsis")

    # Draws the plot onto the canvas
    canvas2.draw() 
visualize_3d_orbit(1.0, 1.0, 0.5, 0.0, 30.0, 0.0, fig2)

def retrace_orbit():
    visualize_3d_orbit(semi_major_axis_slider.get(), mean_anamoly_slider.get(), eccentricity_slider.get(), raan_slider.get(), inclination_slider.get(), argument_periapsis_slider.get(), fig2)

trace_button = ttk.Button(right_frame, text="Retrace Orbit", command=retrace_orbit, style='TButton')
trace_button.pack()

def download_csv():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["A", "E", "I", "O", "W", "V"])
        writer.writeheader()
        writer.writerow({
            "A": semi_major_axis_slider.get(), 
            "E": eccentricity_slider.get(), 
            "I": inclination_slider.get(), 
            "O": raan_slider.get(), 
            "W": argument_periapsis_slider.get(), 
            "V": mean_anamoly_slider.get()  
        })

csv_button = ttk.Button(right_frame, text="Download CSV", command=download_csv, style='TButton')
csv_button.pack()

root.mainloop()