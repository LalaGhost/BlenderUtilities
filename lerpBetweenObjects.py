import bpy
from bpy.types import (Operator,)
from bpy.props import (IntProperty, BoolProperty)
import textwrap


class OT_LerpBetweenObjects(Operator):
	bl_label = 'Lerp Between Objects'
	bl_idname = 'blender_utilities.lerp_between_objects'
	bl_description = textwrap.fill('Duplicates and lerps position & rotation of between 2 objects', 80)
	bl_options = {'REGISTER', 'UNDO'}


	inbetween_objects : IntProperty (
		name = "Inbetween Objects",
		description = "Amount of objects lerped between your selection",
		default = 2,
		min = 1,
		max = 1000,
	)
	rotation : BoolProperty (
		name = "Rotation",
		description = "Enable to rotate inbetween objects",
		default = True,
		)
	scale : BoolProperty (
		name = "Scale",
		description = "Enable to scale inbetween objects",
		default = True,
		)
	selectOnlyDuplicates : BoolProperty (
		name = "Select Only Duplicates",
		description = "Enable to only select duplicates",
		default = True,
		)


	def execute(self, context):
		selection = bpy.context.selected_objects
		initialActiveObject = bpy.context.active_object
		inbetweenObjects = []

		if len(selection) > 2:
			self.report({'ERROR'}, 'You are not allowed to have more than 2 objects selected.')
			return{'FINISHED'}
		elif len(selection) < 2:
			self.report({'ERROR'}, 'You need to have exactly 2 objects selected.')
			return{'FINISHED'}

		firstObjectTranslation = selection[0].location
		firstObjectRotation = selection[0].rotation_euler
		firstObjectScale = selection[0].scale

		secondObjectTranslation = selection[1].location
		secondObjectRotation = selection[1].rotation_euler
		secondObjectScale = selection[1].scale

		bpy.ops.object.select_all(action = 'DESELECT')
		bpy.context.view_layer.objects.active = bpy.data.objects[selection[0].name]
		bpy.data.objects[selection[0].name].select_set(True)

		for i in range(self.inbetween_objects):
			bpy.ops.object.duplicate(linked = False)
			duplicate = bpy.context.view_layer.objects.active
			inbetweenObjects.append(duplicate)

			interpolant = (i + 1) / (self.inbetween_objects + 1)
			duplicate.location.x = firstObjectTranslation[0] * (1 - interpolant) + secondObjectTranslation[0] * (interpolant)
			duplicate.location.y = firstObjectTranslation[1] * (1 - interpolant) + secondObjectTranslation[1] * (interpolant)
			duplicate.location.z = firstObjectTranslation[2] * (1 - interpolant) + secondObjectTranslation[2] * (interpolant)

			if self.rotation:
				duplicate.rotation_euler.x = firstObjectRotation[0] * (1 - interpolant) + secondObjectRotation[0] * (interpolant)
				duplicate.rotation_euler.y = firstObjectRotation[1] * (1 - interpolant) + secondObjectRotation[1] * (interpolant)
				duplicate.rotation_euler.z = firstObjectRotation[2] * (1 - interpolant) + secondObjectRotation[2] * (interpolant)

			if self.scale:
				duplicate.scale.x = firstObjectScale[0] * (1 - interpolant) + secondObjectScale[0] * (interpolant)
				duplicate.scale.y = firstObjectScale[1] * (1 - interpolant) + secondObjectScale[1] * (interpolant)
				duplicate.scale.z = firstObjectScale[2] * (1 - interpolant) + secondObjectScale[2] * (interpolant)

		# Restore selection and active object
		bpy.ops.object.select_all(action = 'DESELECT')
		if not self.selectOnlyDuplicates:
			for obj in selection:
				bpy.data.objects[obj.name].select_set(True)

		for obj in inbetweenObjects:
			bpy.data.objects[obj.name].select_set(True)

		if not self.selectOnlyDuplicates:
			bpy.context.view_layer.objects.active = bpy.data.objects[initialActiveObject.name]
		return{'FINISHED'}


def register():
	bpy.utils.register_class(OT_LerpBetweenObjects)


def unregister():
	bpy.utils.unregister_class(OT_LerpBetweenObjects)


if __name__ == '__main__':
	register()
	bpy.ops.blender_utilities.lerp_between_objects('INVOKE_DEFAULT')