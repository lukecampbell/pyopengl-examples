import numpy as np

def perspective(fovy, aspect, near, far):
    f  = 1.0 / np.tan(fovy / 2.)
    nf = 1.0 / (near - far)

    a = f / aspect
    b = (far + near) * nf
    c = (2 * far * near) * nf

    mat = np.empty(16, dtype=np.float32)

    mat[0] = f / aspect
    mat[1] = 0
    mat[2] = 0
    mat[3] = 0
    mat[4] = 0
    mat[5] = f
    mat[6] = 0
    mat[7] = 0
    mat[8] = 0
    mat[9] = 0
    mat[10] = (far + near) * nf
    mat[11] = -1
    mat[12] = 0
    mat[13] = 0
    mat[14] = (2 * far * near) * nf
    mat[15] = 0

    return mat.reshape(4,4)


