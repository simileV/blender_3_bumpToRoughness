# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8 compliant>
""""Nodes based User interface for shaders exported to POV textures."""
import bpy

from bpy.utils import register_class, unregister_class
from bpy.types import Menu, Node, NodeSocket, CompositorNodeTree, TextureNodeTree, Operator
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
)
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem


# ---------------------------------------------------------------- #
# Pov Nodes init
# ---------------------------------------------------------------- #


class PovraySocketUniversal(NodeSocket):
    bl_idname = "PovraySocketUniversal"
    bl_label = "Povray Socket"
    value_unlimited: bpy.props.FloatProperty(default=0.0)
    value_0_1: bpy.props.FloatProperty(min=0.0, max=1.0, default=0.0)
    value_0_10: bpy.props.FloatProperty(min=0.0, max=10.0, default=0.0)
    value_000001_10: bpy.props.FloatProperty(min=0.000001, max=10.0, default=0.0)
    value_1_9: bpy.props.IntProperty(min=1, max=9, default=1)
    value_0_255: bpy.props.IntProperty(min=0, max=255, default=0)
    percent: bpy.props.FloatProperty(min=0.0, max=100.0, default=0.0)

    def draw(self, context, layout, node, text):
        space = context.space_data
        tree = space.edit_tree
        links = tree.links
        if self.is_linked:
            value = []
            for link in links:
                if link.from_node == node:
                    inps = link.to_node.inputs
                    for inp in inps:
                        if inp.bl_idname == "PovraySocketFloat_0_1" and inp.is_linked:
                            prop = "value_0_1"
                            if prop not in value:
                                value.append(prop)
                        if inp.bl_idname == "PovraySocketFloat_000001_10" and inp.is_linked:
                            prop = "value_000001_10"
                            if prop not in value:
                                value.append(prop)
                        if inp.bl_idname == "PovraySocketFloat_0_10" and inp.is_linked:
                            prop = "value_0_10"
                            if prop not in value:
                                value.append(prop)
                        if inp.bl_idname == "PovraySocketInt_1_9" and inp.is_linked:
                            prop = "value_1_9"
                            if prop not in value:
                                value.append(prop)
                        if inp.bl_idname == "PovraySocketInt_0_255" and inp.is_linked:
                            prop = "value_0_255"
                            if prop not in value:
                                value.append(prop)
                        if inp.bl_idname == "PovraySocketFloatUnlimited" and inp.is_linked:
                            prop = "value_unlimited"
                            if prop not in value:
                                value.append(prop)
            if len(value) == 1:
                layout.prop(self, "%s" % value[0], text=text)
            else:
                layout.prop(self, "percent", text="Percent")
        else:
            layout.prop(self, "percent", text=text)

    def draw_color(self, context, node):
        return (1, 0, 0, 1)


class PovraySocketFloat_0_1(NodeSocket):
    bl_idname = "PovraySocketFloat_0_1"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(
        description="Input node Value_0_1", min=0, max=1, default=0
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (0.5, 0.7, 0.7, 1)


class PovraySocketFloat_0_10(NodeSocket):
    bl_idname = "PovraySocketFloat_0_10"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(
        description="Input node Value_0_10", min=0, max=10, default=0
    )

    def draw(self, context, layout, node, text):
        if node.bl_idname == "ShaderNormalMapNode" and node.inputs[2].is_linked:
            layout.label(text="")
            self.hide_value = True
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (0.65, 0.65, 0.65, 1)


class PovraySocketFloat_10(NodeSocket):
    bl_idname = "PovraySocketFloat_10"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(
        description="Input node Value_10", min=-10, max=10, default=0
    )

    def draw(self, context, layout, node, text):
        if node.bl_idname == "ShaderNormalMapNode" and node.inputs[2].is_linked:
            layout.label(text="")
            self.hide_value = True
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (0.65, 0.65, 0.65, 1)


class PovraySocketFloatPositive(NodeSocket):
    bl_idname = "PovraySocketFloatPositive"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(
        description="Input Node Value Positive", min=0.0, default=0
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (0.045, 0.005, 0.136, 1)


class PovraySocketFloat_000001_10(NodeSocket):
    bl_idname = "PovraySocketFloat_000001_10"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(min=0.000001, max=10, default=0.000001)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (1, 0, 0, 1)


class PovraySocketFloatUnlimited(NodeSocket):
    bl_idname = "PovraySocketFloatUnlimited"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(default=0.0)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text, slider=True)

    def draw_color(self, context, node):
        return (0.7, 0.7, 1, 1)


class PovraySocketInt_1_9(NodeSocket):
    bl_idname = "PovraySocketInt_1_9"
    bl_label = "Povray Socket"
    default_value: bpy.props.IntProperty(
        description="Input node Value_1_9", min=1, max=9, default=6
    )

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (1, 0.7, 0.7, 1)


class PovraySocketInt_0_256(NodeSocket):
    bl_idname = "PovraySocketInt_0_256"
    bl_label = "Povray Socket"
    default_value: bpy.props.IntProperty(min=0, max=255, default=0)

    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 1)


class PovraySocketPattern(NodeSocket):
    bl_idname = "PovraySocketPattern"
    bl_label = "Povray Socket"

    default_value: bpy.props.EnumProperty(
        name="Pattern",
        description="Select the pattern",
        items=(
            ("boxed", "Boxed", ""),
            ("brick", "Brick", ""),
            ("cells", "Cells", ""),
            ("checker", "Checker", ""),
            ("granite", "Granite", ""),
            ("leopard", "Leopard", ""),
            ("marble", "Marble", ""),
            ("onion", "Onion", ""),
            ("planar", "Planar", ""),
            ("quilted", "Quilted", ""),
            ("ripples", "Ripples", ""),
            ("radial", "Radial", ""),
            ("spherical", "Spherical", ""),
            ("spotted", "Spotted", ""),
            ("waves", "Waves", ""),
            ("wood", "Wood", ""),
            ("wrinkles", "Wrinkles", ""),
        ),
        default="granite",
    )

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text="Pattern")
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (1, 1, 1, 1)


class PovraySocketColor(NodeSocket):
    bl_idname = "PovraySocketColor"
    bl_label = "Povray Socket"

    default_value: FloatVectorProperty(
        precision=4,
        step=0.01,
        min=0,
        soft_max=1,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="COLOR",
    )

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (1, 1, 0, 1)


class PovraySocketColorRGBFT(NodeSocket):
    bl_idname = "PovraySocketColorRGBFT"
    bl_label = "Povray Socket"

    default_value: FloatVectorProperty(
        precision=4,
        step=0.01,
        min=0,
        soft_max=1,
        default=(0.0, 0.0, 0.0),
        options={"ANIMATABLE"},
        subtype="COLOR",
    )
    f: bpy.props.FloatProperty(default=0.0, min=0.0, max=1.0)
    t: bpy.props.FloatProperty(default=0.0, min=0.0, max=1.0)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    def draw_color(self, context, node):
        return (1, 1, 0, 1)


class PovraySocketTexture(NodeSocket):
    bl_idname = "PovraySocketTexture"
    bl_label = "Povray Socket"
    default_value: bpy.props.IntProperty()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0, 1, 0, 1)


class PovraySocketTransform(NodeSocket):
    bl_idname = "PovraySocketTransform"
    bl_label = "Povray Socket"
    default_value: bpy.props.IntProperty(min=0, max=255, default=0)

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (99 / 255, 99 / 255, 199 / 255, 1)


