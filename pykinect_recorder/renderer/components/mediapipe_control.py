import os
import cv2
from abc import abstractmethod

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from PySide6.QtCore import Slot, QThread, QTimer
from PySide6.QtGui import QImage

from ..signals import all_signals
from ...pyk4a import Device


class MediaPipeConfig:
    def __init__(self) -> None:
        self.model_input_size = None
        self.model_option = None
        self.model_path = None
        self.root_path = os.path.dirname(os.path.abspath(__file__))

        self.mediapipe_input_sizes = {
            "ssdmobilenet_v2": (256, 256),
            "efficientdet_lite0": (320, 320),
            "efficientdet_lite2": (448, 448),   
            "selfiesegmenter_square": (256, 256),
            "selfiesegmenter_landscape": (144, 256),
            "selfie_multiclass": (256, 256),
            "deeplab_v3": (257, 257)
        }

    def set_config(self, value: list[str, str]) -> None:
        self.model_input_size = self.mediapipe_input_sizes['_'.join(value[1].split('_')[:2])]
        self.model_option = value[0]
        self.model_path = value[1] + ".tflite" if self.model_option != 'pose_landmark_detection' else value[1] + ".task"
        self.model_path = os.path.join(self.root_path, "mediapipe_model_ckpt", self.model_path)

    def __str__(self) -> str:
        return 'Current Selected model config \n' + \
            f'input_size: {self.model_input_size}\n' + \
            f'model_option: {self.model_option}\n' + \
            f'model_path: {self.model_path}\n'


class MediaPipeModel:
    def __init__(self, config: MediaPipeConfig) -> None:
        self.model_config = config
        self.model = None
        self.set_model()

    def set_model(self) -> None:
        base_option = python.BaseOptions(model_asset_path=self.model_config.model_path)
        options = {
            "object_detection": vision.ObjectDetectorOptions(base_options=base_option, score_threshold=0.5),
            "semantic_segmentation": vision.ImageSegmenterOptions(base_options=base_option, output_category_mask=True),
            "face_detection": vision.FaceDetectorOptions(base_options=base_option),
            "pose_landmark_detection": vision.PoseLandmarkerOptions(base_options=base_option, output_segmentation_masks=True),
        }.get(self.model_config.model_option, lambda: "Invalid model option")

        self.model = {
            "object_detection": vision.ObjectDetector.create_from_options(options),
            # "semantic_segmentation": vision.ImageSegmenter.create_from_options(options),
            # "face_detection": vision.FaceDetector.create_from_options(options),
            # "pose_landmark_detection": vision.PoseLandmarker.create_from_options(options),
        }.get(self.model_config.model_option, lambda: "Invalid model option")


class MediaPipeBaseDetector(QThread):
    def __init__(self, device: Device, model: MediaPipeModel) -> None:
        super().__init__()
        self.device = device
        self.model = model

        self.timer = QTimer()
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.update_next_frame)

    # capture Image
    def update_next_frame(self) -> None:
        current_frame = self.device.update()
        ret, rgb_frame = current_frame.get_color_image()
        if ret:
            self.h, self.w, self.ch = rgb_frame.shape
            # resized_img = cv2.resize(rgb_frame, self.model.model_config.model_input_size)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            self.inference(rgb_frame, mp_img)

    # inference Image
    @abstractmethod
    def inference(self, np_img: np.ndarray, mp_img: mp.Image) -> None:
        pass


class MediaPipeObjectDetector(MediaPipeBaseDetector):
    MARGIN = 10  # pixels
    ROW_SIZE = 10  # pixels
    FONT_SIZE = 1
    FONT_THICKNESS = 1
    TEXT_COLOR = (255, 0, 0)  # red

    def __init__(self, device: Device, model: MediaPipeModel) -> None:
        super().__init__(device, model)

    def inference(self, np_img: np.ndarray, mp_img: mp.Image) -> None:
        result = self.model.model.detect(mp_img)
        result_img = self.visualize(np_img, result)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        result_img = QImage(result_img, self.w, self.h, self.ch * self.w, QImage.Format_RGB888)
        all_signals.mediapipe_signals.model_result.emit(result_img)

    def visualize(self, np_img: np.ndarray, result: list) -> np.ndarray:
        for detection in result.detections:
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(np_img, start_point, end_point, self.TEXT_COLOR, 3)

            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            result_text = category_name + ' (' + str(probability) + ')'
            text_location = (self.MARGIN + bbox.origin_x,
                            self.MARGIN + self.ROW_SIZE + bbox.origin_y)
            cv2.putText(np_img, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        self.FONT_SIZE, self.TEXT_COLOR, self.FONT_THICKNESS)
        return np_img



class MediaPipeSegmentationDetector(MediaPipeBaseDetector):
    BG_COLOR = (192, 192, 192) # gray
    MASK_COLOR = (255, 255, 255) # white
    def __init__(self) -> None:
        super().__init__()

    def inference(self, np_img: np.ndarray, mp_img: mp.Image) -> None:
        result = self.model.model.segment(mp_img)
        result_img = self.visualize(np_img, result)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        result_img = QImage(result_img, self.w, self.h, self.ch * self.w, QImage.Format_RGB888)
        all_signals.mediapipe_signals.model_result.emit(result_img)

    def visualize(self, np_img: np.ndarray, result: list) -> np.ndarray:
        # Draw segmentation mask
        category_mask = result.category_mask
        fg_image = np.zeros(np_img.shape, dtype=np.uint8)
        fg_image[:] = self.MASK_COLOR
        bg_image = np.zeros(np_img.shape, dtype=np.uint8)
        bg_image[:] = self.BG_COLOR

        condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
        output_image = np.where(condition, fg_image, bg_image)
        return output_image

    # def resize_and_show(np_img: np.ndarray):
    #     h, w = np_img.shape[:2]
    #     if h < w:
    #         img = cv2.resize(np_img, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    #     else:
    #         img = cv2.resize(np_img, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    #     cv2_imshow(img)


# class MediaPipeFaceDetector(MediaPipeBaseDetector):
#     def __init__(self) -> None:
#         super().__init__()


# class MediaPipePoseLandmarkDetector(MediaPipeBaseDetector):
#     def __init__(self) -> None:
#         super().__init__()


