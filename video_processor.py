import cv2 as cv
import numpy as np

class VideoProcessor:
    def __init__(self):

        self.ordered_operations = []

        self.operation_map = {
            "Canny Edge Detection": self.canny_edge_detection,
            "Gaussian Blur": self.gaussian_blur,
            "Sobel": self.sobel,
        }

    def process_frame(self, frame, prev_frame, t):


        has_roi, background_frame, frame_at_difference = False, None, frame

        for operation in self.ordered_operations:
            if operation == "Running Difference":
                frame, frame_at_difference = self.running_difference(frame, prev_frame)

            elif operation == "Region of Interest":

                cropped_frame, cropped_prev_frame = self.region_of_interest(frame, prev_frame)
                background_frame = frame.copy()
                frame, prev_frame = cropped_frame, cropped_prev_frame
                has_roi = True
            else:
                frame = self.operation_map[operation](frame)

        if has_roi:
            x1, x2, y1, y2 = getattr(self, "roi")

            if frame_at_difference is not None and frame_at_difference.shape != background_frame.shape :
                background_frame_at_difference = background_frame.copy()
                background_frame_at_difference[y1:y2, x1:x2] = frame_at_difference
                frame_at_difference = background_frame_at_difference

            background_frame[y1:y2, x1:x2] = frame
            frame = background_frame

        return frame, frame_at_difference, t

    def canny_edge_detection(self, frame):
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray_frame, getattr(self, "canny_t1"), getattr(self, "canny_t2"))
        return cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

    def gaussian_blur(self, frame):
        kernel_size = getattr(self, "gaussian_kernel_size")
        return cv.GaussianBlur(frame, (kernel_size, kernel_size), getattr(self, "sigmaX"))

    def sobel(self, frame):

        kernel_size = getattr(self, "sobel_kernel_size")

        vert_gradient = cv.Sobel(frame, cv.CV_32F, 1, 0, ksize=kernel_size, borderType=cv.BORDER_REPLICATE)
        horiz_gradient = cv.Sobel(frame, cv.CV_32F, 0, 1, ksize=kernel_size, borderType=cv.BORDER_REPLICATE)

        combined_gradient = vert_gradient + horiz_gradient

        return np.uint8(np.absolute(combined_gradient))

    def region_of_interest(self, frame, prev_frame):
        x1, x2, y1, y2 = getattr(self, "roi")  # Coordinates of the ROI
        frame_to_crop = frame.copy()
        prev_frame_to_crop = prev_frame.copy()
        return frame_to_crop[y1:y2, x1:x2], prev_frame_to_crop[y1:y2, x1:x2]

    def running_difference(self, frame, prev_frame):
        if prev_frame is None:
            return frame, frame.copy()
        return cv.absdiff(frame, prev_frame), frame.copy()


