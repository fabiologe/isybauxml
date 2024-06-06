import numpy as np
from glumpy import app, gloo, gl

# Vertex shader
vertex = """
attribute vec2 position;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Fragment shader
fragment = """
void main() {
    gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

# Create a window
window = app.Window(width=800, height=600, color=(0, 0, 0, 1))

# Define the vertices of the triangle
vertices = np.array([[0, 0], [1, 0], [0.5, 1]], dtype=np.float32)

# Create VertexBuffer object
triangle = gloo.Program(vertex, fragment)
triangle['position'] = vertices

@window.event
def on_draw(dt):
    window.clear()
    triangle.draw(gl.GL_TRIANGLES)

# Run the application
app.run()
