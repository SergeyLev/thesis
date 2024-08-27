import queue
import threading
from typing import List

import ultralytics
import numpy as np
from numpy.typing import NDArray
from ultralytics import YOLO


class Detector(threading.Thread):
    def __init__(self, model_path: str, input: queue.Queue, output: queue.Queue, threshold=0.8, img_size=640):
        super().__init__()
        self.model = YOLO(model=model_path, task="detect", verbose=False)
        self.threshold = threshold
        self.img_size = img_size
        self.input = input
        self.output = output
        self._stop = threading.Event()

        # warmup
        self.detect(np.zeros((self.img_size, self.img_size, 3), dtype=np.uint8))

    def detect(self, frame: NDArray[np.uint8]) -> List[ultralytics.engine.results.Results]:
        """
        Function sets up a predictor if not set already and starts prediction
        :param frame: Frame recieved from a camera as np.array
        :return: Prediction results if any as list of Results object
        """
        return self.model.predict(
            source=frame,
            conf=self.threshold,
            imgsz=self.img_size,
            verbose=False,
            stream=True,
            show=False
        )

    def run(self):
        while not self._stop.is_set():
            try:
                frame = self.input.get(timeout=1)
                result = self.detect(frame)
                self.output.put(result)
            except queue.Empty:
                continue

    def stop(self):
        self._stop.set()
