import ptz_video_stream_module as streamer
import cv2
import time
import threading
from ptz_control_module import ptz_controller  as controller
from ultralytics import YOLO
import numpy as np

#YOLOv8 update : v8버전에 맞추어 코드변경하였음.

#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

def position_finder(box, target):
    print("box: ", box)
    print("target: ", target)
    if box[0] > target[0] :
        print("move left")
        #ptz.move_left()
    elif box[1] > target[1]:
        print("move up")
        #ptz.move_up()
    elif box[2] < target[2]:
        print("move right")
        #ptz.move_right()
    elif box[3] < target[3]:
        print("move down")
        #ptz.move_down()


def drone_detection():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        height, width, channels = frame.shape
        upper_left = (width // 4, height // 4)
        bottom_right = (width * 3 // 4, height * 3 // 4)
        box_area = (upper_left[0], upper_left[1], bottom_right[0], bottom_right[1])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # resize the frame | small frame optimise the run
        # frame = cv2.resize(frame, (frame_wid, frame_hyt))

        # Predict on image
        # Device parameter가 GPU를 잡는것인지 확인.
        detect_params = model.predict(source=[frame], conf=0.45, save=False, device=0)

        # Convert tensor array to numpy
        DP = detect_params[0].cpu().numpy()
        print(DP)

        if len(DP) != 0:

            for i in range(len(detect_params[0])):
                print(i)

                boxes = detect_params[0].boxes
                box = boxes[i]
                clsID = box.cls.cpu().numpy()[0]
                conf = box.conf.cpu().numpy()[0]
                bb = box.xyxy.cpu().numpy()[0]
                frame_id += 1

                target = (bb[0], bb[1], bb[2], bb[3])
                #position_finder(box_area, target)
                cv2.rectangle(
                    frame,
                    (int(bb[0]), int(bb[1])),
                    (int(bb[2]), int(bb[3])),
                    colors[0],
                    3,
                )

                cv2.putText(
                    frame,
                    classes[0] + " " + str(round(conf, 3)) + "%",
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
        cv2.imshow('Image2', frame)

        # Terminate run when "0" pressed
        if cv2.waitKey(1) == ord('q'):
            break

def drone_tracking():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        height, width, channels = frame.shape
        upper_left = (width // 4, height // 4)
        bottom_right = (width * 3 // 4, height * 3 // 4)
        box_area = (upper_left[0], upper_left[1], bottom_right[0], bottom_right[1])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # resize the frame | small frame optimise the run
        # frame = cv2.resize(frame, (frame_wid, frame_hyt))

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
                clsID = box.cls.cpu().numpy()[0]
                conf = box.conf.cpu().numpy()[0]
                bb = box.xyxy.cpu().numpy()[0]
                frame_id += 1

                target = (bb[0], bb[1], bb[2], bb[3])
                position_finder(box_area, target)
            
        time.sleep(1)

        # Terminate run when "0" pressed
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    IP="192.168.0.2"   # Camera IP address
    PORT=80           # Port
    USER="admin"         # Username
    PASS="idcitic405"        # Password

    def position_finder(box, target):
        print("box: ", box)
        print("target: ", target)
        if box[0] > target[0] :
            ptz.move_left()
        elif box[1] > target[1]:
            ptz.move_up()
        elif box[2] < target[2]:
            ptz.move_right()
        elif box[3] < target[3]:
            ptz.move_down()

    model = YOLO("band.pt", "v8")

    my_file = open("classes.txt", "r")
    data = my_file.read()
    classes = data.split("\n")
    my_file.close()

    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading camera
    video = streamer.ptz_streamer(IP,PORT,USER,PASS)
    cap = cv2.VideoCapture(video.uri)
    pTime = 0
    ptz = controller(IP,PORT,USER,PASS)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    frame = None



    t1 = threading.Thread(target=drone_detection)  
    t2 = threading.Thread(target=drone_tracking)  

    t1.daemon = True
    t2.daemon = True

    time.sleep(5)

    t1.start()
    t2.start()

    while True:
        #print('press Ctrl+C to quit:\n')
        input()
