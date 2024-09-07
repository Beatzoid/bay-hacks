import numpy as np
import datetime
import cv2
from ultralytics import YOLO
from collections import deque

from deep_sort.deep_sort.tracker import Tracker
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
from deep_sort.tools import generate_detections as gdet

from helper import create_video_writer

def detecting_the_objects():
    
    # define some parameters
    conf_threshold = 0.5
    max_cosine_distance = 0.4
    nn_budget = None
    points = [deque(maxlen=32) for _ in range(1000)] # list of deques to store the points

    # Initialize the video capture and the video writer objects
    video_cap = cv2.VideoCapture("image_recognition/lkj.mp4")
    writer = create_video_writer(video_cap, "image_recognition/output.mp4")

    # Initialize the YOLOv8 model using the default weights
    model = YOLO("image_recognition/yolov8s.pt")

    # Initialize the deep sort tracker
    model_filename = "image_recognition/config/mars-small128.pb"
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    metric = nn_matching.NearestNeighborDistanceMetric(
        "cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    # load the COCO class labels the YOLO model was trained on
    classes_path = "image_recognition/config/coco.names"
    with open(classes_path, "r") as f:
        class_names = f.read().strip().split("\n")

    # create a list of random colors to represent each class
    np.random.seed(42)  # to get the same colors
    colors = np.random.randint(0, 255, size=(len(class_names), 3))  # (80, 3)

    # loop over the frames
    while True:
        # starter time to computer the fps
        start = datetime.datetime.now()
        ret, frame = video_cap.read()
        # if there is no frame, we have reached the end of the video
        if not ret:
            # print("End of the video file...")
            break
        overlay = frame.copy()
        

        ############################################################
        ### Detect the objects in the frame using the YOLO model ###
        ############################################################

        # run the YOLO model on the frame
        results = model(frame)

        # loop over the results
        for result in results:
            # initialize the list of bounding boxes, confidences, and class IDs
            bboxes = []
            confidences = []
            class_ids = []

            # loop over the detections
            for data in result.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = data
                x = int(x1)
                y = int(y1)
                w = int(x2) - int(x1)
                h = int(y2) - int(y1)
                class_id = int(class_id)

                # filter out weak predictions by ensuring the confidence is
                # greater than the minimum confidence
                if confidence > conf_threshold:
                    bboxes.append([x, y, w, h])
                    confidences.append(confidence)
                    class_ids.append(class_id)
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
        ############################################################
        ### Track the objects in the frame using DeepSort        ###
        ############################################################

        # get the names of the detected objects
        names = [class_names[class_id] for class_id in class_ids]

        # get the features of the detected objects
        features = encoder(frame, bboxes)
        # convert the detections to deep sort format
        dets = []
        for bbox, conf, class_name, feature in zip(bboxes, confidences, names, features):
            dets.append(Detection(bbox, conf, class_name, feature))
            # print(bbox, conf, class_name, feature)
            # print()
            # print()

        # run the tracker on the detections
        tracker.predict()
        tracker.update(dets)

        # loop over the tracked objects
        X = len(tracker.tracks)
        

    return X



print(detecting_the_objects())