class PovraySocketNormal(NodeSocket):
    bl_idname = "PovraySocketNormal"
    bl_label = "Povray Socket"
    default_value: bpy.props.IntProperty(min=0, max=255, default=0)

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.65, 0.65, 0.65, 1)


class PovraySocketSlope(NodeSocket):
    bl_idname = "PovraySocketSlope"
    bl_label = "Povray Socket"
    default_value: bpy.props.FloatProperty(min=0.0, max=1.0)
    height: bpy.props.FloatProperty(min=0.0, max=10.0)
    slope: bpy.props.FloatProperty(min=-10.0, max=10.0)

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text="")
            layout.prop(self, "height", text="")
            layout.prop(self, "slope", text="")

    def draw_color(self, context, node):
        return (0, 0, 0, 1)


class PovraySocketMap(NodeSocket):
    bl_idname = "PovraySocketMap"
    bl_label = "Povray Socket"
    default_value: bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.2, 0, 0.2, 1)


class PovrayShaderNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "ObjectNodeTree"


class PovrayTextureNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "TextureNodeTree"


class PovraySceneNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "CompositorNodeTree"


node_categories = [
    PovrayShaderNodeCategory("SHADEROUTPUT", "Output", items=[NodeItem("PovrayOutputNode")]),
    PovrayShaderNodeCategory("SIMPLE", "Simple texture", items=[NodeItem("PovrayTextureNode")]),
    PovrayShaderNodeCategory(
        "MAPS",
        "Maps",
        items=[
            NodeItem("PovrayBumpMapNode"),
            NodeItem("PovrayColorImageNode"),
            NodeItem("ShaderNormalMapNode"),
            NodeItem("PovraySlopeNode"),
            NodeItem("ShaderTextureMapNode"),
            NodeItem("ShaderNodeValToRGB"),
        ],
    ),
    PovrayShaderNodeCategory(
        "OTHER",
        "Other patterns",
        items=[NodeItem("PovrayImagePatternNode"), NodeItem("ShaderPatternNode")],
    ),
    PovrayShaderNodeCategory("COLOR", "Color", items=[NodeItem("PovrayPigmentNode")]),
    PovrayShaderNodeCategory(
        "TRANSFORM",
        "Transform",
        items=[
            NodeItem("PovrayMappingNode"),
            NodeItem("PovrayMultiplyNode"),
            NodeItem("PovrayModifierNode"),
            NodeItem("PovrayTransformNode"),
            NodeItem("PovrayValueNode"),
        ],
    ),
    PovrayShaderNodeCategory(
        "FINISH",
        "Finish",
        items=[
            NodeItem("PovrayFinishNode"),
            NodeItem("PovrayDiffuseNode"),
            NodeItem("PovraySpecularNode"),
            NodeItem("PovrayPhongNode"),
            NodeItem("PovrayAmbientNode"),
            NodeItem("PovrayMirrorNode"),
            NodeItem("PovrayIridescenceNode"),
            NodeItem("PovraySubsurfaceNode"),
        ],
    ),
    PovrayShaderNodeCategory(
        "CYCLES",
        "Cycles",
        items=[
            NodeItem("ShaderNodeAddShader"),
            NodeItem("ShaderNodeAmbientOcclusion"),
            NodeItem("ShaderNodeAttribute"),
            NodeItem("ShaderNodeBackground"),
            NodeItem("ShaderNodeBlackbody"),
            NodeItem("ShaderNodeBrightContrast"),
            NodeItem("ShaderNodeBsdfAnisotropic"),
            NodeItem("ShaderNodeBsdfDiffuse"),
            NodeItem("ShaderNodeBsdfGlass"),
            NodeItem("ShaderNodeBsdfGlossy"),
            NodeItem("ShaderNodeBsdfHair"),
            NodeItem("ShaderNodeBsdfRefraction"),
            NodeItem("ShaderNodeBsdfToon"),
            NodeItem("ShaderNodeBsdfTranslucent"),
            NodeItem("ShaderNodeBsdfTransparent"),
            NodeItem("ShaderNodeBsdfVelvet"),
            NodeItem("ShaderNodeBump"),
            NodeItem("ShaderNodeCameraData"),
            NodeItem("ShaderNodeCombineHSV"),
            NodeItem("ShaderNodeCombineRGB"),
            NodeItem("ShaderNodeCombineXYZ"),
            NodeItem("ShaderNodeEmission"),
            NodeItem("ShaderNodeExtendedMaterial"),
            NodeItem("ShaderNodeFresnel"),
            NodeItem("ShaderNodeGamma"),
            NodeItem("ShaderNodeGeometry"),
            NodeItem("ShaderNodeGroup"),
            NodeItem("ShaderNodeHairInfo"),
            NodeItem("ShaderNodeHoldout"),
            NodeItem("ShaderNodeHueSaturation"),
            NodeItem("ShaderNodeInvert"),
            NodeItem("ShaderNodeLampData"),
            NodeItem("ShaderNodeLayerWeight"),
            NodeItem("ShaderNodeLightFalloff"),
            NodeItem("ShaderNodeLightPath"),
            NodeItem("ShaderNodeMapping"),
            NodeItem("ShaderNodeMaterial"),
            NodeItem("ShaderNodeMath"),
            NodeItem("ShaderNodeMixRGB"),
            NodeItem("ShaderNodeMixShader"),
            NodeItem("ShaderNodeNewGeometry"),
            NodeItem("ShaderNodeNormal"),
            NodeItem("ShaderNodeNormalMap"),
            NodeItem("ShaderNodeObjectInfo"),
            NodeItem("ShaderNodeOutput"),
            NodeItem("ShaderNodeOutputLamp"),
            NodeItem("ShaderNodeOutputLineStyle"),
            NodeItem("ShaderNodeOutputMaterial"),
            NodeItem("ShaderNodeOutputWorld"),
            NodeItem("ShaderNodeParticleInfo"),
            NodeItem("ShaderNodeRGB"),
            NodeItem("ShaderNodeRGBCurve"),
            NodeItem("ShaderNodeRGBToBW"),
            NodeItem("ShaderNodeScript"),
            NodeItem("ShaderNodeSeparateHSV"),
            NodeItem("ShaderNodeSeparateRGB"),
            NodeItem("ShaderNodeSeparateXYZ"),
            NodeItem("ShaderNodeSqueeze"),
            NodeItem("ShaderNodeSubsurfaceScattering"),
            NodeItem("ShaderNodeTangent"),
            NodeItem("ShaderNodeTexBrick"),
            NodeItem("ShaderNodeTexChecker"),
            NodeItem("ShaderNodeTexCoord"),
            NodeItem("ShaderNodeTexEnvironment"),
            NodeItem("ShaderNodeTexGradient"),
            NodeItem("ShaderNodeTexImage"),
            NodeItem("ShaderNodeTexMagic"),
            NodeItem("ShaderNodeTexMusgrave"),
            NodeItem("ShaderNodeTexNoise"),
            NodeItem("ShaderNodeTexPointDensity"),
            NodeItem("ShaderNodeTexSky"),
            NodeItem("ShaderNodeTexVoronoi"),
            NodeItem("ShaderNodeTexWave"),
            NodeItem("ShaderNodeTexture"),
            NodeItem("ShaderNodeUVAlongStroke"),
            NodeItem("ShaderNodeUVMap"),
            NodeItem("ShaderNodeValToRGB"),
            NodeItem("ShaderNodeValue"),
            NodeItem("ShaderNodeVectorCurve"),
            NodeItem("ShaderNodeVectorMath"),
            NodeItem("ShaderNodeVectorTransform"),
            NodeItem("ShaderNodeVolumeAbsorption"),
            NodeItem("ShaderNodeVolumeScatter"),
            NodeItem("ShaderNodeWavelength"),
            NodeItem("ShaderNodeWireframe"),
        ],
    ),
    PovrayTextureNodeCategory(
        "TEXTUREOUTPUT",
        "Output",
        items=[NodeItem("TextureNodeValToRGB"), NodeItem("TextureOutputNode")],
    ),
    PovraySceneNodeCategory("ISOSURFACE", "Isosurface", items=[NodeItem("IsoPropsNode")]),
    PovraySceneNodeCategory("FOG", "Fog", items=[NodeItem("PovrayFogNode")]),
]
# -------- end nodes init
# -------- nodes ui
# -------- Nodes

