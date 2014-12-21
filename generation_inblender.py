import bpy
from mathutils import *
from math import *
from bpy.props import *
import pickle
F=open(r'C:\Users\Administrator\Desktop\roadway_auto_generation\datafile2.pkl','rb')

e=pickle.load(F)
for i in list(e.keys()):
    for ii in list(e[i].keys()):
       me = bpy.data.meshes.new("PyramidMesh%s"%i)
       ob = bpy.data.objects.new("Pyramid%s"%i, me)
       bpy.context.scene.objects.link(ob)
       me.from_pydata(e[i][ii][2],[],e[i][ii][3])
       me.update(calc_edges=True)
