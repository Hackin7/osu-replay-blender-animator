import bpy.ops

import bpy
from bpy import context

# Get the current scene
scene = context.scene

# Get the 3D cursor location
#cursor = scene.cursor.location

# Get the active object (assume we have one)
obj = context.active_object
print(obj.location)


with open("D:\\Users\\zunmu\\Documents\\Stuff\\Work In Progress\\Projects\\osu\\data.txt",) as f:
    data = eval(f.read())
    
def add_keyframe(x, y, z, frame):
    obj.location[0] = x
    obj.location[1] = y 
    obj.location[2] = z
    obj.scale[0] = 1
    obj.scale[1] = 1
    obj.scale[2] = 1
    #obj.keyframe_delete(data_path='location', frame=frame)
    obj.keyframe_insert(data_path='location', frame=frame) # , index=2
    obj.keyframe_insert(data_path='scale', frame=frame)
    
    
time_counter = 0 # Time passed in milliseconds
xtransform = lambda x : x/100
ytransform = lambda y : y/100
for i in range(len(data)):
    #i - len(data) // 2
    time_counter += data[i][2]
    add_keyframe(
        xtransform(data[i][0]), 
        ytransform(data[i][1]),
        0 if data[i][3] > 0 else -0.4,
        (time_counter / 1000) / (1/60) # current frame
    )
    print(i, data[i][0], data[i][1], time_counter / 1000 * 50) #obj.location)
    #input()
    
    
