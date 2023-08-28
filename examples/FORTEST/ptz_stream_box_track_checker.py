import ptz_video_stream_module as streamer
import cv2
import time
from ptz_control_module import ptz_controller  as controller
from ultralytics import YOLO
import numpy as np
import threading    

#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

def position_finder(box, target):
    print("box: ", box)
    print("target: ", target)
    global tracking
    tracking = True
    if box[0] > target[0]:
        ptz.move_left()
    elif box[1] > target[1]:
        ptz.move_up()
    elif box[2] < target[2]:
        ptz.move_right()
    elif box[3] < target[3]:
        ptz.move_down()
    tracking = False

model = YOLO("band.pt", "v8")

my_file = open("classes.txt", "r")
data = my_file.read()
classes = data.split("\n")
my_file.close()


colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading camera
video = streamer.ptz_streamer(IP,PORT,USER,PASS)
cap = cv2.VideoCapture(video.uri)

cap.set(cv2.CAP_PROP_BUFFERSIZE, 3) # added to limit the buffer size
pTime = 0
prev = 0 # referenced
frame_rate = 30 # referenced 
ptz = controller(IP,PORT,USER,PASS)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

font = cv2.FONT_HERSHEY_PLAIN
frame_id = 0
tracking = False


while True:
    # Capture frame-by-frame
    time_elapsed = time.time() - prev # referenced
    ret, frame = cap.read()

    # if frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    if time_elapsed > 1./frame_rate: # wait for a period time instead of using sleep method (referenced)
        prev = time.time() # referenced

        height, width, channels = frame.shape
        upper_left = (width // 4, height // 4)
        bottom_right = (width * 3 // 4, height * 3 // 4)
        box_area = (upper_left[0], upper_left[1], bottom_right[0], bottom_right[1])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        # Predict on image
        detect_params = model.predict(source=[frame], conf=0.45, save=False)

        # Convert tensor array to numpy
        DP = detect_params[0].cpu().numpy()
        print(DP)

        if len(DP) != 0:

            for i in range(len(detect_params[0])):
                print(i)

                boxes = detect_params[0].boxes
                box = boxes[i]
                clsID = 0
                conf = box.conf.cpu().numpy()[0]
                bb = box.xyxy.cpu().numpy()[0]
                frame_id += 1

                target = (bb[0], bb[1], bb[2], bb[3])

                # If position_finder function already running, do not run it again
                if not tracking:
                    position_finder(box_area, target)

                cv2. rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    colors[int(clsID)],
                    3,
                )

                cv2.putText(
                    frame,
                    classes[int(clsID)] + " " + str(round(conf, 3)) + "%",
                    (int(bb[0]), int(bb[1]) - 10),
                    font,
                    1,
                    (255,255,255),
                    2,
                )
            if "drone" in classes:
                print("drone found")
        cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3,(0,255,0), 2)
        cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 0), thickness=1)
        cv2.imshow('frame', frame)

    # Terminate run when "0" pressed
    if cv2.waitKey(1) == ord('q'):
        break
 