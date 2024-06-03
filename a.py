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

magnetic_field = 0.1



mu_0 = 4 * pi * 10**-7
resistance = 3

# Parameters for Wire
axis_of_rotation = cylinder(pos=vector(0,0,-magnet_height/2), axis=vector(0,0,magnet_height), radius=0.05, color=color.gray(0.5)) # Central Axis
current = 0.1


#Parameters for Plane
plane_length = radius * 3/2
plane_width = magnet_height
plane_thickness = 0.1

# Direction of Current
current_direction = 1 # 1 is clockwise, -1 is counterclockwise

# Create position vectors of the corners of our wire lopo
armature_perimeter = [
    vector(-plane_length/2, 0, -plane_width/2),
    vector(-plane_length/2, 0, plane_width/2),
    vector(plane_length/2, 0 , plane_width/2),
    vector(plane_length/2, 0, -plane_width/2),
    vector(-plane_length/2, 0, -plane_width/2) # Close the loop
]


armature_perimeter = [
    vector(-plane_length/2, 0, plane_width/2),
    vector(-plane_length/2, 0, -plane_width/2),
    vector(plane_length/2, 0, -plane_width/2),
    vector(plane_length/2, 0 , plane_width/2),
    vector(plane_length/8,0,plane_width/2),
    vector(plane_length/8,0,plane_width),
    vector(-plane_length/8,0,plane_width),
    vector(-plane_length/8,0,plane_width/2),
    vector(-plane_length/2,0, plane_width/2)
    # Close the loop
]

circuit_perimeter = [
    vector(plane_length/8,0, plane_width),
    vector(plane_length, 0,plane_width),
    # vector(plane_length/)
]

# Create boxes coneecting the armature position vectors
carved_sections = []
for i in range(len(armature_perimeter) - 1):
    section_length = mag(armature_perimeter[i] - armature_perimeter[i+1])
    section_center = (armature_perimeter[i] + armature_perimeter[i+1]) / 2
    section_direction = norm(armature_perimeter[i+1] - armature_perimeter[i])
    section = box(pos=section_center, length=section_length, height=plane_thickness, width=plane_thickness, axis=section_direction, color=color.yellow)
    carved_sections.append(section)
#

armature_sections = []
for i in range (len(circuit_perimeter) - 1):
    section_length = mag(circuit_perimeter[i] - circuit_perimeter[i+1])
    section_center = (circuit_perimeter[i] + circuit_perimeter[i+1]) / 2
    section_direction = norm(circuit_perimeter[i+1] - circuit_perimeter[i])
    section = box(pos=section_center, length=section_length, height=plane_thickness, width=plane_thickness, axis=section_direction, color=color.yellow)
    armature_sections.append(section)

# Creating the induced fields from the wire loop
induced_fields = []
scale = 0.85
top_plane = box(pos=vector(0,plane_thickness,0), length=plane_length*scale, height=plane_thickness*scale, width=plane_width * scale, color=color.blue)
bottom_plane = box(pos=vector(0,-plane_thickness,0), length=plane_length*scale, height=plane_thickness * scale, width=plane_width * scale, color=color.red)
induced_fields.append(top_plane)
induced_fields.append(bottom_plane)

#Parameters for Rotational Motion
# torque = vector(0,0,0.1)
angular_velocity = vector(0,0,0) # initial angular veclocity 
# mass_wire = 0.001

# remember to change MOI
moment_of_inertia = (1/12) * (plane_length ** 2 + plane_width ** 2) # MOI for Rectangle

#Parameters for Time
dt = 0.01
t = 0

# Angle between each magnet
angle_between_magnets = (pi - 2 * angle_offset) / (num_magnets -1)


# Function that runs on current slider change
def current_slider_change(slider):
    global current
    current = slider.value
# Function that runs on magnetic field slider change
def magnetic_field_slider_change(slider):
    global magnetic_field
    magnetic_field = slider.value
# Function that runs on current direction button change
def current_direction_button_change():
    global current_direction
    current_direction = current_direction * -1
    for field in induced_fields:
        if(field.color == color.red):
            field.color = color.blue
        else:
            field.color = color.red
# Function that runs on show magnetic field button change
def magnetic_field_button_change(button):
    for line in magnetic_field_arrows:
        line.visible = not (line.visible)


# Creating the sliders
wtext(text = "\nStrength of Magnetic Field: \n")
magnetic_field_slider = slider(min=0, max=10, value=3, step = 1, length=220, bind=magnetic_field_slider_change, right=15)
wtext(text="\nWire Current: \n")
current_slider = slider(min=0, max=5, value=10, step = 1, length=220, bind=current_slider_change , right=15)
wtext(text="\n")
# Create the button to change the direction of current
clrbtn = button(bind=current_direction_button_change, text='Click to change direction of current!', background=color.white)
# Create the button to show/hide the magnetic 
wtext(text="\n")
magneticFieldButton = button(bind = magnetic_field_button_change, text = "Click to show/hide magnetic field", background = color.white)

