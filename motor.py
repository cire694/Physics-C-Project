from vpython import *

# creating the scene
scene = canvas(title='3D Stator Magnets', width=800, height=600, center=vector(0,0,0), background=color.white)
scene.userzoom = False

# motor configurations
num_magnets = 8
radius = 5       
magnet_length = 2  
magnet_width = 0.25
magnet_height = 5  
angle_offset = pi/4 
magnetic_field = 0.1
angular_velocity_bound = 15
resistance = 1
battery_emf = 0
current = battery_emf / resistance
axis_of_rotation = cylinder(pos=vector(0,0,-magnet_height/2), axis=vector(0,0,magnet_height), radius=0.05, color=color.gray(0.5)) # Central Axis
angle_between_magnets = (pi - 2 * angle_offset) / (num_magnets -1)

# plane settings: 
plane_length = radius * 3/2
plane_width = magnet_height
plane_thickness = 0.1

moment_of_inertia = (1/12) * (plane_length ** 2 + plane_width ** 2) # MOI for Rectangle

# physical constants
mu_0 = 4 * pi * 10**-7

# motor states
current_direction = 1 # 1 is clockwise, -1 is counterclockwise
angular_velocity = vector(0,0,0) # initial angular veclocity 

# visuals
magnetic_field_arrows = []
degree_angle_list = []

dt = 0.01
t = 0


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
]

# Create boxes conecting the armature position vectors
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

############################################################################################
# visuals: 
    
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

def does_pass_angle(angle_list: list, angle : float):
    bound1 = angle_list[0]
    bound2 = angle_list[1]
    diff =  abs(bound2 - bound1)
    if(diff < 10):
        return angle > bound1 and angle < bound2 or angle < bound1 and angle > bound2

# commutator
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




############################################################################################
# sliders:
def voltage_slider_change(slider):
    global battery_emf
    battery_emf = slider.value
    battery_emf_text.text = f"Battery EMF: {battery_emf} V\n"
    current_text.text = f"Current: {current}\n"
    net_emf_text = f"net EMF: {battery_emf - getBackEMF(angular_velocity)}"

def resistance_slide_change(slider):
    global resistance
    resistance = slider.value
    resistance_text.text = f"Resistance: {resistance} Ohms\n"
    current_text.text = f"Current: {current}\n"

def magnetic_field_slider_change(slider):
    global magnetic_field
    magnetic_field = slider.value
    magnetic_field_text.text = f"Magnetic Field: {magnetic_field} T\n"

def angular_velocity_bound_slider_change(slider):
    global angular_velocity_bound
    angular_velocity_bound = slider.value
    angular_velocity_bound_text.text = f"Angular Velocity Bound: {angular_velocity_bound} rad/s\n"


# Creating the sliders
wtext(text = "\nStrength of Magnetic Field: \n")
magnetic_field_slider = slider(min=0, max=10, value=0, step = 1, length=220, bind=magnetic_field_slider_change, right=15)

wtext(text=f"\n Bound: \n\n")
bound_slider = slider(min=1, max=10, value=3, step = 1, length=220, bind=angular_velocity_bound , right=15)
wtext(text="\n Voltage: \n")
voltage_slider = slider(min=0, max=15, value=0, step = 1, length=220, bind=voltage_slider_change, right=15)
wtext(text=f"\n Resistance: \n")
resistance_slider = slider(min=1, max=10, value=0, step = 1, length=220, bind=resistance_slide_change, right=15)



################################################################################################
# physics: 
def getMagneticField():
    return magnetic_field * vec(-1, 0, 0) 

def getNetMagneticField(omega):
    return (magnetic_field  - inducedB(omega)) * vec(-1, 0, 0)

def getWireLength():
    return plane_length * vec(0, 0, current_direction)

def getCurrent(): 
    return current

def getAngle(): 
    return atan2(carved_sections[0].pos.x, carved_sections[0].pos.y)

def getBackEMF(omega): 
    area = plane_width * plane_length
    # this is in radians
    angle =  getAngle()
    return magnetic_field * area * mag(omega) * cos(angle)

def inducedB(omega):
    return mu_0 * getBackEMF(omega) / resistance

def getTorque(): 
    force = getCurrent() * cross(getWireLength(),  getMagneticField())
    r = carved_sections[0].pos
    torque = cross(r, force)
    return torque

