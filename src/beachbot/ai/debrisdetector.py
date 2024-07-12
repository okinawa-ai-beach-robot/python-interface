import os
import numpy as np
import cv2 as cv
import yaml



from .. import get_model_path, logger



class DerbrisDetector():
    _model_lib={}
    _description="""
    Abstract base class of coastal debris classificator.\n
    can not be used direclty, please use implementation found in sublcasses.
    """

    def __init__(self, model_file=None) -> None:

        self.img_height = -1
        self.img_width = -1
        self.dtype=None
        self.num_classes=0
        self.list_classes=[]


        if model_file is not None:
            model_folder = os.path.dirname(os.path.realpath(model_file))
            with open(model_folder + "/export_info.yaml", 'r') as stream:
                export_info = yaml.safe_load(stream)
                self.img_height = export_info['img_heigt_export']
                self.img_width = export_info['img_width_export']
                self.num_classes = str(export_info.get('nc', 6))
                self.list_classes = export_info.get('names',["other_avoid","other_avoid_boundaries","other_avoid_ocean","others_traverable","trash_easy","trash_hard"])
            logger.info("Exported ONNX model operates on images of size " + str(self.img_width) + "x" + str(self.img_height) + " [wxh] pixels")
            logger.info("Dataset defines " + str(self.num_classes) + " classes -> " +  str(self.list_classes))

    def crop_and_scale_image(self, image):
        h = image.shape[0]
        w = image.shape[1]
        intended_x = self.img_width
        intended_y = self.img_height
        ratio_w = intended_x / w
        ratio_h = intended_y / h
        maxratio = max(ratio_w, ratio_h)
        image = cv.resize(image, (int(w * maxratio), int(h * maxratio)))
        crop_w = image.shape[1] - intended_x
        crop_h = image.shape[0] - intended_y
        if crop_h > 0:
            image = image[crop_h // 2 : -crop_h // 2]
        if crop_w > 0:
            image = image[:, crop_w // 2 : -crop_w // 2]
        return image
    
    def wrap_detection(self, output_data, confidence_threshold=0.2, class_threshold=0.25):
        class_ids = []
        confidences = []
        boxes = []
        rows = output_data.shape[0]

        x_factor = 1
        y_factor = 1

        for r in range(rows):
            row = output_data[r]
            confidence = row[4]

            if confidence >= confidence_threshold:

                classes_scores = row[5:]
                class_id = np.argmax(classes_scores)

                if classes_scores[class_id] > class_threshold:
                    confidences.append(confidence)

                    class_ids.append(class_id)

                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                    left = int((x - 0.5 * w) * x_factor)
                    top = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.45)

        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in indexes:
            result_confidences.append(confidences[i])
            result_class_ids.append(class_ids[i])
            result_boxes.append(boxes[i])

        return result_class_ids, result_confidences, result_boxes


    
    def wrap_detection_percent(self, output_data, confidence_threshold=0.2, class_threshold=0.25):
        class_ids = []
        confidences = []
        boxes = []
        rows = output_data.shape[0]

        x_factor = 1/self.img_width
        y_factor = 1/self.img_height

        for r in range(rows):
            row = output_data[r]
            confidence = row[4]

            if confidence >= confidence_threshold:
                classes_scores = row[5:]
                class_id = np.argmax(classes_scores)

                if classes_scores[class_id] > class_threshold:
                    confidences.append(confidence)

                    class_ids.append(class_id)

                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                    left = ((x - 0.5 * w) * x_factor)
                    top = ((y - 0.5 * h) * y_factor)
                    width = (w * x_factor)
                    height = (h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)
                else:
                    pass
                    #print("Class score not above threshold:", classes_scores[class_id])
            else:
                pass
                #print("Confidence score not above threshold:", confidence)

        indexes = cv.dnn.NMSBoxes(boxes, confidences, confidence_threshold, 0.45)

        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in indexes:
            result_confidences.append(confidences[i])
            result_class_ids.append(class_ids[i])
            result_boxes.append(boxes[i])

        return result_class_ids, result_confidences, result_boxes
 
    def apply_model(self, inputs):
        raise NotImplementedError
    
    @staticmethod
    def draw_boxes(class_ids, confidences, boxes, image, config):
        colors = [
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
            (255, 0, 0),
        ]
        for classid, confidence, box in zip(class_ids, confidences, boxes):
            if confidence >= config:
                color = colors[int(classid) % len(colors)]
                cv.rectangle(image, box, color, 2)
        img2 = image[:, :, ::-1]
        return img2
    
    def list_models_by_type(type):
        return DerbrisDetector._model_lib.get(type, [])

    def add_model(type, modelcls):
        curr_list = DerbrisDetector._model_lib.get(type,[])
        if modelcls not in curr_list:
            curr_list.append(modelcls)
            DerbrisDetector._model_lib[type]=curr_list
            logger.info("Added class " +str(modelcls) + " with type " + str(type))

    def list_model_types():
        return list(DerbrisDetector._model_lib.keys())

    def list_model_paths():
        base_path=get_model_path()
        modelfolders = [ f.path for f in os.scandir(base_path) if f.is_dir() ]
        return modelfolders
    
    def get_model_type(modelpath):
        model_type = None
        if modelpath is not None:
            if modelpath.endswith(os.path.sep+"best.onnx"):
                modelpath=modelpath[:-len(os.path.sep+"best.onnx")]
            # load files
            with open(modelpath + os.path.sep + "export_info.yaml", 'r') as stream:
                export_info = yaml.safe_load(stream)
                model_type = export_info.get('model_type', "YOLOv5") # for backward-compatibility
        return model_type
    
    def list_models_by_path(modelpath):
        model_type = DerbrisDetector.get_model_type(modelpath)
        return DerbrisDetector.list_models_by_type(model_type)
            

    

