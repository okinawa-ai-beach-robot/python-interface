import sys, os, cv2
import beachbot

# specify path to video file
vid_file = beachbot.get_data_path()+os.path.sep+"video_beach_test.mp4"
# specify which modele to use
model_file = beachbot.get_model_path()+os.path.sep+"beachbot_yolov5s_beach-cleaning-object-detection__v3-augmented_ver__2__yolov5pytorch_1280"+os.path.sep+"best.onnx"
# specify which frames of the video to analyze
frame_numbers = [0,10,20]

# Open openCV video device
video_capture = cv2.VideoCapture(vid_file)
total_num_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
video_capture.set(cv2.CAP_PROP_POS_FRAMES,0)



# Read first frame of video to test if file is available and to read resolution
success, frame_bgr = video_capture.read()
frame = frame_bgr[..., ::-1]  # OpenCV image (BGR to RGB)
if not success:
    beachbot.logger.error("Video " + vid_file + " file could not be loaded")
    sys.exit(-1)
img_width = frame.shape[1]
img_height = frame.shape[0]
beachbot.logger.info("Video " + vid_file + " loaded, resolution is " + str(img_width)+"x"+str(img_height))





beachbot.logger.info("Load AI model")
model_type = beachbot.ai.DerbrisDetector.get_model_type(model_file)
beachbot.logger.info("Model type is" + str(model_type))

model_cls_list= beachbot.ai.DerbrisDetector.list_models_by_type(model_type)
beachbot.logger.info("Available model backends are " + str(model_cls_list))
beachbot.logger.info("Here we will take the first one: " + str(model_cls_list[0]))

# Instantiate ai model class
ai_detect = model_cls_list[0](model_file=model_file, use_accel=True)
class_threshold=0.25
confidence_threshold=0.2
# Perform one inital evaluation to initialize the model
# First: preprocess frame to fir model data format:
frame = ai_detect.crop_and_scale_image(frame)
# Second: apply model, ignore results, as this is just one inital dummy execution of the model to initialze internal buffers etc
class_ids, confidences, boxes = ai_detect.apply_model_percent(frame, confidence_threshold=confidence_threshold, class_threshold=class_threshold)
beachbot.logger.info("Done loading AI model")


# Do example inference on list of frame numbers of video:
for f_num in frame_numbers:
    print("Processing frame number", f_num)
    # Set video frame to requested frame number
    video_capture.set(cv2.CAP_PROP_POS_FRAMES,int(f_num))
    # Read frame from video file
    succ, frame_bgr = video_capture.read()
    # OpenCV image (BGR to RGB)
    frame = frame_bgr[..., ::-1]  
    # Process input image to fit requested format of AI model
    frame = ai_detect.crop_and_scale_image(frame)
    # Apply model
    class_ids, confidences, boxes = ai_detect.apply_model_percent(frame, confidence_threshold=confidence_threshold, class_threshold=class_threshold)
    # Print detected objects (boxes, id and confidence)
    for classid, confidence, box in zip(class_ids, confidences, boxes):
        if confidence >= 0.01:
            print("\tObject [", *box, "](left, top, width, height) has class id", ai_detect.list_classes[classid], "with confidence", confidence)
    if len(class_ids)==0:
        print("\tNothing detected in current frame.")