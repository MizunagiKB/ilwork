import unittest
import numpy as np


class test_CTest(unittest.TestCase):
    def setUp(self) -> None:
        import src.deps.util_cv2

        self.util_cv2 = src.deps.util_cv2
        return super().setUp()

    def test_util_brightness(self):

        TEST_W = 256
        TEST_H = 256
        DIV_SIZE = 16

        w, h = TEST_W // DIV_SIZE, TEST_H // DIV_SIZE

        for y in range(0, TEST_H, TEST_H // DIV_SIZE):
            for x in range(0, TEST_W, TEST_W // DIV_SIZE):
                cv2_image = np.zeros((TEST_H, TEST_W, 3), np.float32)

                cv2_image[y : y + h, x : x + w] = 255

                rx, ry, _ = self.util_cv2.brightness(cv2_image, (DIV_SIZE, DIV_SIZE))