# def find_node_input(node, name):
# for input in node.inputs:
# if input.name == name:
# return input

# def panel_node_draw(layout, id_data, output_type, input_name):
# if not id_data.use_nodes:
# #layout.operator("pov.material_use_nodes", icon='SOUND')#'NODETREE')
# #layout.operator("pov.use_shading_nodes", icon='NODETREE')
# layout.operator("WM_OT_context_toggle", icon='NODETREE').data_path = \
# "material.pov.material_use_nodes"
# return False

# ntree = id_data.node_tree

# node = find_node(id_data, output_type)
# if not node:
# layout.label(text="No output node")
# else:
# input = find_node_input(node, input_name)
# layout.template_node_view(ntree, node, input)

# return True


class NODE_MT_POV_map_create(Menu):
    """Create maps"""

    bl_idname = "POVRAY_MT_node_map_create"
    bl_label = "Create map"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.map_create")


def menu_func_nodes(self, context):
    ob = context.object
    if hasattr(ob, 'active_material'):
        mat = context.object.active_material
        if mat and context.space_data.tree_type == 'ObjectNodeTree':
            self.layout.prop(mat.pov, "material_use_nodes")
            self.layout.menu(NODE_MT_POV_map_create.bl_idname)
            self.layout.operator("wm.updatepreviewkey")
        if hasattr(mat, 'active_texture') and context.scene.render.engine == 'POVRAY_RENDER':
            tex = mat.active_texture
            if tex and context.space_data.tree_type == 'TextureNodeTree':
                self.layout.prop(tex.pov, "texture_use_nodes")


# -------- object


class ObjectNodeTree(bpy.types.NodeTree):
    """Povray Material Nodes"""

    bl_idname = 'ObjectNodeTree'
    bl_label = 'Povray Object Nodes'
    bl_icon = 'PLUGIN'

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'POVRAY_RENDER'

    @classmethod
    def get_from_context(cls, context):
        ob = context.active_object
        if ob and ob.type not in {'LIGHT'}:
            ma = ob.active_material
            if ma is not None:
                nt_name = ma.node_tree
                if nt_name != '':
                    return nt_name, ma, ma
        return (None, None, None)

    def update(self):
        self.refresh = True


# -------- output # ---------------------------------------------------------------- #


class PovrayOutputNode(Node, ObjectNodeTree):
    """Output"""

    bl_idname = 'PovrayOutputNode'
    bl_label = 'Output'
    bl_icon = 'SHADING_TEXTURE'

    def init(self, context):

        self.inputs.new('PovraySocketTexture', "Texture")

    def draw_buttons(self, context, layout):

        ob = context.object
        layout.prop(ob.pov, "object_ior", slider=True)

    def draw_buttons_ext(self, context, layout):

        ob = context.object
        layout.prop(ob.pov, "object_ior", slider=True)

    def draw_label(self):
        return "Output"


# -------- material # ---------------------------------------------------------------- #
class PovrayTextureNode(Node, ObjectNodeTree):
    """Texture"""

    bl_idname = 'PovrayTextureNode'
    bl_label = 'Simple texture'
    bl_icon = 'SHADING_TEXTURE'

    def init(self, context):

        color = self.inputs.new('PovraySocketColor', "Pigment")
        color.default_value = (1, 1, 1)
        normal = self.inputs.new('NodeSocketFloat', "Normal")
        normal.hide_value = True
        finish = self.inputs.new('NodeSocketVector', "Finish")
        finish.hide_value = True

        self.outputs.new('PovraySocketTexture', "Texture")

    def draw_label(self):
        return "Simple texture"


class PovrayFinishNode(Node, ObjectNodeTree):
    """Finish"""

    bl_idname = 'PovrayFinishNode'
    bl_label = 'Finish'
    bl_icon = 'SHADING_TEXTURE'

    def init(self, context):

        self.inputs.new('PovraySocketFloat_0_1', "Emission")
        ambient = self.inputs.new('NodeSocketVector', "Ambient")
        ambient.hide_value = True
        diffuse = self.inputs.new('NodeSocketVector', "Diffuse")
        diffuse.hide_value = True
        specular = self.inputs.new('NodeSocketVector', "Highlight")
        specular.hide_value = True
        mirror = self.inputs.new('NodeSocketVector', "Mirror")
        mirror.hide_value = True
        iridescence = self.inputs.new('NodeSocketVector', "Iridescence")
        iridescence.hide_value = True
        subsurface = self.inputs.new('NodeSocketVector', "Translucency")
        subsurface.hide_value = True
        self.outputs.new('NodeSocketVector', "Finish")

    def draw_label(self):
        return "Finish"


class PovrayDiffuseNode(Node, ObjectNodeTree):
    """Diffuse"""

    bl_idname = 'PovrayDiffuseNode'
    bl_label = 'Diffuse'
    bl_icon = 'MATSPHERE'

    def init(self, context):

        intensity = self.inputs.new('PovraySocketFloat_0_1', "Intensity")
        intensity.default_value = 0.8
        albedo = self.inputs.new('NodeSocketBool', "Albedo")
        albedo.default_value = False
        brilliance = self.inputs.new('PovraySocketFloat_0_10', "Brilliance")
        brilliance.default_value = 1.8
        self.inputs.new('PovraySocketFloat_0_1', "Crand")
        self.outputs.new('NodeSocketVector', "Diffuse")

    def draw_label(self):
        return "Diffuse"


class PovrayPhongNode(Node, ObjectNodeTree):
    """Phong"""

    bl_idname = 'PovrayPhongNode'
    bl_label = 'Phong'
    bl_icon = 'MESH_UVSPHERE'

    def init(self, context):

        albedo = self.inputs.new('NodeSocketBool', "Albedo")
        intensity = self.inputs.new('PovraySocketFloat_0_1', "Intensity")
        intensity.default_value = 0.8
        phong_size = self.inputs.new('PovraySocketInt_0_256', "Size")
        phong_size.default_value = 60
        metallic = self.inputs.new('PovraySocketFloat_0_1', "Metallic")

        self.outputs.new('NodeSocketVector', "Phong")

    def draw_label(self):
        return "Phong"


class PovraySpecularNode(Node, ObjectNodeTree):
    """Specular"""

    bl_idname = 'PovraySpecularNode'
    bl_label = 'Specular'
    bl_icon = 'MESH_UVSPHERE'

    def init(self, context):

        albedo = self.inputs.new('NodeSocketBool', "Albedo")
        intensity = self.inputs.new('PovraySocketFloat_0_1', "Intensity")
        intensity.default_value = 0.8
        roughness = self.inputs.new('PovraySocketFloat_0_1', "Roughness")
        roughness.default_value = 0.02
        metallic = self.inputs.new('PovraySocketFloat_0_1', "Metallic")

        self.outputs.new('NodeSocketVector', "Specular")

    def draw_label(self):
        return "Specular"


