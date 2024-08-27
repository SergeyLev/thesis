import cv2

from fire_helmet.usb.camera_cli import camera_reset

from fire_helmet.exceptions import CameraBusy, CameraException


class Camera:
    def __init__(self):
        self.camera = None

    def open_camera(self):
        """
        Function creates VideoCapture instance with required setting to work with camera: video codec, resolution,
        frames per second, and makes a check if data can be received from camera
        :return: Instance of cv2.VideoCapture
        """
        try:
            self._make_camera()
            if not self.camera.isOpened():
                raise CameraBusy
        except CameraBusy:
            try:
                camera_reset()
                self._make_camera()
            except CameraException:
                print("Camera is not accessible")

    def _make_camera(self):
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        cap.set(cv2.CAP_PROP_FPS, 30)
        self.camera = cap

    def release_camera(self):
        self.camera.release()

    def frame(self):
        ret, frame = self.camera.read()
        if ret:
            return frame
        else:
            raise CameraBusy

    def get_fps(self):
        return self.camera.get(cv2.CAP_PROP_FPS)