def getNetTorque(omega): 
    force = getCurrent() * cross(getWireLength(),  getNetMagneticField(omega))
    r = carved_sections[0].pos
    torque = cross(r, force)
    return torque

def getPower(omega):
    return (battery_emf - getBackEMF(omega)) * getCurrent()

def signum(x):
    return -1 if x < 0 else 1

################################################################################################
# texts:

battery_emf_text = wtext(text=f"Battery EMF: {battery_emf} V\n")
resistance_text = wtext(text=f"Resistance: {resistance} Ohms\n")
magnetic_field_text = wtext(text=f"Magnetic Field: {magnetic_field} T\n")
angular_velocity_bound_text = wtext(text=f"Angular Velocity Bound: {angular_velocity_bound} rad/s\n")
current_text = wtext(text=f"current: {current} amps\n")
net_emf_text = wtext(text=f"net EMf: {battery_emf - getBackEMF(angular_velocity)}\n")


################################################################################################
# buttons:
def current_direction_button_change():
    global current_direction
    current_direction = current_direction * -1
    for field in induced_fields:
        if(field.color == color.red):
            field.color = color.blue
        else:
            field.color = color.red

def magnetic_field_button_change(button):
    for line in magnetic_field_arrows:
        line.visible = not (line.visible)

def reset_button():
    global battery_emf, resistance, angular_velocity, t, angular_velocity_bound, magnetic_field, current_direction
    
    # Reset parameters
    battery_emf = 0
    resistance = 1
    angular_velocity = vec(0, 0, 0)
    t = 0
    angular_velocity_bound = 3
    magnetic_field = 0.1
    current_direction = 1
    
    # Reset sliders
    voltage_slider.value = battery_emf
    resistance_slider.value = resistance
    magnetic_field_slider.value = magnetic_field
    bound_slider.value = angular_velocity_bound

    # Delete existing armature sections
    for section in armature_sections:
        section.visible = False
    armature_sections.clear()

    for section in carved_sections:
        section.visible = False
    carved_sections.clear()
    
    for piece in com_pieces:
        piece.visible = False
    com_pieces.clear()

    for field in induced_fields:
        field.visible = False
    induced_fields.clear()

    # Recreate armature sections
    for i in range(len(circuit_perimeter) - 1):
        section_length = mag(circuit_perimeter[i] - circuit_perimeter[i+1])
        section_center = (circuit_perimeter[i] + circuit_perimeter[i+1]) / 2
        section_direction = norm(circuit_perimeter[i+1] - circuit_perimeter[i])
        section = box(pos=section_center, length=section_length, height=plane_thickness, width=plane_thickness, axis=section_direction, color=color.yellow)
        armature_sections.append(section)
    
    # Recreate carved sections
    for i in range(len(armature_perimeter) - 1):
        if i == 5:
            continue
        section_length = mag(armature_perimeter[i] - armature_perimeter[i+1])
        section_center = (armature_perimeter[i] + armature_perimeter[i+1]) / 2
        section_direction = norm(armature_perimeter[i+1] - armature_perimeter[i])
        section = box(pos=section_center, length=section_length, height=plane_thickness, width=plane_thickness, axis=section_direction, color=color.yellow)
        carved_sections.append(section)

    # Recreate commutator pieces
    for i in range(pieces):
        if (i == pieces / 4 or i == pieces * 3 / 4):
            continue
        angle = i * 2 * pi / pieces
        x = com_radius * cos(angle)
        y = com_radius * sin(angle)
        position = vector(x, y, plane_width)
        rotation_angle = angle + pi / 2
        com = box(pos=position, size=vector(com_length, com_width, com_height), color=color.orange)
        com.rotate(angle=rotation_angle, axis=vector(0, 0, 1))
        com_pieces.append(com)

    # Recreate induced fields
    scale = 0.85
    top_plane = box(pos=vector(0, plane_thickness, 0), length=plane_length * scale, height=plane_thickness * scale, width=plane_width * scale, color=color.red)
    bottom_plane = box(pos=vector(0, -plane_thickness, 0), length=plane_length * scale, height=plane_thickness * scale, width=plane_width * scale, color=color.blue)
    induced_fields.append(top_plane)
    induced_fields.append(bottom_plane)

    # Reset brushes
    right_brush.pos = vector(plane_length / 8 + brush_length / 2, 0, plane_width)
    left_brush.pos = vector(-plane_length / 8 - brush_length / 2, 0, plane_width)

    global angular_velocity_graph, kDots, back_emf_graph, emfDots, power_graph, pDots
    
    # Create new graphs and gdots objects
    angular_velocity_graph.delete()
    back_emf_graph.delete()
    power_graph.delete()
    kDots.delete()
    emfDots.delete()
    pDots.delete()

    angular_velocity_graph = graph(width=350, height=250, xtitle="Time", ytitle="Angular Velocity", align='left', scroll=True, xmin=0, xmax=5)
    kDots = gdots(color=color.red, graph=angular_velocity_graph)

    back_emf_graph = graph(width=350, height=250, xtitle="Time", ytitle="Back EMF", align='left', scroll=True, xmin=0, xmax=5)
    emfDots = gdots(color=color.blue, graph=back_emf_graph)

    power_graph = graph(width=350, height=250, xtitle="Time", ytitle="Power", align='left', scroll=True, xmin=0, xmax=5)
    pDots = gdots(color=color.green, graph=power_graph)


