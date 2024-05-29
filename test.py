from vpython import *

# Create the scene
scene = canvas(title='3D Stator Magnets', width=800, height=600, center=vector(0,0,0), background=color.white)

# Parameters for the stator
num_magnets = 8 # Number of magnets in the stator
radius = 5       # Radius of the stator
magnet_length = 2  # Length of each magnet
magnet_width = 0.25  # Width of each magnet
magnet_height = 5   # Height of each magnet
angle_offset = pi/4
slab_thickness = 0.4


# Parameters for Wire
axis_of_rotation = cylinder(pos=vector(0,0,-magnet_height/2), axis=vector(0,0,magnet_height), radius=0.05, color=color.gray(0.5)) # Central Axis

#Parameters for Plane
plane_length = radius * 3/2
plane_width = magnet_height
plane_thickness = 0.05
# plane = box(pos=vector(0,0,0), length=plane_length, height=plane_thickness, width=plane_width, color=color.cyan)

perimeter = [
    vector(-plane_length/2, 0, -plane_width/2),
    vector(-plane_length/2, 0, plane_width/2),
    vector(plane_length/2, 0 , plane_width/2),
    vector(plane_length/2, 0, -plane_width/2),
    vector(-plane_length/2, 0, -plane_width/2) # Close the loop
]

carved_sections = []
for i in range(len(perimeter) - 1):
    section_length = mag(perimeter[i] - perimeter[i+1])
    section_center = (perimeter[i] + perimeter[i+1]) / 2
    section_direction = norm(perimeter[i+1] - perimeter[i])
    section = box(pos=section_center, length=section_length, height=plane_thickness, width=plane_thickness, axis=section_direction, color=color.cyan)
    carved_sections.append(section)

#Parameters for Rotational Motion
torque = vector(0,0,0.1)
angular_velocity = vector(0,0,0) # initial angular vecelity
moment_of_inertia = (1/12) * (plane_length ** 2 + plane_width ** 2) # MOI for Rectangle

#Parameters for Time
dt = 0.01
t = 0

# Angle between each magnet
angle_between_magnets = (pi - 2 * angle_offset) / (num_magnets -1)

# Create the magnets
# Creating the north pole magnet
for i in range(num_magnets):
    angle = i * angle_between_magnets - pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    position = vector(x, y, 0)
    rotation_angle = angle + pi / 2
    magnet = box(pos=position, size=vector(magnet_length, magnet_width, magnet_height), color=color.red)
    magnet.rotate(angle=rotation_angle, axis=vector(0, 0, 1))
# Creating the south pole magnet
for i in range(num_magnets):
    angle = i * angle_between_magnets + pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    position = vector(x, y, 0)
    rotation_angle = angle + pi / 2
    magnet = box(pos=position, size=vector(magnet_length, magnet_width, magnet_height), color=color.blue)
    magnet.rotate(angle=rotation_angle, axis=vector(0, 0, 1))



# Add magnetic field lines
def draw_field_line(start_point, direction, length, color=color.blue):
    arrow(pos=start_point, axis=length * direction, color=color,shaftwidth = 0.01)

for i in range(num_magnets):
    angle = i * angle_between_magnets - pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    start_point = vector(x, y, 0)
    direction = vector(-1, 0, 0)
    draw_field_line(start_point, direction, 2*x, color=color.blue)


while True:
    rate(100)

    # Calculate Angular Acceleration
    angular_acceleration = torque/moment_of_inertia

    # Update Angular Velocity
    angular_velocity += angular_acceleration * dt

    # Update plane rotation
    for boxi in carved_sections:
        boxi.rotate(angle = mag(angular_velocity) *  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))


    # Update Time
    t += dt

