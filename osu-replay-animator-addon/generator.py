import bpy
import bpy.ops
from bpy import context

class Generator:
    def __init__(self):
        self.scale_factor = 1/1000
        self.cursor_scale = (0.005, 0.005, 0.005)
        self.dimensions = (512, 384) # for the playfield
        self.tap_bitmask = 31 # default all on
        
        xtransform = lambda x : x * self.scale_factor
        ytransform = lambda y : (self.dimensions[1] - y) * self.scale_factor # Flip direction
        ztransform = lambda z : 0 if (z & self.tap_bitmask) > 0 else 0.4
        self.modes = {
          "x_aim": xtransform, 
          "y_aim": ytransform, 
          "z_tapall": ztransform,
          "none": lambda z : 0
        }
    
    ### Class Methods to Handle Data ###########################################################
    def add_keyframe(obj, x, y, z, frame):
        obj.location = (x, y, z)
        obj.scale = (1, 1, 1)
        #obj.keyframe_delete(data_path='location', frame=frame)
        obj.keyframe_insert(data_path='location', frame=frame) # , index=2
        obj.keyframe_insert(data_path='scale', frame=frame)
    
    ### Object Methods #########################################################################
    
    def generateAssembly(self):
        origin = (0, 0, 0)
        
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.active_object.name = 'osuReplayCursor'
        self.cursor = bpy.context.object
        self.cursor.location = origin
        
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = 'osuReplayCursorVisible'
        self.cursorVisible = bpy.context.object
        self.cursorVisible.location = origin
        self.cursorVisible.scale = self.cursor_scale
        self.cursorVisible.parent = self.cursor
        
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.active_object.name = 'osuReplayPlanePlayfield'
        self.plane = bpy.context.object
        self.plane.scale = (
            self.dimensions[0]*self.scale_factor/2, # Divide to adjust scale factor
            self.dimensions[1]*self.scale_factor/2, 
            1
        )
        self.plane.location = (
            origin[0] + self.dimensions[0]*self.scale_factor/2, # midpoint
            origin[1] + self.dimensions[1]*self.scale_factor/2,
            0
        ) # middle of plane
        
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.active_object.name = 'osuReplayPlaneVideo'
        self.planeVideo = bpy.context.object
        # Hardcoded values based of videos from https://ordr.issou.best/
        self.planeVideo.scale = (
            0.435033, #1280*self.scale_factor, 
            0.244706, #720*self.scale_factor, 
            1
        )
        self.planeVideo.location = (
            0.262399,
            0.189001,
            0
        ) 
        
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.active_object.name = 'osuReplay'
        self.replayObj = bpy.context.object
        self.replayObj.location = origin
        
        self.cursor.parent = self.replayObj
        self.plane.parent = self.replayObj
        self.planeVideo.parent = self.replayObj

    def readDataFromFile(self, filename):
        with open(filename) as f:
            self.setData(eval(f.read()))
            
    def setData(self, data):
        self.replay_data = data
        
    def generateKeyframes(self, aim=True, tapx=False, tap_bitmask=31):
        self.tap_bitmask = tap_bitmask
        #bpy.context.view_layer.objects.active = self.cursor
        time_counter = 0 # Time passed in milliseconds
        
        mode = {
            "xtransform": self.modes["x_aim"] if aim else self.modes["none"],
            "ytransform": self.modes["y_aim"] if aim else self.modes["none"], 
            "ztransform": self.modes["none"] if tapx==False else self.modes["z_tapall"]  
        }
        for i in range(len(self.replay_data)):
            #i - len(data) // 2
            time_counter += self.replay_data[i][2]
            Generator.add_keyframe(
                self.cursor,
                mode["xtransform"](self.replay_data[i][0]), 
                mode["ytransform"](self.replay_data[i][1]),
                mode["ztransform"](self.replay_data[i][3]),
                (time_counter / 1000) / (1/60) # current frame
            )
            #print(i, data[i][0], data[i][1], time_counter / 1000 * 50) 
    def linkVideoToPlane(self, filename, filedirectory):
        #bpy.ops.material.new()# "osuReplayPlaneVideoMaterial")
        self.video_mat = bpy.data.materials.new(name="osuReplayPlaneVideoMaterial") #bpy.data.materials.get("osuReplayPlaneVideoMaterial")
        self.video_mat.use_nodes = True
        
        # Assign it to object
        if self.planeVideo.data.materials:
            # assign to 1st material slot
            self.planeVideo.data.materials[0] = self.video_mat
        else:
            # no slots
            self.planeVideo.data.materials.append(self.video_mat)
        
        bpy.ops.image.open(filepath=filedirectory+filename)
        
        video_mat_links = self.planeVideo.active_material.node_tree.links
        video_mat_nodes = self.planeVideo.active_material.node_tree.nodes
        
        node_texture = video_mat_nodes.new(type='ShaderNodeTexImage')
        node_texture.image = bpy.data.images[filename]
        MAX = 1048574
        node_texture.image_user.frame_duration = MAX # Currently not working
        node_texture.image_user.frame_offset = 217 # Hardcoded
        node_texture.image_user.use_auto_refresh = True # Loop Through Video
                
        video_shader = video_mat_nodes.get('Principled BSDF')
        video_mat_links.new(video_shader.inputs["Base Color"], node_texture.outputs["Color"])
        # bpy.data.materials.remove(self.video_mat)
