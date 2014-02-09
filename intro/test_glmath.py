import unittest
import numpy as np
from glmath import perspective

class TestGLMath(unittest.TestCase):
    def test_perspective(self):
        out = perspective(45., 1., 0.1, 100.)
        correct = np.array([[1.792591,0.000000,0.000000,0.000000,],
                            [0.000000,1.792591,0.000000,0.000000,],
                            [0.000000,0.000000,-1.002002,-1.000000,],
                            [0.000000,0.000000,-0.200200,0.000000,]], dtype=np.float32)
        np.testing.assert_array_almost_equal(out, correct)

