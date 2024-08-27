import cv2
import numpy as np


class Screen:
    def __init__(self):
        self.screen_width = 1024
        self.frame_center = None
        self.frame_cut_by = None
        self.calibration = 0

    @staticmethod
    def create_screen():
        """
        Function creates new window to be used as output, and sets it to work in fullscreen mode
        """
        cv2.namedWindow("eyes", cv2.WINDOW_NORMAL)
        cv2.setWindowProperty("eyes", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    @staticmethod
    def destroy_screen():
        cv2.destroyAllWindows()

    def frame_cut_width(self, frame: np.array):
        """
        Function calculates dimensions needed to crop initial frame
        :param frame: np.array
        """
        _, w, _ = frame.shape
        self.frame_center = int(w / 2)
        self.frame_cut_by = int((w - self.screen_width) / 4)

    def set_frame_resolution(self, frame: np.array) -> np.array:
        """
        Function crops frame to get center image for each eye
        :param frame: np.array
        :return: cropped frame as np.array
        """

        left_eye = frame[:, :self.frame_center]
        right_eye = frame[:, self.frame_center:]

        left_eye = left_eye[:, self.frame_cut_by+self.calibration:self.frame_center - self.frame_cut_by + self.calibration]
        right_eye = right_eye[:, self.frame_cut_by-self.calibration:self.frame_center - self.frame_cut_by - self.calibration]

        return cv2.hconcat([left_eye, right_eye])
