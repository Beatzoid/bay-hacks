import udpsocket as U
from image_recognition.object_detection_tracking.py import object_detection
from traffic_algorithm.algorithmic_timing.py import traffic_algorithm
from python_utils.py import jpg_to_single_frame_mp4, extract_first_digit

# Create UDP socket to use for sending (and receiving)
sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)
print("Listening")

obs = [0 for _ in range(4)]
while True:
    data = sock.ReadReceivedData()  # read data

    if data is not None:  # if NEW data has been received since last ReadReceivedData function call
        # print(data)

        obs[extract_first_digit(data)] = object_detection(jpt_to_single_frame_mp4(data))
        

