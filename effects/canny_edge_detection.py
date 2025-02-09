from effect import Effect
import cv2 as cv

from parameter import Parameter



class CannyEdgeDetection(Effect):

    def my_effect(self):
        gray_frame = cv.cvtColor(getattr(self, "frame"), cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray_frame, getattr(self, "t1"), getattr(self, "t2"))
        return cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

    def init_parameters(self):

        return {
            "t1": Parameter( "Threshold 1", 0,0,100,200,1000,1),
            "t2": Parameter( "Threshold 2", 0,0,200,300,1000,1),
        }

    def init_display_name(self):
        return "Canny Edge Detection"
