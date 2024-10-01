from .. import logger
from .debrisdetector import DerbrisDetector
import numpy as np
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import yaml

class MediaPipeMobilenet(DerbrisDetector):
    _description="""
    Google mediapipe implementation of SSDMobilenetV2 and related architectures.
    Based on tflite export of model.
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
        #TODO optimize parameters for speedup possilbe?
        options = vision.ObjectDetectorOptions(base_options=base_options, running_mode=vision.RunningMode.IMAGE, max_results=10, score_threshold=0.5)
        self.detector = vision.ObjectDetector.create_from_options(options)


    


    def apply_model(self, inputs, confidence_threshold=0.2, units_percent=True):  
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
                if units_percent:
                    # percent estimate, relative to image size
                    left /= inputs.shape[1]
                    top /= inputs.shape[0]
                    width /= inputs.shape[1]
                    height /= inputs.shape[0]
                else:
                    # pixel coordinates, rond float estimates
                    left = round(left)
                    top = round(top)
                    width = round(width)
                    height = round(height)

                boxes.append(np.array([left, top, width, height]))
                
        return class_ids, confidences, boxes



DerbrisDetector.add_model("MediaPipeMobilenet", MediaPipeMobilenet)
