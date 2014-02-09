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
uniform mat4 uMVMatrix;
void main() {
    gl_Position = uPMatrix * uMVMatrix * aPosition;
}'''

fs_src = '''
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}'''

class HelloGL:
    def initialiseGLUT(self):
        '''
        Initialize the application and tell GLUT where/how to render the context.
        GLUT will create a window 250x250 and initialize the GL Context so that 
        we can call GL functions and interact with the context.
        '''
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(250, 250)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("Hello GL")
        # Now that the context is created we can initialize our open gl program
        self.compileProgram()
        self.drawScene()
        # Tells glut what to call to render the scene
        glutDisplayFunc(self.display)
        # We setup a keyboard handler so that we can interact with the program
        glutKeyboardFunc(self.keyPressed)
        # GLUT will call the display as much as it can in a loop
        # spawns a listener thread for certain loops like user input and rendering
        glutMainLoop()

    def __init__(self):
        self.initialiseGLUT()

    def makeVertexBuffer(self, vertices):
        '''
        Creates a VBO for the vertices specified and copies the vertices 
        into the buffer

        returns a GL_ARRAY_BUFFER
        '''
        array_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, array_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        return array_buffer

    def compileProgram(self):
        '''
        Compiles the vertex shader and the fragment shader and
        runs glUseProgram on the resulting program object
        '''
        # Compile each shader
        vertex_shader = shaders.compileShader(vs_src, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fs_src, GL_FRAGMENT_SHADER)
        # Compile and link the program
        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)
        # Tells the GL Context that this is the pipeline to use.
        shaders.glUseProgram(self.shader)

    def setUnifroms(self):
        '''
        Sets the uniforms for the projection-matrix and the
        model-view-matrix.
        '''
        # Get the uniform location for uPMatrix
        self.uniform_perspective = glGetUniformLocation(self.shader, "uPMatrix")
        # Generate the projection matrix
        perspective_matrix = perspective(45., 1., 0.1, 100.)
        # Copy the values from our matrix to the uniform location
        glUniformMatrix4fv(self.uniform_perspective, 1, GL_FALSE, perspective_matrix)

        # Get the uniform location for uMVMatrix
        self.uniform_mv = glGetUniformLocation(self.shader, "uMVMatrix")
        # Just use an identity matrix for now
        mv_matrix = np.identity(4, dtype=np.float32)
        # Copy the 4x4 floating point matrix to the uniform location
        glUniformMatrix4fv(self.uniform_mv, 1, GL_FALSE, mv_matrix)

    def drawVBO(self, vertices, attribute_location):
        '''
        Builds a VBO for the vertices and binds it to the attribute specified

        Note: does not actually call draw
        '''
        vertex_buffer = self.makeVertexBuffer(vertices)
        # bind vertex buffer to attribute_position
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        glEnableVertexAttribArray(attribute_location)
        glVertexAttribPointer(attribute_location, 3, GL_FLOAT, GL_FALSE, 0, None)

    def drawScene(self):
        '''
        Draws the scene
            1. Clear the scene
            2. Get the vertex attribute
            3. Build the host vertex buffer
            4. Copy to device
        '''

        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.attribute_position = glGetAttribLocation(self.shader, 'aPosition')

        vertices = np.array([
                [-0.90, -0.90, -2.],
                [ 0.85, -0.90, -2.],
                [-0.90,  0.85, -2.],
                [ 0.90, -0.85, -2.],
                [ 0.90,  0.90, -2.],
                [-0.85,  0.90, -2.],
                ],dtype=np.float32)
        
        self.drawVBO(vertices, self.attribute_position)
        self.setUnifroms()


    def display(self):
        '''
        Renders the frame
        '''
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
