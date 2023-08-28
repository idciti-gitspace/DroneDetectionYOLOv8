import cv2
import numpy as np
import time
import pyautogui as gui
from ultralytics import YOLO

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

# Loading camera
cap = cv2.VideoCapture("rtsp://admin:idcitic405@192.168.0.2:554/0/onvif/profile1/media.smp")

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

    # resize the frame | small frame optimise the run
    # frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
    detect_params = model.predict(source=[frame], conf=0.25, save=False)

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
                classes[int(clsID)] + " " + str(round(conf, 3)),
                (int(bb[0]), int(bb[1]) - 10),
                font,
                1,
                (255,255,255),
                2,
            )

    # Display the resulting frame
    cv2.imshow('ObjectDetection', frame)

    # Terminate run when "0" pressed
    if cv2.waitKey(1) == ord('q'):
        break

# while True:
#     pic = gui.screenshot() # gui.screenshot(region=(0,0,2048,1080))
#     img = np.array(pic)
#     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
#     # _, frame = cap.read()
#     frame = img
#     frame_id += 1
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # frame = np.stack((frame,)*3, axis=-1)
#     height, width, channel = frame.shape

#     # Detecting objects
#     blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

#     net.setInput(blob)
#     # outs = net.forward(output_layers)

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
#             cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#             cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
#             cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, (255,255,255), 3)
#             print(0,x,y,w,h)
#     if "cabinet" in classes:
#         print("cabinet found")
#     elapsed_time = time.time() - starting_time
#     fps = frame_id / elapsed_time
#     # cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)
#     cv2.imshow("Image2", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

cap.release()
cv2.destroyAllWindows()