bl_info = {
    "name": "Generate osu Replay Keyframes",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bpy.ops
from bpy import context
from .generator import Generator
from .read_replay_file import read_replay_file

### Blender Addon Code #############################################################

# == GLOBAL VARIABLES
PROPS = [
    ('replay_file', bpy.props.StringProperty(name='Processed Replay File Path', default='/tmp/replay.osr')),
    ('video_file_directory', bpy.props.StringProperty(name='Video File Directory', default='/tmp/')),
    ('video_file_name', bpy.props.StringProperty(name='Video File Name', default='file.mp4')),
    ('tapx', bpy.props.BoolProperty(name='TapX', default=False)),
]

class SamplePanel(bpy.types.Panel):
    """ Displayy panel in 3D view"""
    bl_label = "osu Replay Animator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        
        for (prop_name, _) in PROPS:
            row = col.row()
            if prop_name == 'version':
                row = row.row()
                row.enabled = context.scene.add_version
            row.prop(context.scene, prop_name)
        
        col.operator("object.osu_replay_keyframes", text="Generate Replay Object")

class GenerateOsuReplayKeyframes(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.osu_replay_keyframes"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Generate Object with osu Replay Keyframes"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    
    def execute(self, context):        # execute() is called when running the operator.        
        generator = Generator()
        generator.generateAssembly()
        generator.setData(read_replay_file(context.scene.replay_file))
        generator.generateKeyframes(context.scene.tapx)
        generator.linkVideoToPlane(
            context.scene.video_file_name,
            context.scene.video_file_directory
        )
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.


### Registration #######################################################

classes = (
    SamplePanel, GenerateOsuReplayKeyframes
)
    

def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    for cls in classes:
        bpy.utils.register_class(cls)
        '''
        bpy.types.VIEW3D_MT_object.append(
            lambda self, context: self.layout.operator(GenerateOsuReplayKeyframes.bl_idname)
        )  # Adds the new operator to an existing menu.
        '''

def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
    for cls in classes:
        bpy.utils.unregister_class(cls)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
