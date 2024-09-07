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
    conf_threshold = 0.4
    max_cosine_distance = 0.4
    nn_budget = None
    points = [deque(maxlen=32) for _ in range(1000)]  # list of deques to store the points

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

    total_objects = 0  # Initialize a counter for total objects detected

    # loop over the frames
    while True:
        # starter time to computer the fps
        start = datetime.datetime.now()
        ret, frame = video_cap.read()
        # if there is no frame, we have reached the end of the video
        if not ret:
            break
        
        # Detect objects using YOLO
        results = model(frame)

        # Process YOLO detections
        bboxes = []
        confidences = []
        class_ids = []

        for result in results:
            for data in result.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = data
                if confidence > conf_threshold:
                    x, y, w, h = int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1)
                    bboxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        # Prepare detections for DeepSORT
        names = [class_names[class_id] for class_id in class_ids]
        features = encoder(frame, bboxes)
        detections = [Detection(bbox, conf, class_name, feature) 
                      for bbox, conf, class_name, feature 
                      in zip(bboxes, confidences, names, features)]

        # Update tracker
        tracker.predict()
        tracker.update(detections)

        # Count unique objects
        unique_objects = len(tracker.tracks)
        total_objects = max(total_objects, unique_objects)

        # Optional: Draw bounding boxes and labels
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            class_id = track.get_class()
            color = [int(c) for c in colors[class_id]]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.putText(frame, f"{class_names[class_id]}-{track.track_id}", 
                        (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, color, 2)

        # Write the frame to the output video
        writer.write(frame)

        # Calculate and print FPS
        end = datetime.datetime.now()
        fps = 1 / (end - start).total_seconds()
        print(f"FPS: {fps:.2f}")

    # Release resources
    video_cap.release()
    writer.release()
    cv2.destroyAllWindows()

    return total_objects

# Run the function and print the result
print(f"Total unique objects detected: {detecting_the_objects()}")