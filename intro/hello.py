import sys

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from glmath import perspective
import numpy as np

vs_src = '''
attribute vec4 aPosition;
uniform mat4 uPMatrix;
void main() {
    gl_Position = uPMatrix * aPosition;
}'''

fs_src = '''
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}'''

class HelloGL:
    def initialiseGLUT(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(250, 250)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Hello GL")
        self.compileProgram()
        self.drawScene()
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyPressed)
        glutMainLoop()

    def __init__(self):
        self.initialiseGLUT()

    def makeVertexBuffer(self, vertices):
        array_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, array_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        return array_buffer

    def compileProgram(self):
        vertex_shader = shaders.compileShader(vs_src, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fs_src, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        shaders.glUseProgram(self.shader)

    def drawScene(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.attribute_position = glGetAttribLocation(self.shader, 'aPosition')
        self.uniform_perspective = glGetUniformLocation(self.shader, "uPMatrix")

        vertices = np.array([
                [-0.90, -0.90, -2.],
                [ 0.85, -0.90, -2.],
                [-0.90,  0.85, -2.],
                [ 0.90, -0.85, -2.],
                [ 0.90,  0.90, -2.],
                [-0.85,  0.90, -2.],
                ],dtype=np.float32)

        vertex_buffer = self.makeVertexBuffer(vertices)
        # bind vertex buffer to attribute_position
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glEnableVertexAttribArray(self.attribute_position)
        glVertexAttribPointer( self.attribute_position, 3, GL_FLOAT, GL_FALSE, 0, None)

        perspective_matrix = perspective(45., 1., 0.1, 100.)
        glUniformMatrix4fv(self.uniform_perspective, 1, GL_FALSE, perspective_matrix)


    def display(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 6)
        finally:
            glFlush ()

    def keyPressed(self, *args):
        if args[0] == '\033':
            sys.exit(0)


if __name__ == '__main__':
    HelloGL()
