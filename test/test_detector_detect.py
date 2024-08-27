import pytest
from pathlib import Path
import cv2
from fire_helmet.detection.detector import Detector


model_path = str(Path.cwd().parent / "fire_helmet/detection/model/fire_helmet_edgetpu.tflite")
detector = Detector(model_path)

scenarios = (
    [
        "Two Dogs",
        "test_images/dog_dog.png"
    ],
)

test_ids = [i[0] for i in scenarios]


@pytest.mark.parametrize("test_name, input_data_path", scenarios, ids=test_ids)
def test_detect(test_name: str, input_data_path: str):
    image_fullpath = str(Path(input_data_path).resolve())
    image = cv2.imread(image_fullpath)
    res = detector.detect(image)
    print()