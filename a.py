from vpython import *

# Create the scene
scene = canvas(title='3D Stator Magnets', width=800, height=600, center=vector(0,0,0), background=color.white)
scene.userzoom = False
# Parameters for the stator
num_magnets = 8 # Number of magnets in the stator
radius = 5       # Radius of the stator
magnet_length = 2  # Length of each magnet
magnet_width = 0.25  # Width of each magnet
magnet_height = 5   # Height of each magnet
angle_offset = pi/4 

magnetic_field = 0.1


mu_0 = 4 * pi * 10**-7

battery_emf = 0
resistance = 1
current = battery_emf / resistance


# Parameters for Wire
axis_of_rotation = cylinder(pos=vector(0,0,-magnet_height/2), axis=vector(0,0,magnet_height), radius=0.05, color=color.gray(0.5)) # Central Axis


#Parameters for Plane
plane_length = radius * 3/2
plane_width = magnet_height
plane_thickness = 0.1

# Direction of Current
current_direction = 1 # 1 is clockwise, -1 is counterclockwise

# Create position vectors of the corners of our wire loop


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
    vector(plane_length/2, 0,plane_width),
    vector(plane_length/2, 0,  1.5 * plane_width),
    vector(-plane_length/2, 0, 1.5 * plane_width),
    vector(-plane_length/2, 0, plane_width),
    vector(-plane_length/8, 0, plane_width)
    # vector(plane_length/)
]

# Create boxes coneecting the armature position vectors
carved_sections = []
for i in range(len(armature_perimeter) - 1):
    if i == 5:
        continue
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

# Add Brushes
brush_length = 1
brush_width = 0.5
brush_height = 0.5

right_brush = box(pos = vector(plane_length/8 + brush_length/2, 0, plane_width), length = brush_length, height = brush_height, width = brush_width, color=color.black)
left_brush = box(pos = vector(-plane_length/8 - brush_length/2, 0 , plane_width), length = brush_length, height = brush_height, width = brush_width, color=color.black)


# Creating the induced fields from the wire loop
induced_fields = []
scale = 0.85
top_plane = box(pos=vector(0,plane_thickness,0), length=plane_length*scale, height=plane_thickness*scale, width=plane_width * scale, color=color.red)
bottom_plane = box(pos=vector(0,-plane_thickness,0), length=plane_length*scale, height=plane_thickness * scale, width=plane_width * scale, color=color.blue)
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
def voltage_slider_change(slider):
    global battery_emf
    battery_emf = slider.value

def resistance_slide_change(slider):
    global resistance
    resistance = slider.value
# Function that runs on magnetic field slider change
def magnetic_field_slider_change(slider):
    global magnetic_field
    magnetic_field = slider.value
def angular_velocity_bound(slider):
    global angular_velocity_bound
    angular_velocity_bound = slider.value
    
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

def reset_button():
    global battery_emf
    battery_emf = 0
    global resistance
    resistance = 1
    global angular_velocity
    angular_velocity = vec(0, 0, 0)


    


# Creating the sliders
wtext(text = "\nStrength of Magnetic Field: \n")
magnetic_field_slider = slider(min=0, max=10, value=0, step = 1, length=220, bind=magnetic_field_slider_change, right=15)

wtext(text=f"\n Bound: {angular_velocity_bound}\n\n")
bound_slider = slider(min=1, max=10, value=3, step = 1, length=220, bind=angular_velocity_bound , right=15)
wtext(text="\n Voltage: \n")
voltage_slider = slider(min=0, max=15, value=0, step = 1, length=220, bind=voltage_slider_change, right=15)
wtext(text=f"\n Resistance: \n")
resistance_slider = slider(min=1, max=1500, value=0, step = 1, length=220, bind=resistance_slide_change, right=15)

wtext(text="\n\n")
# Create the button to change the direction of current
clrbtn = button(bind=current_direction_button_change, text='Click to change direction of current!', background=color.white)
# Create the button to show/hide the magnetic 
wtext(text="\n\n")
magneticFieldButton = button(bind = magnetic_field_button_change, text = "Click to show/hide magnetic field", background = color.white)
wtext(text="\n\n")
resetbutton = button(bind = reset_button, text = "Reset Simulation" , background = color.white )
wtext(text="\n\n")

