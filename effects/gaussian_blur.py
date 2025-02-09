import numpy as np

from effect import Effect
import cv2 as cv

from parameter import Parameter


class GaussianBlur(Effect):

    def my_effect(self):
        kernel_size = getattr(self, "kernel")
        return cv.GaussianBlur(getattr(self, "frame"), (kernel_size, kernel_size), getattr(self, "sigmaX"))

    def init_parameters(self):
        return {
            "kernel": Parameter("Kernel", 1, 1, 5, 13, 1001, 2),
            "sigmaX": Parameter("SigmaX", 1, 1, 5, 13, 1001, 2),
        }

    def init_display_name(self):
        return "Gaussian Blur"
