from vpython import *

# Define the scene
scene = canvas(title="Torque on a Plane", width=800, height=600, center=vector(0,0,0), background=color.white)

# Define the plane properties
plane_length = 2
plane_width = 1
plane_thickness = 0.05
plane = box(pos=vector(0,0,0), length=plane_length, height=plane_thickness, width=plane_width, color=color.cyan)

# Define the central axis
axis_rod = cylinder(pos=vector(0,0,-0.5), axis=vector(0,0,1), radius=0.05, color=color.gray(0.5))

# Define parameters for torque and rotation
torque = vector(0,0,0.1)  # Torque applied around the z-axis
angular_velocity = vector(0,0,0)  # Initial angular velocity
moment_of_inertia = (1/12) * (plane_length**2 + plane_width**2)  # Moment of inertia for a rectangle

# Time parameters
dt = 0.01
t = 0

# Label for time
time_label = label(pos=vector(2,2,0), text='Time: 0.0 s', height=16, color=color.black, box=False)

while t < 10:
    rate(100)
    
    # Calculate angular acceleration
    angular_acceleration = torque / moment_of_inertia
    
    # Update angular velocity
    angular_velocity += angular_acceleration * dt
    
    # Update plane rotation
    plane.rotate(angle=mag(angular_velocity) * dt, axis=vector(0,0,1), origin=plane.pos)
    
    # Update time
    t += dt
    
    # Update the label
    time_label.text = 'Time: {:.1f} s'.format(t)