class PovrayMirrorNode(Node, ObjectNodeTree):
    """Mirror"""

    bl_idname = 'PovrayMirrorNode'
    bl_label = 'Mirror'
    bl_icon = 'SHADING_TEXTURE'

    def init(self, context):

        color = self.inputs.new('PovraySocketColor', "Color")
        color.default_value = (1, 1, 1)
        metallic = self.inputs.new('PovraySocketFloat_0_1', "Metallic")
        metallic.default_value = 1.0
        exponent = self.inputs.new('PovraySocketFloat_0_1', "Exponent")
        exponent.default_value = 1.0
        self.inputs.new('PovraySocketFloat_0_1', "Falloff")
        self.inputs.new('NodeSocketBool', "Fresnel")
        self.inputs.new('NodeSocketBool', "Conserve energy")
        self.outputs.new('NodeSocketVector', "Mirror")

    def draw_label(self):
        return "Mirror"


class PovrayAmbientNode(Node, ObjectNodeTree):
    """Ambient"""

    bl_idname = 'PovrayAmbientNode'
    bl_label = 'Ambient'
    bl_icon = 'SHADING_SOLID'

    def init(self, context):

        self.inputs.new('PovraySocketColor', "Ambient")

        self.outputs.new('NodeSocketVector', "Ambient")

    def draw_label(self):
        return "Ambient"


class PovrayIridescenceNode(Node, ObjectNodeTree):
    """Iridescence"""

    bl_idname = 'PovrayIridescenceNode'
    bl_label = 'Iridescence'
    bl_icon = 'MESH_UVSPHERE'

    def init(self, context):

        amount = self.inputs.new('NodeSocketFloat', "Amount")
        amount.default_value = 0.25
        thickness = self.inputs.new('NodeSocketFloat', "Thickness")
        thickness.default_value = 1
        self.inputs.new('NodeSocketFloat', "Turbulence")

        self.outputs.new('NodeSocketVector', "Iridescence")

    def draw_label(self):
        return "Iridescence"


class PovraySubsurfaceNode(Node, ObjectNodeTree):
    """Subsurface"""

    bl_idname = 'PovraySubsurfaceNode'
    bl_label = 'Subsurface'
    bl_icon = 'MESH_UVSPHERE'

    def init(self, context):

        translucency = self.inputs.new('NodeSocketColor', "Translucency")
        translucency.default_value = (0, 0, 0, 1)
        energy = self.inputs.new('PovraySocketInt_0_256', "Energy")
        energy.default_value = 20
        self.outputs.new('NodeSocketVector', "Translucency")

    def draw_buttons(self, context, layout):
        scene = context.scene
        layout.prop(scene.pov, "sslt_enable", text="SSLT")

    def draw_buttons_ext(self, context, layout):
        scene = context.scene
        layout.prop(scene.pov, "sslt_enable", text="SSLT")

    def draw_label(self):
        return "Subsurface"


# ---------------------------------------------------------------- #


class PovrayMappingNode(Node, ObjectNodeTree):
    """Mapping"""

    bl_idname = 'PovrayMappingNode'
    bl_label = 'Mapping'
    bl_icon = 'NODE_TEXTURE'

    warp_type: EnumProperty(
        name="Warp Types",
        description="Select the type of warp",
        items=(
            ('cubic', "Cubic", ""),
            ('cylindrical', "Cylindrical", ""),
            ('planar', "Planar", ""),
            ('spherical', "Spherical", ""),
            ('toroidal', "Toroidal", ""),
            ('uv_mapping', "UV", ""),
            ('NONE', "None", "No indentation"),
        ),
        default='NONE',
    )

    warp_orientation: EnumProperty(
        name="Warp Orientation",
        description="Select the orientation of warp",
        items=(('x', "X", ""), ('y', "Y", ""), ('z', "Z", "")),
        default='y',
    )

    warp_dist_exp: FloatProperty(
        name="Distance exponent", description="Distance exponent", min=0.0, max=100.0, default=1.0
    )

    warp_tor_major_radius: FloatProperty(
        name="Major radius",
        description="Torus is distance from major radius",
        min=0.0,
        max=5.0,
        default=1.0,
    )

    def init(self, context):
        self.outputs.new('NodeSocketVector', "Mapping")

    def draw_buttons(self, context, layout):

        column = layout.column()
        column.prop(self, "warp_type", text="Warp type")
        if self.warp_type in {'toroidal', 'spherical', 'cylindrical', 'planar'}:
            column.prop(self, "warp_orientation", text="Orientation")
            column.prop(self, "warp_dist_exp", text="Exponent")
        if self.warp_type == 'toroidal':
            column.prop(self, "warp_tor_major_radius", text="Major R")

    def draw_buttons_ext(self, context, layout):

        column = layout.column()
        column.prop(self, "warp_type", text="Warp type")
        if self.warp_type in {'toroidal', 'spherical', 'cylindrical', 'planar'}:
            column.prop(self, "warp_orientation", text="Orientation")
            column.prop(self, "warp_dist_exp", text="Exponent")
        if self.warp_type == 'toroidal':
            column.prop(self, "warp_tor_major_radius", text="Major R")

    def draw_label(self):
        return "Mapping"


class PovrayMultiplyNode(Node, ObjectNodeTree):
    """Multiply"""

    bl_idname = 'PovrayMultiplyNode'
    bl_label = 'Multiply'
    bl_icon = 'SHADING_SOLID'

    amount_x: FloatProperty(
        name="X", description="Number of repeats", min=1.0, max=10000.0, default=1.0
    )

    amount_y: FloatProperty(
        name="Y", description="Number of repeats", min=1.0, max=10000.0, default=1.0
    )

    amount_z: FloatProperty(
        name="Z", description="Number of repeats", min=1.0, max=10000.0, default=1.0
    )

    def init(self, context):
        self.outputs.new('NodeSocketVector', "Amount")

    def draw_buttons(self, context, layout):

        column = layout.column()
        column.label(text="Amount")
        row = column.row(align=True)
        row.prop(self, "amount_x")
        row.prop(self, "amount_y")
        row.prop(self, "amount_z")

    def draw_buttons_ext(self, context, layout):

        column = layout.column()
        column.label(text="Amount")
        row = column.row(align=True)
        row.prop(self, "amount_x")
        row.prop(self, "amount_y")
        row.prop(self, "amount_z")

    def draw_label(self):
        return "Multiply"


class PovrayTransformNode(Node, ObjectNodeTree):
    """Transform"""

    bl_idname = 'PovrayTransformNode'
    bl_label = 'Transform'
    bl_icon = 'NODE_TEXTURE'

    def init(self, context):

        self.inputs.new('PovraySocketFloatUnlimited', "Translate x")
        self.inputs.new('PovraySocketFloatUnlimited', "Translate y")
        self.inputs.new('PovraySocketFloatUnlimited', "Translate z")
        self.inputs.new('PovraySocketFloatUnlimited', "Rotate x")
        self.inputs.new('PovraySocketFloatUnlimited', "Rotate y")
        self.inputs.new('PovraySocketFloatUnlimited', "Rotate z")
        sX = self.inputs.new('PovraySocketFloatUnlimited', "Scale x")
        sX.default_value = 1.0
        sY = self.inputs.new('PovraySocketFloatUnlimited', "Scale y")
        sY.default_value = 1.0
        sZ = self.inputs.new('PovraySocketFloatUnlimited', "Scale z")
        sZ.default_value = 1.0

        self.outputs.new('NodeSocketVector', "Transform")

    def draw_label(self):
        return "Transform"


