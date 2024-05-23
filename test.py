from vpython import *


# Parameters for the stator
num_magnets = 8 # Number of magnets in the stator
radius = 5       # Radius of the stator
magnet_length = 2  # Length of each magnet
magnet_width = 0.25  # Width of each magnet
magnet_height = 5   # Height of each magnet
angle_offset = pi/4
slab_thickness = 0.4

# Create the scene
scene = canvas(title='3D Stator Magnets', width=800, height=600, center=vector(0,0,0), background=color.white)

# Angle between each magnet
angle_between_magnets = (pi - 2 * angle_offset) / (num_magnets -1)

# Create the magnets

# North pole of magnet
for i in range(num_magnets):
    angle = i * angle_between_magnets - pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    position = vector(x, y, 0)
    rotation_angle = angle + pi / 2
    magnet = box(pos=position, size=vector(magnet_length, magnet_width, magnet_height), color=color.red)
    magnet.rotate(angle=rotation_angle, axis=vector(0, 0, 1))
# South pole of magnet
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
    curve(pos=[start_point, start_point + length * direction], color=color)

for i in range(num_magnets):
    angle = i * angle_between_magnets - pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    start_point = vector(x, y, 0)
    direction = vector(cos(angle), sin(angle), 0)
    draw_field_line(start_point, direction, 2, color=color.green)

for i in range(num_magnets):
    angle = i * angle_between_magnets + pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    start_point = vector(x, y, 0)
    direction = vector(cos(angle), sin(angle), 0)
    draw_field_line(start_point, direction, 2, color=color.green)

north_slab = box(pos= vec(0,slab_thickness/2,0), length = radius* 7/6, height = slab_thickness, width = magnet_height, color = color.red) 
south_slab = box(pos= vec(0,-slab_thickness/2,0), length = radius* 7/6, height = slab_thickness, width = magnet_height, color = color.blue) 


while True:
    rate(100)
