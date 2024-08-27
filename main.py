import time
import queue

import cv2

from fire_helmet.detection.detector import Detector
from fire_helmet.vision.camera import Camera
from fire_helmet.vision.painter import Painter
from fire_helmet.vision.screen import Screen


def run_app():
    input_q = queue.Queue()
    output_q = queue.Queue()

    try:
        camera = Camera()
        screen = Screen()
        painter = Painter()
        detector = Detector("fire_helmet/detection/model/fire_helmet_edgetpu.tflite", input_q, output_q)
        detector.start()

        camera.open_camera()
        screen.create_screen()
    except Exception:
        # Cleanup
        detector.stop()
        detector.join()
        camera.release_camera()
        Screen.destroy_screen()

    fps = 0
    while True:
        start_time = time.time()
        frame = camera.frame()

        if not screen.frame_cut_by:
            screen.frame_cut_width(frame)

        frame = screen.set_frame_resolution(frame)
        input_q.put(frame)

        try:
            detected_objects = output_q.get(block=False)
        except queue.Empty:
            detected_objects = None

        if detected_objects:
            frame = painter.draw_bbox(frame, detected_objects, fps)

        if painter.is_fps:
            fps = camera.get_fps()
            painter.show_fps(frame, fps)

        if painter.is_res:
            frame = painter.show_resolution(frame)

        cv2.imshow("eyes", frame)

        elapsed_time = time.time() - start_time
        fps = 1 / elapsed_time

        key = cv2.waitKey(50)
        if key != -1:
            print(key)

        if key == 102:  # press f to get FPS on screen
            painter.is_fps_active()
        elif key == 115:  # press s to get resolution
            painter.is_res_active()
        elif key == 100:  # press d to enable/disable detector
            pass
        elif key == 81:
            screen.calibration =+ 1
        elif key == 84:
            print(f"calibration value: {screen.calibration}")
        elif key == 27:  # press ESC to stop execution
            break

    # Cleanup
    detector.stop()
    detector.join()
    camera.release_camera()
    Screen.destroy_screen()


if __name__ == '__main__':
    run_app()
