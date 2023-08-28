import ptz_video_stream_module as streamer
import cv2
import time
from ptz_control_module import ptz_controller  as controller
from ultralytics import YOLO
import numpy as np

#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

# # Load Yolo
# net = cv2.dnn.readNet("obj_detection/yolov4-custom_5000.weights", "obj_detection/yolov4-obj.cfg")
# classes = []
# with open("obj_detection/obj.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# colors = np.random.uniform(0, 255, size=(len(classes), 3))
# video = streamer.ptz_streamer(IP,PORT,USER,PASS)
# cap = cv2.VideoCapture(video.uri)
# pTime = 0
# ptz = controller(IP,PORT,USER,PASS)

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

# Load Yolo
# net = cv2.dnn.readNet("obj_detection/yolov4-custom_5000.weights", "obj_detection/yolov4-obj.cfg")
model = YOLO("band.pt", "v8")

# classes = []
# with open("obj_detection/obj.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]
my_file = open("classes.txt", "r")
data = my_file.read()
classes = data.split("\n")
my_file.close()


# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
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

            cv2. rectangle(
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
        cv2.imshow('frame', frame)

    else:
        print("no video")

    # Terminate run when "0" pressed
    if cv2.waitKey(1) == ord('q'):
        break

# while True:
    # ret, frame = cap.read()
    # if ret == 1:
    #     #frame = cv2.rotate(frame, cv2.ROTATE_180)
    #     height, width, channels = frame.shape
    #     upper_left = (width//4, height//4)
    #     bottom_right = (width*3//4, height*3//4)
    #     box_area = (upper_left[0],upper_left[1], bottom_right[0], bottom_right[1])
    #     cTime = time.time()
    #     fps = 1/(cTime - pTime)
    #     pTime = cTime
    #     # Detecting objects
    #     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    #     net.setInput(blob)
    #     outs = net.forward(output_layers)
    #     # Showing informations on the screen
    #     class_ids = []
    #     confidences = []
    #     boxes = []
    #     for out in outs:
    #         for detection in out:
    #             scores = detection[5:]
    #             class_id = np.argmax(scores)
    #             confidence = scores[class_id]
    #             if confidence > 0.3:
    #                 # Object detected
    #                 center_x = int(detection[0] * width)
    #                 center_y = int(detection[1] * height)
    #                 w = int(detection[2] * width)
    #                 h = int(detection[3] * height)
    #                 # Rectangle coordinates
    #                 x = int(center_x - w / 2)
    #                 y = int(center_y - h / 2)
    #                 boxes.append([x, y, w, h])
    #                 confidences.append(float(confidence))
    #                 class_ids.append(class_id)
    #     indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
    #     for i in range(len(boxes)):
    #         if i in indexes:
    #             x, y, w, h = boxes[i]
    #             label = str(classes[class_ids[i]])
    #             confidence = confidences[i]
    #             color = colors[class_ids[i]]
    #             target = (x, y,  x+w, y+h)
    #             position_finder(box_area, target) 
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    #             cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
    #             cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    #     if "drone" in classes:
    #         print("drone found")
    #     cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN,3,(0,255,0), 2)
    #     cv2.rectangle(frame, upper_left, bottom_right, (0, 255, 0), thickness=1)
    #     cv2.imshow('frame',frame)
    # else:
    #     print ("no video")
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
