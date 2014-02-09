import sys

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np

vs_src = '''
attribute vec4 vPosition;
void main() {
    gl_Position = vPosition;
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

        self.position_location = glGetAttribLocation(self.shader, 'vPosition')

        vertices = np.array([
                [-0.90, -0.90],
                [ 0.85, -0.90],
                [-0.90,  0.85],
                [ 0.90, -0.85],
                [ 0.90,  0.90],
                [-0.85,  0.90],
                ],dtype=np.float32)

        vertex_buffer = self.makeVertexBuffer(vertices)
        # bind vertex buffer to position_location
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glEnableVertexAttribArray(self.position_location)
        glVertexAttribPointer( self.position_location, 2, GL_FLOAT, GL_FALSE, 0, None)

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
