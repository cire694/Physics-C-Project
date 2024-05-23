from vpython import *

scene = canvas(width = 600, height = 600)
mycurve = curve()
mycurve.append(pos=vector(-1,0,0), color=color.red,
            radius=0.15)
mycurve.append(pos=vector(0,1,0), color=color.red,
            radius=0.15)
mycurve.append(pos=vector(1,0,0), color=color.red,
            radius=0.15)
