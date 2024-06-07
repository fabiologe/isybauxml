from surface_runoff.boundary import ModelHandler, Polygon

from surface_runoff.opengl_viewer import create_buffers
import numpy as np
from glumpy import app, gl, gloo
from glumpy.transforms import Trackball, Position


handler = ModelHandler()

# Load STL file
stl_file_path = 'surface_runoff/input/2024-06-07-22h50m23s-attachments/Auslauf_ASCII.stl'
handler.load_stl(stl_file_path)
stl_polygons = handler.get_polygons()
print("STL Polygons:")
for polygon in stl_polygons:
    print(polygon)


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
    
    for polygon in stl_polygons:
        vertices, faces, colors, normals, texcoords = polygon.to_buffer()
        vertex_buffer, filled_buffer, outline_buffer = create_buffers(vertices, faces, colors, normals, texcoords)
        
        program['u_color'] = colors[0]  # Set color from the polygon
        program.bind(vertex_buffer)
        program.draw(gl.GL_TRIANGLES, filled_buffer)
        program.draw(gl.GL_LINES, outline_buffer)







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