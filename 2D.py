import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.transforms import Trackball, Position

    
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

vertex = """
uniform vec4 u_color;
attribute vec3 position;
attribute vec4 color;
varying vec4 v_color;
void main()
{
    v_color = u_color * color;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

@window.event
def on_draw(dt):
    window.clear()

    # Draw green surface
    program['u_color'] = 0, 1, 0, 1
    program.bind(green_vertex_buffer)
    program.draw(gl.GL_TRIANGLES, green_filled_buffer)
    program.draw(gl.GL_LINES, green_outline_buffer)

    # Draw blue surface
    program['u_color'] = 0, 0, 1, 1
    program.bind(blue_vertex_buffer)
    program.draw(gl.GL_TRIANGLES, blue_filled_buffer)
    program.draw(gl.GL_LINES, blue_outline_buffer)

# Example 2D surface data for green surface
green_vertices = np.array([[ 1, 1, 0], [-1, 1, 0], [-1, -1, 0], [ 1, -1, 0]], dtype=np.float32)
green_faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
green_colors = np.array([[0, 1, 0, 1]] * len(green_vertices), dtype=np.float32)
green_normals = np.array([[0, 0, 1]] * len(green_vertices), dtype=np.float32)
green_texcoords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)

# Example 2D surface data for blue surface
blue_vertices = np.array([[ 7, 0.5, 8], [-3, 0.5, 5], [-0.5, -0.5, 1], [ 0.5, -0.5, 0]], dtype=np.float32)
blue_faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
blue_colors = np.array([[0, 0, 1, 1]] * len(blue_vertices), dtype=np.float32)
blue_normals = np.array([[0, 0, 1]] * len(blue_vertices), dtype=np.float32)
blue_texcoords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=np.float32)

# Create buffers for the green surface
green_vertex_buffer, green_filled_buffer, green_outline_buffer = create_buffers(green_vertices, green_faces, green_colors, green_normals, green_texcoords)

# Create buffers for the blue surface
blue_vertex_buffer, blue_filled_buffer, blue_outline_buffer = create_buffers(blue_vertices, blue_faces, blue_colors, blue_normals, blue_texcoords)

# Create and set up program
program = gloo.Program(vertex, fragment)
program['transform'] = Trackball(Position("position"))
window.attach(program['transform'])

# OpenGL initialization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Run
app.run()