class PovrayValueNode(Node, ObjectNodeTree):
    """Value"""

    bl_idname = 'PovrayValueNode'
    bl_label = 'Value'
    bl_icon = 'SHADING_SOLID'

    def init(self, context):

        self.outputs.new('PovraySocketUniversal', "Value")

    def draw_label(self):
        return "Value"


class PovrayModifierNode(Node, ObjectNodeTree):
    """Modifier"""

    bl_idname = 'PovrayModifierNode'
    bl_label = 'Modifier'
    bl_icon = 'NODE_TEXTURE'

    def init(self, context):

        turb_x = self.inputs.new('PovraySocketFloat_0_10', "Turb X")
        turb_x.default_value = 0.1
        turb_y = self.inputs.new('PovraySocketFloat_0_10', "Turb Y")
        turb_y.default_value = 0.1
        turb_z = self.inputs.new('PovraySocketFloat_0_10', "Turb Z")
        turb_z.default_value = 0.1
        octaves = self.inputs.new('PovraySocketInt_1_9', "Octaves")
        octaves.default_value = 1
        lambat = self.inputs.new('PovraySocketFloat_0_10', "Lambda")
        lambat.default_value = 2.0
        omega = self.inputs.new('PovraySocketFloat_0_10', "Omega")
        omega.default_value = 0.5
        freq = self.inputs.new('PovraySocketFloat_0_10', "Frequency")
        freq.default_value = 2.0
        self.inputs.new('PovraySocketFloat_0_10', "Phase")

        self.outputs.new('NodeSocketVector', "Modifier")

    def draw_label(self):
        return "Modifier"


class PovrayPigmentNode(Node, ObjectNodeTree):
    """Pigment"""

    bl_idname = 'PovrayPigmentNode'
    bl_label = 'Color'
    bl_icon = 'SHADING_SOLID'

    def init(self, context):

        color = self.inputs.new('PovraySocketColor', "Color")
        color.default_value = (1, 1, 1)
        pov_filter = self.inputs.new('PovraySocketFloat_0_1', "Filter")
        transmit = self.inputs.new('PovraySocketFloat_0_1', "Transmit")
        self.outputs.new('NodeSocketColor', "Pigment")

    def draw_label(self):
        return "Color"


