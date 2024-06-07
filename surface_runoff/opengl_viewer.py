import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.transforms import Trackball, Position
from surface_runoff.boundary import Polygon

    
def create_buffers(vertices, faces, colors, normals, texcoords):
    """ Generate buffers for vertices, faces, colors, normals, and texcoords """

    vtype = [('position', np.float32, 3),
             ('texcoord', np.float32, 2),
             ('normal',   np.float32, 3),
             ('color',    np.float32, 4)]
    itype = np.uint32

    # Create vertex buffer
    vertex_data = np.zeros(len(vertices), vtype)
    vertex_data['position'] = vertices
    vertex_data['normal'] = normals
    vertex_data['color'] = colors
    vertex_data['texcoord'] = texcoords

    # Create index buffers for filled and outlined shapes
    filled = np.resize(faces, len(faces) * 3)
    outline = np.resize(faces, len(faces) * 3)

    vertex_buffer = vertex_data.view(gloo.VertexBuffer)
    filled_buffer = filled.view(gloo.IndexBuffer)
    outline_buffer = outline.view(gloo.IndexBuffer)

    return vertex_buffer, filled_buffer, outline_buffer