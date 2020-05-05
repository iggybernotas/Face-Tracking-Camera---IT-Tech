import cv2, serial
from FeatureClasses import Face, Eye


ser = serial.Serial(timeout=0.05)
ser.baudrate = 115200
ser.port = 'COM4'
ser.open()

# Create Feature objects
face = Face()
eye = Eye()

face.set_cascade()
eye.set_cascade()

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX


def readresponse():
    b = bytearray(b"                   ");
    ser.readinto(b)
    print(b.decode())


# Default/Starting Position
PanPosition = 90
TiltPosition = 70

# Camera is 620px x 480px so this is the middle of each X and Y
middleXCam = 310
middleYCam = 240

while True:
    # Frame by frame capture
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.get_detected(gray)
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        gray = gray[y:y+h, x:x+w]
        color = frame[y:y+h, x:x+w]
        eyes = eye.get_detected(gray)
        for (ex, ey, ew, eh) in eyes:
            if len(eyes) > 2:
                break
            else:
                cv2.rectangle(color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                cv2.putText(frame, 'Eyes Found', (520, 470), font, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    if len(faces) > 0:  # If a face is detected
        cv2.putText(frame, 'Face Found', (520, 445), font, 0.6, (255, 0, 0), 2, cv2.LINE_AA)
        middleX = faces[0][2] / 2 + faces[0][0]  # Width divided by 2 +
        middleY = faces[0][3] / 2 + faces[0][1]
        middleXDiff = (middleX - middleXCam)
        middleYDiff = (middleY - middleYCam)
        #print(middleXDiff)
        #print(middleYDiff)
        if abs(middleXDiff) > 20:   # If the difference between the middle of the camera and the middle of the screen
            PanPosition -= (middleXDiff / 37)   # Pan Position is in degrees
            #print(PanPosition)

        if abs(middleYDiff) > 20:
            TiltPosition += (middleYDiff / 47)
            #print(PanPosition)

    ser.write(bytearray([49, int(PanPosition)]))
    ser.write(bytearray([48, int(TiltPosition)]))
    ser.write(bytearray([50]))    # Comment for smoother running/no 2 way communication (causes a small amount of camera lag)
    # Display the resulting frame

    cv2.imshow('Camera Project Group 1', frame)

    readresponse()    # Comment for smoother running/no 2 way communication (causes a small amount of camera lag)

    # Press Q to Escape Program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release when done/loop broken with Q

cap.release()
cv2.destroyAllWindows()