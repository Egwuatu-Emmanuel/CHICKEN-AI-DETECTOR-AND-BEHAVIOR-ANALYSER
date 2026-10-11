import cv2

from .config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)

import cv2


class Camera:

    def __init__(self, video_path):
        self.capture = cv2.VideoCapture("1,069 Chicken Farm House Videos, Clips and Stock Footage - Getty Images.mp4")

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Could not open video file: {video_path}"
            )

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            FRAME_WIDTH
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            FRAME_HEIGHT
        )


# class Camera:

#     def __init__(self):
#         self.capture = cv2.VideoCapture(CAMERA_INDEX)

#         if not self.capture.isOpened():
#             raise RuntimeError(
#                 "Could not open the camera."
#             )

#         self.capture.set(
#             cv2.CAP_PROP_FRAME_WIDTH,
#             FRAME_WIDTH
#         )

#         self.capture.set(
#             cv2.CAP_PROP_FRAME_HEIGHT,
#             FRAME_HEIGHT
#         )

    def read(self):

        success, frame = self.capture.read()

        if not success:
            raise RuntimeError(
                "Could not read frame from camera."
            )

        return frame

    def release(self):

        self.capture.release()