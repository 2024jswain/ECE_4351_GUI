import time
from collections import deque
from multiprocessing.pool import ThreadPool

import cv2 as cv
import streamlit as st
from streamlit_sortables import sort_items

from helpers import StatValue, DummyTask
from video_processor import VideoProcessor
import logging

logging.getLogger("cv2").setLevel(logging.ERROR)


def app():
    st.set_page_config(layout="wide")

    # Initialize session state
    if "app_configured" not in st.session_state:
        st.session_state.app_configured = True
        st.session_state.available_operations = [
            "Canny Edge Detection",
            "Running Difference",
            "Gaussian Blur",
            "Sobel",
            "Region of Interest"
        ]

        st.session_state.vp = VideoProcessor()

        st.session_state.cap = cv.VideoCapture(0)

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Select Operations:")
        selected_operations = set(
            operation for operation in st.session_state.available_operations
            if st.checkbox(operation, value=False, key=f"op_{operation}")
        )

        multi_threaded = st.checkbox("Multi Threaded", value=False, key="multi_threaded")

        st.subheader("Order Operations:")
        st.session_state.vp.ordered_operations = sort_items(list(selected_operations), direction="vertical")

        if "Canny Edge Detection" in selected_operations:
            st.write("Canny Edge Parameters:")
            st.session_state.vp.canny_t1 = st.slider("Threshold 1", 0, 255, 100, key="canny_t1")
            st.session_state.vp.canny_t2 = st.slider("Threshold 2", 0, 255, 200, key="canny_t2")

        if "Gaussian Blur" in selected_operations:
            st.write("Gaussian Blur Parameters:")
            st.session_state.vp.gaussian_kernel_size = st.slider("Kernel Size", 1, 11, 5, 2, key="gaussian")
            st.session_state.vp.sigmaX = st.slider("sigmaX", 0, 5, 0, key="sigmax")

        if "Sobel" in selected_operations:
            st.write("Sobel Parameters:")
            st.session_state.vp.sobel_kernel_size = st.slider("Kernel Size", 1, 11, 5, 2, key="sobel")

        if "Region of Interest" in selected_operations:
            st.subheader("Adjust Borders:")
            w = st.slider("Width", 0, 640, 64 * 2, step=5)
            h = st.slider("Height", 0, 480, 48 * 2, step=5)

            half_w = w // 2
            half_h = h // 2

            x_center = st.slider("Right and Left", 0 + half_w, 640 - half_w, 640 // 2, step=5)
            y_center = st.slider("Up and Down", 0 + half_h, 480 - half_h, 480 // 2, step=5)

            st.session_state.vp.roi = (x_center - half_w, x_center + half_w, y_center - half_h, y_center + half_h)

    with col2:

        if "frame_placeholder" not in st.session_state:
            st.session_state.latency_placeholder = st.empty()
            st.session_state.frame_placeholder = st.empty()

        threadn = cv.getNumberOfCPUs()
        pool = ThreadPool(processes=threadn)
        pending = deque()

        ret, prev_frame = st.session_state.cap.read()
        if ret:
            prev_frame, _, _ = st.session_state.vp.process_frame(prev_frame.copy(), prev_frame.copy(),
                                                                 time.perf_counter())

        latency, frame_interval, last_frame_time = StatValue(), StatValue(), time.perf_counter()

        while ret:

            while len(pending) > 0 and pending[0].ready():  # There are frames in the queue
                st.session_state.processed_frame, prev_frame, t0 = pending.popleft().get()
                latency.update(time.perf_counter() - t0)

                # Update latency metric
                st.session_state.latency_placeholder.metric("Latency (ms)", f"{latency.value * 1000:.2f}")

                # Update the frame placeholder
                st.session_state.frame_placeholder.image(
                    st.session_state.processed_frame,
                    channels="BGR",
                    use_container_width=True
                )

            if len(pending) < threadn:
                ret, frame = st.session_state.cap.read()

                if frame is not None:
                    t = time.perf_counter()
                    frame_interval.update(t - last_frame_time)
                    last_frame_time = t

                    if multi_threaded:
                        task = pool.apply_async(st.session_state.vp.process_frame,
                                                (frame.copy(), prev_frame.copy(), t))
                    else:
                        task = DummyTask(st.session_state.vp.process_frame(frame.copy(), prev_frame.copy(), t))

                    pending.append(task)

        if not ret:
            st.error("Camera Not Available. Please free up the camera and try again!")


if __name__ == "__main__":
    app()
