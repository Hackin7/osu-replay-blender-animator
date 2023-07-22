bl_info = {
    "name": "Generate osu Replay Keyframes",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy

import bpy.ops
from bpy import context

class Generator:
    def __init__(self):
        self.scale_factor = 1/1000
        self.dimensions = (512, 384) # for the playfield
    
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
        self.cursorVisible.scale = (0.005, 0.005, 0.005)
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

    def readData(self, filename):
        with open(filename) as f:
            self.replay_data = eval(f.read())

    def generateKeyframes(self):
        #bpy.context.view_layer.objects.active = self.cursor
        time_counter = 0 # Time passed in milliseconds
        xtransform = lambda x : x * self.scale_factor
        ytransform = lambda y : (self.dimensions[1] - y) * self.scale_factor # Flip direction
        ztransform = lambda z : 1 #0 if z > 0 else -0.4
        for i in range(len(self.replay_data)):
            #i - len(data) // 2
            time_counter += self.replay_data[i][2]
            Generator.add_keyframe(
                self.cursor,
                xtransform(self.replay_data[i][0]), 
                ytransform(self.replay_data[i][1]),
                ztransform(self.replay_data[i][3]),
                (time_counter / 1000) / (1/60) # current frame
            )
            #print(i, data[i][0], data[i][1], time_counter / 1000 * 50) 
    def linkVideoToPlane(self):
        #bpy.ops.material.new()# "osuReplayPlaneVideoMaterial")
        self.video_mat = bpy.data.materials.get("osuReplayPlaneVideoMaterial")
        #self.video_mat
        # Assign it to object
        if self.planeVideo.data.materials:
            # assign to 1st material slot
            self.planeVideo.data.materials[0] = self.video_mat
        else:
            # no slots
            self.planeVideo.data.materials.append(self.video_mat)
        
        filename = "render1250840.mp4"
        filepath = "/run/media/hacker/Windows/Users/zunmu/Documents/Stuff/Github/PERSONAL PROJECTS/osu-replay-blender-animator/"+filename
        bpy.ops.image.open(filepath=filepath)
        
        video_mat_links = self.planeVideo.active_material.node_tree.links
        video_mat_nodes = self.planeVideo.active_material.node_tree.nodes
        
        node_texture = video_mat_nodes.new(type='ShaderNodeTexImage')
        node_texture.image = bpy.data.images[filename]
        try:
            node_texture.image_user.frame_duration = 1000000000000 # Max
        except Exception as e:
            print(e)
        node_texture.image_user.frame_offset = 217 # Hardcoded
        node_texture.image_user.use_auto_refresh = True # Loop Through Video
                
        video_shader = video_mat_nodes.get('Principled BSDF')
        video_mat_links.new(video_shader.inputs["Base Color"], node_texture.outputs["Color"])

        # bpy.data.materials.remove(self.video_mat)

class GenerateOsuReplayKeyframes(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.osu_replay_keyframes"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Object with osu Replay Keyframes"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        scene = context.scene
        
        generator = Generator()
        generator.generateAssembly()
        generator.readData("/run/media/hacker/Windows/Users/zunmu/Documents/Stuff/Github/PERSONAL PROJECTS/osu-replay-blender-animator/replay-coordinates-converter/data.txt")
        generator.generateKeyframes()
        #for obj in scene.objects:
        #    obj.location.x += 1.0

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(GenerateOsuReplayKeyframes.bl_idname)

def register():
    bpy.utils.register_class(GenerateOsuReplayKeyframes)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(GenerateOsuReplayKeyframes)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    #register()
    generator = Generator()
    generator.generateAssembly()
    generator.readData("/run/media/hacker/Windows/Users/zunmu/Documents/Stuff/Github/PERSONAL PROJECTS/osu-replay-blender-animator/replay-coordinates-converter/data.txt")
    generator.generateKeyframes()
    generator.linkVideoToPlane()