resetbutton = button(bind = reset_button, text = "Reset Simulation" , background = color.white )
wtext(text="\n\n")

wtext(text="\n\n")
clrbtn = button(bind=current_direction_button_change, text='Click to change direction of current!', background=color.white)
wtext(text="\n\n")

magneticFieldButton = button(bind = magnetic_field_button_change, text = "Click to show/hide magnetic field", background = color.white)
wtext(text="\n\n")

resetbutton = button(bind = reset_button, text = "Reset Simulation" , background = color.white )
wtext(text="\n\n")

################################################################################################
# graphs: 
angular_velocity_graph = graph(width=350, height=250, xtitle=("Time"), ytitle=("Angular Velocity"), align='left', scroll=True, xmin=0, xmax=5)
kDots=gdots(color=color.red, graph=angular_velocity_graph)

back_emf_graph = graph(width=350, height=250, xtitle=("Time"), ytitle=("Back EMF"), align='left', scroll=True, xmin=0, xmax=5)
emfDots = gdots(color=color.blue, graph=back_emf_graph)

power_graph = graph(width=350, height=250, xtitle="Time", ytitle="Power", align='left', scroll=True, xmin=0, xmax=5)
pDots = gdots(color=color.green, graph=power_graph)

################################################################################################
# while loop
while True:
    rate(1/dt)

    current = battery_emf / resistance

    curr_angle = degrees(atan2(carved_sections[2].pos.y, carved_sections[2].pos.x ))
    degree_angle_list.append(curr_angle)
    if(len(degree_angle_list) > 2): degree_angle_list.pop(0)
    if len(degree_angle_list) == 2 and (does_pass_angle(degree_angle_list, 90) or does_pass_angle(degree_angle_list, -90)) : 
        current_direction_button_change()

    torque = getNetTorque(angular_velocity)

    angular_acceleration = torque/moment_of_inertia

    # Update Angular Velocity
    angular_velocity += angular_acceleration * dt
    if(angular_velocity.z < 0):
        angular_velocity.z = max(angular_velocity.z, -angular_velocity_bound)
    else:
        angular_velocity.z = min(angular_velocity.z, angular_velocity_bound)
    
    kDots.plot(t, angular_velocity.z)
    emfDots.plot(t, getBackEMF(angular_velocity))
    pDots.plot(t, getPower(angular_velocity))
    
    # Update wire rotation
    for boxi in carved_sections:
        boxi.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z) *  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))
    #Update induced magnetic field rotation
    for field in induced_fields:
        field.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z)*  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))
    #Update commutator rotation
    for piece in com_pieces:
        piece.rotate(angle = mag(angular_velocity) * signum(angular_velocity.z)*  dt, axis= vector(0,0,1),origin=vec(0, 0, 0))

    # debugging: 
    # print(f"torque {torque}")
    # print(angular_acceleration)
    # print(angular_velocity_original - angular_velocity)
    # print(f"magnetic field: {getMagneticField()}")
    # print(f"net magnetic field: {getNetMagneticField(angular_velocity) - getMagneticField()}")
    # print(f"induced b{inducedB(angular_velocity)}")
    # print(f"getBackEMF: {getBackEMF(angular_velocity)}")

    t += dt

# note to self: why doesn't the backemf cause the motor to stop?