class PovrayColorImageNode(Node, ObjectNodeTree):
    """ColorImage"""

    bl_idname = 'PovrayColorImageNode'
    bl_label = 'Image map'

    map_type: bpy.props.EnumProperty(
        name="Map type",
        description="",
        items=(
            ('uv_mapping', "UV", ""),
            ('0', "Planar", "Default planar mapping"),
            ('1', "Spherical", "Spherical mapping"),
            ('2', "Cylindrical", "Cylindrical mapping"),
            ('5', "Torroidal", "Torus or donut shaped mapping"),
        ),
        default='0',
    )
    image: StringProperty(maxlen=1024)  # , subtype="FILE_PATH"
    interpolate: EnumProperty(
        name="Interpolate",
        description="Adding the interpolate keyword can smooth the jagged look of a bitmap",
        items=(
            ('2', "Bilinear", "Gives bilinear interpolation"),
            ('4', "Normalized", "Gives normalized distance"),
        ),
        default='2',
    )
    premultiplied: BoolProperty(default=False)
    once: BoolProperty(description="Not to repeat", default=False)

    def init(self, context):

        gamma = self.inputs.new('PovraySocketFloat_000001_10', "Gamma")
        gamma.default_value = 2.0
        transmit = self.inputs.new('PovraySocketFloat_0_1', "Transmit")
        pov_filter = self.inputs.new('PovraySocketFloat_0_1', "Filter")
        mapping = self.inputs.new('NodeSocketVector', "Mapping")
        mapping.hide_value = True
        transform = self.inputs.new('NodeSocketVector', "Transform")
        transform.hide_value = True
        modifier = self.inputs.new('NodeSocketVector', "Modifier")
        modifier.hide_value = True

        self.outputs.new('NodeSocketColor', "Pigment")

    def draw_buttons(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        row = column.row()
        row.prop(self, "premultiplied", text="Premul")
        row.prop(self, "once", text="Once")

    def draw_buttons_ext(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        row = column.row()
        row.prop(self, "premultiplied", text="Premul")
        row.prop(self, "once", text="Once")

    def draw_label(self):
        return "Image map"


class PovrayBumpMapNode(Node, ObjectNodeTree):
    """BumpMap"""

    bl_idname = 'PovrayBumpMapNode'
    bl_label = 'Bump map'
    bl_icon = 'TEXTURE'

    map_type: bpy.props.EnumProperty(
        name="Map type",
        description="",
        items=(
            ('uv_mapping', "UV", ""),
            ('0', "Planar", "Default planar mapping"),
            ('1', "Spherical", "Spherical mapping"),
            ('2', "Cylindrical", "Cylindrical mapping"),
            ('5', "Torroidal", "Torus or donut shaped mapping"),
        ),
        default='0',
    )
    image: StringProperty(maxlen=1024)  # , subtype="FILE_PATH"
    interpolate: EnumProperty(
        name="Interpolate",
        description="Adding the interpolate keyword can smooth the jagged look of a bitmap",
        items=(
            ('2', "Bilinear", "Gives bilinear interpolation"),
            ('4', "Normalized", "Gives normalized distance"),
        ),
        default='2',
    )
    once: BoolProperty(description="Not to repeat", default=False)

    def init(self, context):

        self.inputs.new('PovraySocketFloat_0_10', "Normal")
        mapping = self.inputs.new('NodeSocketVector', "Mapping")
        mapping.hide_value = True
        transform = self.inputs.new('NodeSocketVector', "Transform")
        transform.hide_value = True
        modifier = self.inputs.new('NodeSocketVector', "Modifier")
        modifier.hide_value = True

        normal = self.outputs.new('NodeSocketFloat', "Normal")
        normal.hide_value = True

    def draw_buttons(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        column.prop(self, "once", text="Once")

    def draw_buttons_ext(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        column.prop(self, "once", text="Once")

    def draw_label(self):
        return "Bump Map"


class PovrayImagePatternNode(Node, ObjectNodeTree):
    """ImagePattern"""

    bl_idname = 'PovrayImagePatternNode'
    bl_label = 'Image pattern'
    bl_icon = 'NODE_TEXTURE'

    map_type: bpy.props.EnumProperty(
        name="Map type",
        description="",
        items=(
            ('uv_mapping', "UV", ""),
            ('0', "Planar", "Default planar mapping"),
            ('1', "Spherical", "Spherical mapping"),
            ('2', "Cylindrical", "Cylindrical mapping"),
            ('5', "Torroidal", "Torus or donut shaped mapping"),
        ),
        default='0',
    )
    image: StringProperty(maxlen=1024)  # , subtype="FILE_PATH"
    interpolate: EnumProperty(
        name="Interpolate",
        description="Adding the interpolate keyword can smooth the jagged look of a bitmap",
        items=(
            ('2', "Bilinear", "Gives bilinear interpolation"),
            ('4', "Normalized", "Gives normalized distance"),
        ),
        default='2',
    )
    premultiplied: BoolProperty(default=False)
    once: BoolProperty(description="Not to repeat", default=False)
    use_alpha: BoolProperty(default=True)

    def init(self, context):

        gamma = self.inputs.new('PovraySocketFloat_000001_10', "Gamma")
        gamma.default_value = 2.0

        self.outputs.new('PovraySocketPattern', "Pattern")

    def draw_buttons(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        row = column.row()
        row.prop(self, "premultiplied", text="Premul")
        row.prop(self, "once", text="Once")
        column.prop(self, "use_alpha", text="Use alpha")

    def draw_buttons_ext(self, context, layout):

        column = layout.column()
        im = None
        for image in bpy.data.images:
            if image.name == self.image:
                im = image
        split = column.split(factor=0.8, align=True)
        split.prop_search(self, "image", context.blend_data, "images", text="")
        split.operator("pov.imageopen", text="", icon="FILEBROWSER")
        if im is not None:
            column.prop(im, "source", text="")
        column.prop(self, "map_type", text="")
        column.prop(self, "interpolate", text="")
        row = column.row()
        row.prop(self, "premultiplied", text="Premul")
        row.prop(self, "once", text="Once")

    def draw_label(self):
        return "Image pattern"


class ShaderPatternNode(Node, ObjectNodeTree):
    """Pattern"""

    bl_idname = 'ShaderPatternNode'
    bl_label = 'Other patterns'

    pattern: EnumProperty(
        name="Pattern",
        description="Agate, Crackle, Gradient, Pavement, Spiral, Tiling",
        items=(
            ('agate', "Agate", ""),
            ('crackle', "Crackle", ""),
            ('gradient', "Gradient", ""),
            ('pavement', "Pavement", ""),
            ('spiral1', "Spiral 1", ""),
            ('spiral2', "Spiral 2", ""),
            ('tiling', "Tiling", ""),
        ),
        default='agate',
    )

    agate_turb: FloatProperty(
        name="Agate turb", description="Agate turbulence", min=0.0, max=100.0, default=0.5
    )

    crackle_form_x: FloatProperty(
        name="X", description="Form vector X", min=-150.0, max=150.0, default=-1
    )

    crackle_form_y: FloatProperty(
        name="Y", description="Form vector Y", min=-150.0, max=150.0, default=1
    )

    crackle_form_z: FloatProperty(
        name="Z", description="Form vector Z", min=-150.0, max=150.0, default=0
    )

    crackle_metric: FloatProperty(
        name="Metric", description="Crackle metric", min=0.0, max=150.0, default=1
    )

    crackle_solid: BoolProperty(name="Solid", description="Crackle solid", default=False)

    spiral_arms: FloatProperty(name="Number", description="", min=0.0, max=256.0, default=2.0)

    tiling_number: IntProperty(name="Number", description="", min=1, max=27, default=1)

    gradient_orient: EnumProperty(
        name="Orient",
        description="",
        items=(('x', "X", ""), ('y', "Y", ""), ('z', "Z", "")),
        default='x',
    )

    def init(self, context):

        pat = self.outputs.new('PovraySocketPattern', "Pattern")

    def draw_buttons(self, context, layout):

        layout.prop(self, "pattern", text="")
        if self.pattern == 'agate':
            layout.prop(self, "agate_turb")
        if self.pattern == 'crackle':
            layout.prop(self, "crackle_metric")
            layout.prop(self, "crackle_solid")
            layout.label(text="Form:")
            layout.prop(self, "crackle_form_x")
            layout.prop(self, "crackle_form_y")
            layout.prop(self, "crackle_form_z")
        if self.pattern in {"spiral1", "spiral2"}:
            layout.prop(self, "spiral_arms")
        if self.pattern in {'tiling'}:
            layout.prop(self, "tiling_number")
        if self.pattern in {'gradient'}:
            layout.prop(self, "gradient_orient")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Other patterns"


class ShaderTextureMapNode(Node, ObjectNodeTree):
    """Texture Map"""

    bl_idname = 'ShaderTextureMapNode'
    bl_label = 'Texture map'

    brick_size_x: FloatProperty(name="X", description="", min=0.0000, max=1.0000, default=0.2500)

    brick_size_y: FloatProperty(name="Y", description="", min=0.0000, max=1.0000, default=0.0525)

    brick_size_z: FloatProperty(name="Z", description="", min=0.0000, max=1.0000, default=0.1250)

    brick_mortar: FloatProperty(
        name="Mortar", description="Mortar", min=0.000, max=1.500, default=0.01
    )

    def init(self, context):
        mat = bpy.context.object.active_material
        self.inputs.new('PovraySocketPattern', "")
        color = self.inputs.new('NodeSocketColor', "Color ramp")
        color.hide_value = True
        for i in range(0, 4):
            transform = self.inputs.new('PovraySocketTransform', "Transform")
            transform.hide_value = True
        number = mat.pov.inputs_number
        for i in range(number):
            self.inputs.new('PovraySocketTexture', "%s" % i)

        self.outputs.new('PovraySocketTexture', "Texture")

    def draw_buttons(self, context, layout):

        if self.inputs[0].default_value == 'brick':
            layout.prop(self, "brick_mortar")
            layout.label(text="Brick size:")
            layout.prop(self, "brick_size_x")
            layout.prop(self, "brick_size_y")
            layout.prop(self, "brick_size_z")

    def draw_buttons_ext(self, context, layout):

        if self.inputs[0].default_value == 'brick':
            layout.prop(self, "brick_mortar")
            layout.label(text="Brick size:")
            layout.prop(self, "brick_size_x")
            layout.prop(self, "brick_size_y")
            layout.prop(self, "brick_size_z")

    def draw_label(self):
        return "Texture map"


class ShaderNormalMapNode(Node, ObjectNodeTree):
    """Normal Map"""

    bl_idname = 'ShaderNormalMapNode'
    bl_label = 'Normal map'

    brick_size_x: FloatProperty(name="X", description="", min=0.0000, max=1.0000, default=0.2500)

    brick_size_y: FloatProperty(name="Y", description="", min=0.0000, max=1.0000, default=0.0525)

    brick_size_z: FloatProperty(name="Z", description="", min=0.0000, max=1.0000, default=0.1250)

    brick_mortar: FloatProperty(
        name="Mortar", description="Mortar", min=0.000, max=1.500, default=0.01
    )

    def init(self, context):
        self.inputs.new('PovraySocketPattern', "")
        normal = self.inputs.new('PovraySocketFloat_10', "Normal")
        slope = self.inputs.new('PovraySocketMap', "Slope map")
        for i in range(0, 4):
            transform = self.inputs.new('PovraySocketTransform', "Transform")
            transform.hide_value = True
        self.outputs.new('PovraySocketNormal', "Normal")

    def draw_buttons(self, context, layout):
        # for i, inp in enumerate(self.inputs):

        if self.inputs[0].default_value == 'brick':
            layout.prop(self, "brick_mortar")
            layout.label(text="Brick size:")
            layout.prop(self, "brick_size_x")
            layout.prop(self, "brick_size_y")
            layout.prop(self, "brick_size_z")

    def draw_buttons_ext(self, context, layout):

        if self.inputs[0].default_value == 'brick':
            layout.prop(self, "brick_mortar")
            layout.label(text="Brick size:")
            layout.prop(self, "brick_size_x")
            layout.prop(self, "brick_size_y")
            layout.prop(self, "brick_size_z")

    def draw_label(self):
        return "Normal map"


class ShaderNormalMapEntryNode(Node, ObjectNodeTree):
    """Normal Map Entry"""

    bl_idname = 'ShaderNormalMapEntryNode'
    bl_label = 'Normal map entry'

    def init(self, context):
        self.inputs.new('PovraySocketFloat_0_1', "Stop")
        self.inputs.new('PovraySocketFloat_0_1', "Gray")

    def draw_label(self):
        return "Normal map entry"


class IsoPropsNode(Node, CompositorNodeTree):
    """ISO Props"""

    bl_idname = 'IsoPropsNode'
    bl_label = 'Iso'
    node_label: StringProperty(maxlen=1024)

    def init(self, context):
        ob = bpy.context.object
        self.node_label = ob.name
        text_name = ob.pov.function_text
        if text_name:
            text = bpy.data.texts[text_name]
            for line in text.lines:
                split = line.body.split()
                if split[0] == "#declare":
                    socket = self.inputs.new('NodeSocketFloat', "%s" % split[1])
                    value = split[3].split(";")
                    value = value[0]
                    socket.default_value = float(value)

    def draw_label(self):
        return self.node_label


class PovrayFogNode(Node, CompositorNodeTree):
    """Fog settings"""

    bl_idname = 'PovrayFogNode'
    bl_label = 'Fog'

    def init(self, context):
        color = self.inputs.new('NodeSocketColor', "Color")
        color.default_value = (0.7, 0.7, 0.7, 0.25)
        self.inputs.new('PovraySocketFloat_0_1', "Filter")
        distance = self.inputs.new('NodeSocketInt', "Distance")
        distance.default_value = 150
        self.inputs.new('NodeSocketBool', "Ground")
        fog_offset = self.inputs.new('NodeSocketFloat', "Offset")
        fog_alt = self.inputs.new('NodeSocketFloat', "Altitude")
        turb = self.inputs.new('NodeSocketVector', "Turbulence")
        turb_depth = self.inputs.new('PovraySocketFloat_0_10', "Depth")
        turb_depth.default_value = 0.5
        octaves = self.inputs.new('PovraySocketInt_1_9', "Octaves")
        octaves.default_value = 5
        lambdat = self.inputs.new('PovraySocketFloat_0_10', "Lambda")
        lambdat.default_value = 1.25
        omega = self.inputs.new('PovraySocketFloat_0_10', "Omega")
        omega.default_value = 0.35
        translate = self.inputs.new('NodeSocketVector', "Translate")
        rotate = self.inputs.new('NodeSocketVector', "Rotate")
        scale = self.inputs.new('NodeSocketVector', "Scale")
        scale.default_value = (1, 1, 1)

    def draw_label(self):
        return "Fog"


class PovraySlopeNode(Node, TextureNodeTree):
    """Output"""

    bl_idname = 'PovraySlopeNode'
    bl_label = 'Slope Map'

    def init(self, context):
        self.use_custom_color = True
        self.color = (0, 0.2, 0)
        slope = self.inputs.new('PovraySocketSlope', "0")
        slope = self.inputs.new('PovraySocketSlope', "1")
        slopemap = self.outputs.new('PovraySocketMap', "Slope map")
        output.hide_value = True

    def draw_buttons(self, context, layout):

        layout.operator("pov.nodeinputadd")
        row = layout.row()
        row.label(text='Value')
        row.label(text='Height')
        row.label(text='Slope')

    def draw_buttons_ext(self, context, layout):

        layout.operator("pov.nodeinputadd")
        row = layout.row()
        row.label(text='Value')
        row.label(text='Height')
        row.label(text='Slope')

    def draw_label(self):
        return "Slope Map"


# -------- Texture nodes # ---------------------------------------------------------------- #
class TextureOutputNode(Node, TextureNodeTree):
    """Output"""

    bl_idname = 'TextureOutputNode'
    bl_label = 'Color Map'

    def init(self, context):
        tex = bpy.context.object.active_material.active_texture
        num_sockets = int(tex.pov.density_lines / 32)
        for i in range(num_sockets):
            color = self.inputs.new('NodeSocketColor', "%s" % i)
            color.hide_value = True

    def draw_buttons(self, context, layout):

        layout.label(text="Color Ramps:")

    def draw_label(self):
        return "Color Map"


# ------------------------------------------------------------------------------ #
# --------------------------------- Operators ---------------------------------- #
# ------------------------------------------------------------------------------ #


class NODE_OT_iso_add(Operator):
    bl_idname = "pov.nodeisoadd"
    bl_label = "Create iso props"

    def execute(self, context):
        ob = bpy.context.object
        if not bpy.context.scene.use_nodes:
            bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        for node in tree.nodes:
            if node.bl_idname == "IsoPropsNode" and node.label == ob.name:
                tree.nodes.remove(node)
        isonode = tree.nodes.new('IsoPropsNode')
        isonode.location = (0, 0)
        isonode.label = ob.name
        return {'FINISHED'}


class NODE_OT_map_create(Operator):
    bl_idname = "node.map_create"
    bl_label = "Create map"

    def execute(self, context):
        x = y = 0
        space = context.space_data
        tree = space.edit_tree
        for node in tree.nodes:
            if node.select:
                x, y = node.location
            node.select = False
        tmap = tree.nodes.new('ShaderTextureMapNode')
        tmap.location = (x - 200, y)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        mat = context.object.active_material
        layout.prop(mat.pov, "inputs_number")


class NODE_OT_povray_node_texture_map_add(Operator):
    bl_idname = "pov.nodetexmapadd"
    bl_label = "Texture map"

    def execute(self, context):
        tree = bpy.context.object.active_material.node_tree
        tmap = tree.nodes.active
        bpy.context.object.active_material.node_tree.nodes.active = tmap
        el = tmap.color_ramp.elements.new(0.5)
        for el in tmap.color_ramp.elements:
            el.color = (0, 0, 0, 1)
        for inp in tmap.inputs:
            tmap.inputs.remove(inp)
        for outp in tmap.outputs:
            tmap.outputs.remove(outp)
        pattern = tmap.inputs.new('NodeSocketVector', "Pattern")
        pattern.hide_value = True
        for i in range(0, 3):
            tmap.inputs.new('NodeSocketColor', "Shader")
        tmap.outputs.new('NodeSocketShader', "BSDF")
        tmap.label = "Texture Map"
        return {'FINISHED'}


class NODE_OT_povray_node_output_add(Operator):
    bl_idname = "pov.nodeoutputadd"
    bl_label = "Output"

    def execute(self, context):
        tree = bpy.context.object.active_material.node_tree
        tmap = tree.nodes.new('ShaderNodeOutputMaterial')
        bpy.context.object.active_material.node_tree.nodes.active = tmap
        for inp in tmap.inputs:
            tmap.inputs.remove(inp)
        tmap.inputs.new('NodeSocketShader', "Surface")
        tmap.label = "Output"
        return {'FINISHED'}


class NODE_OT_povray_node_layered_add(Operator):
    bl_idname = "pov.nodelayeredadd"
    bl_label = "Layered material"

    def execute(self, context):
        tree = bpy.context.object.active_material.node_tree
        tmap = tree.nodes.new('ShaderNodeAddShader')
        bpy.context.object.active_material.node_tree.nodes.active = tmap
        tmap.label = "Layered material"
        return {'FINISHED'}


class NODE_OT_povray_input_add(Operator):
    bl_idname = "pov.nodeinputadd"
    bl_label = "Add entry"

    def execute(self, context):
        node = bpy.context.object.active_material.node_tree.nodes.active
        if node.type in {'VALTORGB'}:
            number = 1
            for inp in node.inputs:
                if inp.type == 'SHADER':
                    number += 1
            node.inputs.new('NodeSocketShader', "%s" % number)
            els = node.color_ramp.elements
            pos1 = els[len(els) - 1].position
            pos2 = els[len(els) - 2].position
            pos = (pos1 - pos2) / 2 + pos2
            el = els.new(pos)

        if node.bl_idname == 'PovraySlopeNode':
            number = len(node.inputs)
            node.inputs.new('PovraySocketSlope', "%s" % number)

        return {'FINISHED'}


class NODE_OT_povray_input_remove(Operator):
    bl_idname = "pov.nodeinputremove"
    bl_label = "Remove input"

    def execute(self, context):
        node = bpy.context.object.active_material.node_tree.nodes.active
        if node.type in {'VALTORGB', 'ADD_SHADER'}:
            number = len(node.inputs) - 1
            if number > 5:
                inp = node.inputs[number]
                node.inputs.remove(inp)
                if node.type in {'VALTORGB'}:
                    els = node.color_ramp.elements
                    number = len(els) - 2
                    el = els[number]
                    els.remove(el)
        return {'FINISHED'}


class NODE_OT_povray_image_open(Operator):
    bl_idname = "pov.imageopen"
    bl_label = "Open"

    filepath: StringProperty(
        name="File Path", description="Open image", maxlen=1024, subtype='FILE_PATH'
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        im = bpy.data.images.load(self.filepath)
        node = context.object.active_material.node_tree.nodes.active
        node.image = im.name
        return {'FINISHED'}


# class TEXTURE_OT_povray_open_image(Operator):
# bl_idname = "pov.openimage"
# bl_label = "Open Image"

# filepath = StringProperty(
# name="File Path",
# description="Open image",
# maxlen=1024,
# subtype='FILE_PATH',
# )

# def invoke(self, context, event):
# context.window_manager.fileselect_add(self)
# return {'RUNNING_MODAL'}

# def execute(self, context):
# im=bpy.data.images.load(self.filepath)
# tex = context.texture
# tex.pov.image = im.name
# view_layer = context.view_layer
# view_layer.update()
# return {'FINISHED'}


class PovrayPatternNode(Operator):
    bl_idname = "pov.patternnode"
    bl_label = "Pattern"

    add = True

    def execute(self, context):
        space = context.space_data
        tree = space.edit_tree
        for node in tree.nodes:
            node.select = False
        if self.add:
            tmap = tree.nodes.new('ShaderNodeValToRGB')
            tmap.label = "Pattern"
            for inp in tmap.inputs:
                tmap.inputs.remove(inp)
            for outp in tmap.outputs:
                tmap.outputs.remove(outp)
            pattern = tmap.inputs.new('PovraySocketPattern', "Pattern")
            pattern.hide_value = True
            mapping = tmap.inputs.new('NodeSocketVector', "Mapping")
            mapping.hide_value = True
            transform = tmap.inputs.new('NodeSocketVector', "Transform")
            transform.hide_value = True
            modifier = tmap.inputs.new('NodeSocketVector', "Modifier")
            modifier.hide_value = True
            for i in range(0, 2):
                tmap.inputs.new('NodeSocketShader', "%s" % (i + 1))
            tmap.outputs.new('NodeSocketShader', "Material")
            tmap.outputs.new('NodeSocketColor', "Color")
            tree.nodes.active = tmap
            self.add = False
        aNode = tree.nodes.active
        aNode.select = True
        v2d = context.region.view2d
        x, y = v2d.region_to_view(self.x, self.y)
        aNode.location = (x, y)

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            self.x = event.mouse_region_x
            self.y = event.mouse_region_y
            self.execute(context)
            return {'RUNNING_MODAL'}
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        elif event.type in ('RIGHTMOUSE', 'ESC'):
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class UpdatePreviewMaterial(Operator):
    """Operator update preview material"""

    bl_idname = "node.updatepreview"
    bl_label = "Update preview"

    def execute(self, context):
        scene = context.view_layer
        ob = context.object
        for obj in scene.objects:
            if obj != ob:
                scene.objects.active = ob
                break
        scene.objects.active = ob

    def modal(self, context, event):
        if event.type == 'RIGHTMOUSE':
            self.execute(context)
            return {'FINISHED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class UpdatePreviewKey(Operator):
    """Operator update preview keymap"""

    bl_idname = "wm.updatepreviewkey"
    bl_label = "Activate RMB"

    @classmethod
    def poll(cls, context):
        conf = context.window_manager.keyconfigs.active
        mapstr = "Node Editor"
        map = conf.keymaps[mapstr]
        try:
            map.keymap_items["node.updatepreview"]
            return False
        except BaseException as e:
            print(e.__doc__)
            print('An exception occurred: {}'.format(e))
            return True

    def execute(self, context):
        conf = context.window_manager.keyconfigs.active
        mapstr = "Node Editor"
        map = conf.keymaps[mapstr]
        map.keymap_items.new("node.updatepreview", type='RIGHTMOUSE', value="PRESS")
        return {'FINISHED'}


classes = (
    PovraySocketUniversal,
    PovraySocketFloat_0_1,
    PovraySocketFloat_0_10,
    PovraySocketFloat_10,
    PovraySocketFloatPositive,
    PovraySocketFloat_000001_10,
    PovraySocketFloatUnlimited,
    PovraySocketInt_1_9,
    PovraySocketInt_0_256,
    PovraySocketPattern,
    PovraySocketColor,
    PovraySocketColorRGBFT,
    PovraySocketTexture,
    PovraySocketTransform,
    PovraySocketNormal,
    PovraySocketSlope,
    PovraySocketMap,
    # PovrayShaderNodeCategory, # XXX SOMETHING BROKEN from 2.8 ?
    # PovrayTextureNodeCategory, # XXX SOMETHING BROKEN from 2.8 ?
    # PovraySceneNodeCategory, # XXX SOMETHING BROKEN from 2.8 ?
    NODE_MT_POV_map_create,
    ObjectNodeTree,
    PovrayOutputNode,
    PovrayTextureNode,
    PovrayFinishNode,
    PovrayDiffuseNode,
    PovrayPhongNode,
    PovraySpecularNode,
    PovrayMirrorNode,
    PovrayAmbientNode,
    PovrayIridescenceNode,
    PovraySubsurfaceNode,
    PovrayMappingNode,
    PovrayMultiplyNode,
    PovrayTransformNode,
    PovrayValueNode,
    PovrayModifierNode,
    PovrayPigmentNode,
    PovrayColorImageNode,
    PovrayBumpMapNode,
    PovrayImagePatternNode,
    ShaderPatternNode,
    ShaderTextureMapNode,
    ShaderNormalMapNode,
    ShaderNormalMapEntryNode,
    IsoPropsNode,
    PovrayFogNode,
    PovraySlopeNode,
    TextureOutputNode,
    NODE_OT_iso_add,
    NODE_OT_map_create,
    NODE_OT_povray_node_texture_map_add,
    NODE_OT_povray_node_output_add,
    NODE_OT_povray_node_layered_add,
    NODE_OT_povray_input_add,
    NODE_OT_povray_input_remove,
    NODE_OT_povray_image_open,
    PovrayPatternNode,
    UpdatePreviewMaterial,
    UpdatePreviewKey,
)


def register():
    bpy.types.NODE_HT_header.append(menu_func_nodes)
    nodeitems_utils.register_node_categories("POVRAYNODES", node_categories)
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    nodeitems_utils.unregister_node_categories("POVRAYNODES")
    bpy.types.NODE_HT_header.remove(menu_func_nodes)
