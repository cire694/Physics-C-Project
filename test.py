from vpython import *

# Set up the scene
scene = canvas(title="3D Semicircle in VPython", width=800, height=600)

# Parameters
radius = 5       # Radius of the semicircle
thickness = 0.1  # Thickness of the semicircle arc
n_segments = 50  # Number of segments to approximate the semicircle

# Create the semicircle using small cylinders
for i in range(n_segments + 1):
    angle = pi * i / n_segments  # Angle from 0 to pi (180 degrees)
    x = radius * cos(angle)      # X coordinate of the point on the semicircle
    y = radius * sin(angle)      # Y coordinate of the point on the semicircle
    cylinder(pos=vector(x, y, 0), axis=vector(-x, -y, 0).norm() * thickness, radius=thickness / 2)

# Add axes for reference
x_axis = cylinder(pos=vector(-radius, 0, 0), axis=vector(2 * radius, 0, 0), radius=0.05, color=color.red)
y_axis = cylinder(pos=vector(0, -radius, 0), axis=vector(0, 2 * radius, 0), radius=0.05, color=color.green)
z_axis = cylinder(pos=vector(0, 0, -radius), axis=vector(0, 0, 2 * radius), radius=0.05, color=color.blue)
