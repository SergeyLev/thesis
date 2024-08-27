import cv2
import numpy as np


class Painter:
    def __init__(self):
        self.is_fps = False
        self.is_res = False
        self.text_settings = self._text_kwargs

    @property
    def _text_kwargs(self):
        return {
            "font": cv2.FONT_HERSHEY_SIMPLEX,
            "fontScale": 1.0,
            "color": (255, 0, 0),
            "thickness": 2,
            "org": (50, 50)
        }

    def is_fps_active(self):
        self.is_fps = not self.is_fps

    def is_res_active(self):
        self.is_res = not self.is_res

    def show_fps(self, frame, fps):
        return add_text(frame, f"Camera FPS: {fps}", **self.text_settings)

    def show_resolution(self, frame):
        kwargs = self.text_settings
        fr = frame.shape
        return add_text(frame, f"Frame resolution: {fr}", **kwargs)

    def draw_bbox(self, frame, detections, fps=None):
        for det in detections:
            frame = self._draw_detection_boxes(frame, det)

        if fps is not None:
            frame = self._add_text(frame, f"fps: {fps}")

        return frame

    def _draw_detection_boxes(self, frame: np.array, detection) -> np.array:
        """Helper function to draw bounding boxes for each detection.

        Args:
            frame (np.array): The image frame on which to draw.
            detection (object): Detection object containing bounding boxes.

        Returns:
            np.array: The modified frame with bounding boxes.
        """
        for box in detection.boxes:
            cls_index, conf, bb = self._extract_box_details(box)
            label = detection.names[int(cls_index)]
            frame = self._draw_single_bbox(frame, bb)
        return frame

    @staticmethod
    def _extract_box_details(box) -> tuple:
        """Extract class index, confidence, and bounding box coordinates from a box object.

        Args:
            box (object): Box object containing the details.

        Returns:
            tuple: Tuple containing class index, confidence, and bounding box coordinates.
        """
        cls_index = int(box.cls.numpy()[0])
        conf = box.conf.numpy()[0]
        bb = box.xyxy.numpy()[0]
        return cls_index, conf, bb

    @staticmethod
    def _draw_single_bbox(frame: np.array, bb: list) -> np.array:
        """Draw a single bounding box on the frame.

        Args:
            frame (np.array): The frame on which to draw.
            bb (list): Bounding box coordinates.

        Returns:
            np.array: The frame with the bounding box drawn.
        """
        start_point = (int(bb[0]), int(bb[1]))
        end_point = (int(bb[2]), int(bb[3]))
        color = (255, 0, 0)  # Red color for bounding box
        thickness = 2
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        return frame

    @staticmethod
    def _add_text(frame: np.array, text: str) -> np.array:
        """Add text to the frame.

        Args:
            frame (np.array): The frame on which to add text.
            text (str): The text to add.

        Returns:
            np.array: The frame with text added.
        """
        position = (10, 30)  # Position at which to add text
        font_scale = 1
        color = (0, 255, 0)  # Green color for the text
        thickness = 1
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, color, thickness, cv2.LINE_AA)
        return frame


def add_text(img, text, **kwargs):
    return cv2.putText(img, text, kwargs["org"], kwargs["font"],
                       kwargs["fontScale"], kwargs["color"], kwargs["thickness"], cv2.LINE_AA)
