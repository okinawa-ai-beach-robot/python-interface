from .. import logger
from .debrisdetector import DerbrisDetector
import onnxruntime
import numpy as np
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import yaml

class MediaPipeMobilenet(DerbrisDetector):
    _description="""
    TODO
    """

    def __init__(self, model_file, use_accel=True) -> None:
        #super().__init__(model_file)
        self.dtype=np.float16
        self.num_classes=0
        self.list_classes=[]
        print(model_file)
        model_folder = os.path.realpath(model_file)
        if not model_file.endswith("/"):
            model_folder = os.path.dirname(model_folder)
        print(model_folder)
        model_type=None
        with open(model_folder + "/export_info.yaml", 'r') as stream:
            export_info = yaml.safe_load(stream)
            self.list_classes = export_info['classes']
            self.num_classes = len(self.list_classes)
            print(self.list_classes)
            self.clsmap = {a:b for b,a in enumerate(self.list_classes)}
            print(self.clsmap)

        base_options = python.BaseOptions(model_asset_path=model_folder + '/model.tflite')
        options = vision.ObjectDetectorOptions(base_options=base_options,
                                            score_threshold=0.5)
        self.detector = vision.ObjectDetector.create_from_options(options)

    def crop_and_scale_image(self, image):
        return image

    


    def apply_model(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        inimg = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(inputs))
        detection_result = self.detector.detect(inimg)

        class_ids = []
        confidences = []
        boxes = []

        
        for box in detection_result.detections:
            cate = box.categories[0] #TODO only assume one category for now
            cls_name = cate.category_name
            cls_score = cate.score
            cls_box = box.bounding_box

            if cls_score >= confidence_threshold:
                class_ids.append(self.clsmap[cls_name])
                confidences.append(cls_score)

                left = cls_box.origin_x
                top = cls_box.origin_y
                width = cls_box.width
                height = cls_box.height

                boxes.append(np.array([left, top, width, height]))
                
        return class_ids, confidences, boxes



    def apply_model_percent(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        x_factor = 1/inputs.shape[1]
        y_factor = 1/inputs.shape[0]


        inimg = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(inputs))
        detection_result = self.detector.detect(inimg)

        class_ids = []
        confidences = []
        boxes = []

        for box in detection_result.detections:
            cate = box.categories[0] #TODO only assume one category for now
            cls_name = cate.category_name
            cls_score = cate.score
            cls_box = box.bounding_box

            if cls_score >= confidence_threshold:
                class_ids.append(self.clsmap[cls_name])
                confidences.append(cls_score)

                x = cls_box.origin_x
                y = cls_box.origin_y
                w = cls_box.width
                h = cls_box.height

                left = ((x - 0.5 * w) * x_factor)
                top = ((y - 0.5 * h) * y_factor)
                width = (w * x_factor)
                height = (h * y_factor)

                boxes.append(np.array([left, top, width, height]))
            
        return class_ids, confidences, boxes



DerbrisDetector.add_model("MediaPipeMobilenet", MediaPipeMobilenet)
