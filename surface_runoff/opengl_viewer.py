import glfw 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluLookAt
from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
import numpy as np

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 4.0, 3.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    # Camera method for the WASD movement
    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity

        return np.array([eye_x, eye_y, eye_z])


def cursor_pos_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    x_offset = xpos - last_x
    y_offset = last_y - ypos  # reversed since y-coordinates range from bottom to top
    last_x = xpos
    last_y = ypos

    if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        camera.update(x_offset, y_offset, 0.0)


def scroll_callback(window, xoffset, yoffset):
    camera.update(0.0, 0.0, yoffset)

camera = Camera()
last_x = 800 / 2
last_y = 600 / 2
first_mouse = True

def visualize(triangles):
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Triangle Mesh", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        view_matrix = camera.view_matrix()
        gluLookAt(*view_matrix, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glBegin(GL_TRIANGLES)
        for triangle in triangles:
            glColor3f(1.0, 1.0, 1.0)  # Set triangle color
            for vertex in triangle.vertices:
                glVertex3f(vertex.x_value, vertex.y_value, vertex.z_value)
        glEnd()

        glfw.swap_buffers(window)

    glfw.terminate()
def main_text():
    
    # Example usage
    vertices = [
        Vertex(0, 0, 10),
        Vertex(1, 0, 15),
        Vertex(0, 1, 20),
        Vertex(1, 1, 5),
        Vertex(2, 0, 10),
        Vertex(2, 1, 5),
    ]

    Triangles = [
        Triangle(vertices=[vertices[0], vertices[1], vertices[2]], perme=0.1, slop=5.0),
        Triangle(vertices=[vertices[1], vertices[3], vertices[2]], perme=0.05, slop=10.0),
        Triangle(vertices=[vertices[1], vertices[4], vertices[3]], perme=0.1, slop=5.0),
        Triangle(vertices=[vertices[4], vertices[5], vertices[3]], perme=0.05, slop=10.0),
    ]

    visualize(Triangles)