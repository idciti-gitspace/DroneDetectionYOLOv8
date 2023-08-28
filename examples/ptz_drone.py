import ptz_streaming as streamer
import cv2
from ultralytics import YOLO
import numpy as np
import time
import csv
import os
from ptz_control_module import ptz_controller  as ptz_c


#Camera configuration
IP="192.168.0.2"   # Camera IP address
PORT=80           # Port
USER="admin"         # Username
PASS="idcitic405"        # Password

# Load Yolo
# net = cv2.dnn.readNet("obj_detection/yolov4-custom_5000.weights", "obj_detection/yolov4-obj.cfg")
model = YOLO("best.pt", "v8")

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
video = streamer.ptz_streamer(IP,PORT,USER,PASS)
cap = cv2.VideoCapture(video.uri)
font = cv2.FONT_HERSHEY_PLAIN


ptz = ptz_c(IP,PORT,USER,PASS)

# header = ['time', 'frame_id', 'confidence' ,'center_x','center_y','detection_width','detection_height']
# cwd = os.getcwd()
# path = cwd + '/results/'
def position_finder(box, target):
    print("box: ", box)
    print("target: ", target)
    if box[0] > target[0] :
        # val = 'l'
        # val = val.encode('utf-8')
        # ser.write(val)
        ptz.move_left()
        
        # val = 'b'
        # val = val.encode('utf-8')
        # ser.write(val)

    elif box[1] > target[1]:
        # val = 'u'
        # val = val.encode('utf-8')
        # ser.write(val)
        ptz.move_up()

        # val = 'b'
        # val = val.encode('utf-8')
        # ser.write(val)
        
    elif box[2] < target[2]:
        # val = 'r'
        # val = val.encode('utf-8')
        # ser.write(val)
        ptz.move_right()

        # val = 'b'
        # val = val.encode('utf-8')
        # ser.write(val)

    elif box[3] < target[3]:
        # val = 'd'
        # val = val.encode('utf-8')
        # ser.write(val)
        ptz.move_down()
        
        # val = 'b'
        # val = val.encode('utf-8')
        # ser.write(val)
    
    #time.sleep(0.7)
    # val = 's'
    # val = val.encode('utf-8')    
    # ser.write(val)

# cap = cv2.VideoCapture(cap)

# with open(path + '{}.csv'.format(time.strftime('%Y-%m-%d-%H-%M-%S')), 'w', newline='') as f:
#     writer = csv.writer(f, delimiter=',')
#     writer.writerow(header)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

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

    # Display the resulting frame
    cv2.imshow("Image2", frame)

    # Terminate run when "0" pressed
    if cv2.waitKey(1) == ord('q'):
        break
# while True:
#     frame_id = 0
#     ret, frame = cap.read()
#     if ret == 1:
#         height, width, channels = frame.shape
#         # Detecting objects
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         outs = net.forward(output_layers)
#         # Showing informations on the screen
#         class_ids = []
#         confidences = []
#         boxes = []
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:
#                     # Object detected
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     # Rectangle coordinates
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#         for i in range(len(boxes)):
#             if i in indexes:
#                 x, y, w, h = boxes[i]
#                 label = str(classes[class_ids[i]])
#                 confidence = confidences[i]
#                 color = colors[class_ids[i]]
#                 target = (x, y,  x+w, y+h)

#                 cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
#                 cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
#                 # data = time.strftime('%Y-%m-%d %H:%M:%S'),frame_id, str(round(confidence, 2)), x,y,w,h
#                 # print(data)
#                 # writer.writerow(data)
#         if "Drone" in classes:
#             print("Drone not found")
#         cv2.imshow('frame',frame)
#     else:
#         print ("no video")
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
cap.release()
cv2.destroyAllWindows()
# f.close()
