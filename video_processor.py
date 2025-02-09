import cv2 as cv
import numpy as np

import config


class VideoProcessor:
    def __init__(self):

        self.ordered_operations = []

    def process_frame(self, frame):

        # print(self.ordered_operations)
        for operation in self.ordered_operations:
            frame = operation.apply(frame)

        return frame
