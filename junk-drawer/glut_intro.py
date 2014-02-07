from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

vertices = np.array([
    -1, 0, 0, # left
     1, 0, 0, # right
     0, 1, 0  # top
     ], dtype=np.float32)

colors = np.array([
    1, 0, 0, 1,  # red
    0, 1, 0, 1,  # green
    0, 0, 1, 1   # blue
    ], dtype=np.float32)



fshader = '''
void main(void) {
    gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
'''
vshader = '''
attribute vec3 aVertexPosition;

uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;

void main(void) {
    gl_Position = uPMatrix * uMVMatrix * vec4(aVertexPosition, 1.0);
}
'''

class GLError(Exception):
    pass

class GLHello(object):
    def __init__(self):
        glutInit()
        glutInitWindowSize(640,480)
        glutCreateWindow("Hello")
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutDisplayFunc(self.drawScene)
        self.initFun()
        glutMainLoop()

    def getShader(self, source, shader_type):
        if 'fragment' in shader_type:
            shader = glCreateShader(GL_FRAGMENT_SHADER)
        elif 'vertex' in shader_type:
            shader = glCreateShader(GL_VERTEX_SHADER)

        glShaderSource(shader, source)
        glCompileShader(shader)
        infoLogLen = glGetShaderiv(shader, GL_INFO_LOG_LENGTH)
        if infoLogLen:
            infoLog =  glGetShaderInfoLog(shader)
            raise GLError("Error compiling shader: " , infoLog)
        
        return shader 

    def initFun(self):
        self.initShaders()
        self.initBuffers()

        glViewport(0, 0, 640, 480)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_DEPTH_TEST)

        glFlush()

    def initShaders(self):
        vertex_shader = self.getShader(vshader, 'vertex')
        fragment_shader = self.getShader(fshader, 'fragment')

        shaderProgram = glCreateProgram()
        if not shaderProgram:
            raise GLError("Initializing Shader Program")

        glAttachShader(shaderProgram, vertex_shader)
        glAttachShader(shaderProgram, fragment_shader)
        glLinkProgram(shaderProgram)

        infoLogLen = glGetProgramiv(shaderProgram, GL_INFO_LOG_LENGTH)
        if infoLogLen:
            infoLog = glGetProgramInfoLog(shaderProgram)
            raise GLError("Error linking program: ", infoLog)

        linkStatus = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
        if linkStatus == GL_FALSE:
            raise GLError("Failed to link the program")

        glUseProgram(shaderProgram)
        self.shader = shaderProgram

        self.vertexPositionAttr = glGetAttribLocation(shaderProgram, "aVertexPosition")
        glEnableVertexAttribArray(self.vertexPositionAttr)

        self.pMatrixUniform = glGetUniformLocation(shaderProgram, "uPMatrix")
        self.mvMatrixUniform = glGetUniformLocation(shaderProgram, "uMVMatrix")
        
    def setMatrixUniforms(self):
        glUniformMatrix4fv(self.pMatrixUniform, 1, GL_FALSE, self.pMatrix)
        glUniformMatrix4fv(self.mvMatrixUniform, 1, GL_FALSE, self.mvMatrix)

    def initBuffers(self):
        vertexPositionBuffer = glGenBuffers(1)
        print repr(vertexPositionBuffer)
        print type(vertexPositionBuffer)
        glBindBuffer(GL_ARRAY_BUFFER, vertexPositionBuffer)
        glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

        self.vertexPositionBuffer = vertexPositionBuffer
        return vertexPositionBuffer

    def drawScene(self):
        glViewport(0, 0, 640, 480)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.mvMatrix = np.array([
            1, 0, 0, 0, 
            0, 1, 0, 0, 
            0, 0, 1, 0, 
            1.5, 0, -7, 1], dtype=np.float32)

        self.pMatrix = np.array([
            2.4142136573791504, 0, 0, 0, 
            0, 2.4142136573791504, 0, 0, 
            0, 0, -1.0020020008087158, -1, 
            0, 0, -0.20020020008087158, 0], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, self.vertexPositionBuffer)
        glVertexAttribPointer(self.vertexPositionAttr, 3, GL_FLOAT, GL_FALSE, 0, 0)
        self.setMatrixUniforms()

        glDrawArrays(GL_TRIANGLES, 0, 3)
        print 'made it this far'


if __name__ == '__main__':
    GLHello()