# Creating the Graph
angular_velocity_graph = graph(width=350, height=250, xtitle=("Time"), ytitle=("Angular Velocity"), align='left', scroll=True, xmin=0, xmax=5)
kDots=gdots(color=color.red, graph=angular_velocity_graph)

back_emf_graph = graph(width=350, height=250, xtitle=("Time"), ytitle=("Back EMF"), align='left', scroll=True, xmin=0, xmax=5)
emfDots = gdots(color=color.blue, graph=back_emf_graph)

power_graph = graph(width=350, height=250, xtitle="Time", ytitle="Power", align='left', scroll=True, xmin=0, xmax=5)
pDots = gdots(color=color.green, graph=power_graph)

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


# list has to be size 2, 
def does_pass_angle(angle_list: list, angle : float):
    bound1 = angle_list[0]
    bound2 = angle_list[1]
    diff =  abs(bound2 - bound1)
    if(diff < 10):
        return angle > bound1 and angle < bound2 or angle < bound1 and angle > bound2

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
    # print(f'inducedB: {inducedB(omega)}')
    return (magnetic_field  - inducedB(omega)) * vec(-1, 0, 0)

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
    # print(f"omega: {omega}")
    return magnetic_field * area * mag(omega) * cos(angle)

def inducedB(omega):
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

    # print(f"net bfield: {getNetMagneticField(omega)}")
    force = getCurrent() * cross(getWireLength(),  getNetMagneticField(omega))
    r = carved_sections[0].pos
    # box0 = carved_sections[0]
    # angle = sin(atan2(box0.pos.y, box0.pos.x))
    # print(f'r : {r}')
    # print(f'force: {force}')

    torque = cross(r, force)
    return torque

def getPower(omega):
    return (battery_emf - getBackEMF(omega)) * getCurrent()

def signum(x):
    return -1 if x < 0 else 1

# def backEMF():

degree_angle_list = []
angular_velocity_bound = 3


# why is omega in the z direction :skull:

while True:
    rate(1/dt)

    # print(f'Current Direction Vector : {current_direction}')
    current = battery_emf / resistance
    # print(f"resistance {resistance}")
    # print(f"voltage {battery_emf}")
    # print(f"current {current}")
    
    curr_angle = degrees(atan2(carved_sections[2].pos.y, carved_sections[2].pos.x ))
    degree_angle_list.append(curr_angle)
    if(len(degree_angle_list) > 2): degree_angle_list.pop(0)
    if len(degree_angle_list) == 2 and (does_pass_angle(degree_angle_list, 90) or does_pass_angle(degree_angle_list, -90)) : 
        current_direction_button_change()

    # print(f"angle: {getAngle()}")
    # torque = getNetTorque(angular_velocity)

    # it's in the z direction bc torque is the axis

    # torque = getNetTorque(angular_velocity)
    torque = getTorque()
    
    # Calculate Angular Acceleration
    angular_acceleration = torque/moment_of_inertia

    # print(f"net torque: {getNetTorque(angular_velocity)}")
    # print(f"torque {getTorque()}")
    # print(f"diff {getNetTorque(angular_velocity) - getTorque()}")


    # Update Angular Velocity
    angular_velocity += angular_acceleration * dt
    if(angular_velocity.z < 0):
        angular_velocity.z = max(angular_velocity.z, -angular_velocity_bound)
    else:
        angular_velocity.z = min(angular_velocity.z, angular_velocity_bound)
    
    kDots.plot(t, angular_velocity.z)
    emfDots.plot(t, getBackEMF(angular_velocity))
    pDots.plot(t, getPower(angular_velocity))
    
    # print(angular_velocity_original - angular_velocity)
    # print(f"magnetic field: {getMagneticField()}")
    # print(f"net magnetic field: {getNetMagneticField(angular_velocity)}")
    # print(f"induced b{inducedB(angular_velocity)}")
    # print(f"getBackEMF: {getBackEMF(angular_velocity)}")
    
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