# Creating the Graph
angular_velocity_graph = graph(width=350, height=250, xtitle=("Time"), ytitle=("Angular Velocity"), align='left', scroll=True, xmin=0, xmax=5)
kDots=gdots(color=color.red, graph=angular_velocity_graph)

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

magnetic_field_arrows = []

# Add magnetic field lines
def draw_field_line(start_point, direction, length, color=color.blue):
    magnetic_field_arrows.append(arrow(pos=start_point, axis=length * direction, color=color,shaftwidth = 0.01))

for i in range(num_magnets):
    angle = i * angle_between_magnets - pi/2 + angle_offset
    x = radius * cos(angle)
    y = radius * sin(angle)
    start_point = vector(x, y, 0)
    direction = vector(-1, 0, 0)
    draw_field_line(start_point, direction, 2*x, color=color.blue)


# Parameters for the commutator
com_radius = plane_length/8
com_length = 0.2
com_width = 0.1
com_height = 1


com_pieces = []
pieces = int(40)
for i in range(pieces):
    if( i == pieces/4 or i == pieces * 3/4):
        continue
    angle = i * 2 * pi/pieces
    x = com_radius * cos(angle)
    y = com_radius * sin(angle)
    position = vector(x,y,plane_width)
    rotation_angle = angle + pi/2
    com = box(pos = position, size = vector(com_length, com_width, com_height), color = color.orange)
    com.rotate(angle=rotation_angle, axis = vector(0,0,1))
    com_pieces.append(com)


def getMagneticField():
    return magnetic_field * vec(-1, 0, 0) 

def getNetMagneticField(omega):
    return (magnetic_field - inducedB(omega)) * vec(-1, 0, 0) 

def getWireLength():
    return plane_length * vec(0, 0, current_direction)

def getCurrent(): 
    return current

def getAngle(): 
    return atan2(carved_sections[0].pos.x, carved_sections[0].pos.y)

# omega is angular velocity
def getBackEMF(omega): 
    area = plane_width * plane_length
    # this is in radians
    angle =  getAngle()
    print(cos(angle))
    return magnetic_field * area * omega * cos(angle)

def inducedB(omega):
    print(getBackEMF(omega))
    return mu_0 * getBackEMF(omega) / resistance
    



def getTorque(): 
    force = getCurrent() * cross(getWireLength(),  getMagneticField())
    r = carved_sections[0].pos
    # box0 = carved_sections[0]
    # angle = sin(atan2(box0.pos.y, box0.pos.x))
    # print(f'r : {r}')
    # print(f'force: {force}')

    torque = cross(r, force)
    return torque

def getNetTorque(omega): 
    force = getCurrent() * cross(getWireLength(),  getNetMagneticField(omega))
    r = carved_sections[0].pos
    # box0 = carved_sections[0]
    # angle = sin(atan2(box0.pos.y, box0.pos.x))
    # print(f'r : {r}')
    # print(f'force: {force}')

    torque = cross(r, force)
    return torque


def signum(x):
    return -1 if x < 0 else 1

# def backEMF():


while True:
    rate(500)

    # print(f'Current Direction Vector : {current_direction}')
    
    # if(abs(carved_sections[2].pos.x) < 0.2):
    #     current_direction_button_change()
    # curr_angle = atan2(carved_sections[2].pos.y, carved_sections[2].pos.x )
    # print(degrees(curr_angle))

    print(f"angle: {getAngle()}")
    # torque = getNetTorque(angular_velocity)
    torque = getTorque()
    
    # Calculate Angular Acceleration
    angular_acceleration = torque/moment_of_inertia


    # Update Angular Velocity
    angular_velocity += angular_acceleration * dt
    kDots.plot(t, angular_velocity.z)

    # angular_velocity = vector(0,0,0)
    inducedB(angular_velocity)
    # print(f"torque: {torque}")
    # Update wire rotation
    # print(f" sign: {signum(angular_velocity.y)}")
    # print(f"angular velocity: {angular_velocity.z}")
    
    # Update wire rotation
    for boxi in carved_sections:
        boxi.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z) *  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))
    #Update induced magnetic field rotation
    for field in induced_fields:
        field.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z)*  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))
    #Update commutator rotation
    for piece in com_pieces:
        piece.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z)*  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))

    # Update Time
    t += dt

