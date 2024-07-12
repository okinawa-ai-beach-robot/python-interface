from .. import logger
from .debrisdetector import DerbrisDetector
import onnxruntime
import numpy as np

class Yolo5Onnx(DerbrisDetector):
    _description="""
    YOLOv5 implementation based on ONNXruntime framework.\n
    Supports hardware acceleration via CUDA if available on platform.\n
    Tensorrt acceleration is not yet implemented.
    """

    def __init__(self, model_file, use_accel=True) -> None:
        super().__init__(model_file)
        providers=["CPUExecutionProvider"]
        if use_accel and 'TensorrtExecutionProvider' in onnxruntime.get_available_providers():
            logger.info("TODO: Ignore Tensorrt for now!!")
            providers=["CUDAExecutionProvider"]
        elif use_accel and 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
            providers=["CUDAExecutionProvider"]
        else:
            logger.info("No Gpu acceleration availabe!")
        logger.info("DL providers are:" + str(providers))
        self.session = onnxruntime.InferenceSession(model_file, providers=providers)
        if self.session is None:
            raise ValueError("Failed to load the model " + model_file)
        input_shapes = self.session.get_inputs()[0].shape
        input_type = self.session.get_inputs()[0].type
        self.img_width = input_shapes[3]
        self.img_height = input_shapes[2]
        logger.info("model type is " + str(input_type))
        if "float16" in input_type:
            self.dtype=np.float16
        elif "float32" in input_type or "float" in input_type:
            self.dtype=np.float32

    def apply_model(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        inputs = np.swapaxes(np.swapaxes(inputs, 0, -1), -2, -1)[None, :, :, :] / 255.0
        if inputs.dtype != self.dtype:
            inputs = inputs.astype(self.dtype)
        prediction = self.session.run(None, {"images": inputs})
        return self.wrap_detection(prediction[0][0], confidence_threshold=confidence_threshold, class_threshold=class_threshold)

    def apply_model_percent(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        inputs = np.swapaxes(np.swapaxes(inputs, 0, -1), -2, -1)[None, :, :, :] / 255.0
        if inputs.dtype != self.dtype:
            inputs = inputs.astype(self.dtype)
            
        prediction = self.session.run(None, {"images": inputs})
        return self.wrap_detection_percent(prediction[0][0], confidence_threshold=confidence_threshold, class_threshold=class_threshold)


DerbrisDetector.add_model("YOLOv5", Yolo5Onnx)
