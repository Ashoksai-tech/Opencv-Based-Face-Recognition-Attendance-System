import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

# Initialize Firebase app with credentials and connect to Realtime Database and Cloud Storage
cred = credentials.Certificate("C:/Users/aasho/OneDrive/Desktop/image recognition project/src/serviceaccounts.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://real-time-face-attendanc-142ca-default-rtdb.firebaseio.com/",
    'storageBucket': "real-time-face-attendanc-142ca.appspot.com"
})
bucket = storage.bucket()

# Set webcam properties (width: 640, height: 480)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Load the background image and mode images (UI elements)
imgbackground = cv2.imread("Resources/background.png")

# Import mode images into a list
foldermodespath = 'Resources/Modes'
modepathlist = os.listdir(foldermodespath)
imgmodlist = []
for path in modepathlist:
    imgmodlist.append(cv2.imread(os.path.join(foldermodespath, path)))

# Load the face encodings and corresponding IDs from file
print("loading encode file...")
file = open('encode.p', 'rb')
encodelistknownwithids = pickle.load(file)
file.close()
encodelistknown, stids = encodelistknownwithids  # Separate encodings and IDs
print("encode file loaded")

# Initialize variables for tracking attendance state
modetype = 0  # Current mode type for UI
counter = 0   # Counter for managing UI transitions
id = -1       # Current detected student's ID
imgstudent = []  # Student's profile image

# Start capturing webcam video
while True:
    success, img = cap.read()

    # Resize the webcam image for faster processing
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Convert the resized image from BGR to RGB format
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    # Detect faces and generate encodings in the current frame
    facecurframe = face_recognition.face_locations(imgs)
    encodecurframe = face_recognition.face_encodings(imgs, facecurframe)

    # Place the webcam image onto the background image at specific coordinates
    imgbackground[162:162+480, 55:55+640] = img
    # Place the current mode image on the UI
    imgbackground[44:44+633, 808:808+414] = imgmodlist[modetype]

    # If faces are detected in the current frame, process each detected face
    if facecurframe:
        for encodeface, facelocation in zip(encodecurframe, facecurframe):
            # Compare detected face encodings with known encodings
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)

            # Find the index of the closest matching known face
            matchindex = np.argmin(facedis)

            # If a known face is detected
            if matches[matchindex]:
                print("known face detected")
                print(stids[matchindex])

                # Get the face coordinates, resize to original size, and draw a bounding box
                y1, x2, y2, x1 = facelocation
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgbackground = cvzone.cornerRect(imgbackground, bbox, rt=0)

                # Retrieve the student ID
                id = stids[matchindex]
                print(id)

                # Change mode to show student info and initialize counter
                if counter == 0:
                    counter = 1
                    modetype = 1

        # If a face match has been found, process attendance and student info
        if counter != 0:
            if counter == 1:
                # Fetch student data from Firebase database using student ID
                studentinfo = db.reference(f'Students/{id}').get()
                print(studentinfo)

                # Retrieve the student's image from Firebase Storage
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgstudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Check the time since the last attendance was marked
                datetimeobject = datetime.strptime(studentinfo['last attendance time'], "%Y-%m-%d %H:%M:%S")
                seconds = (datetime.now() - datetimeobject).total_seconds()
                print(seconds)
                
                # Update attendance if more than 24 hours have passed
                if seconds > 86400:
                    ref = db.reference(f'Students/{id}')
                    studentinfo['total attendance'] += 1
                    ref.child('total attendance').set(studentinfo['total attendance'])
                    ref.child('last attendance time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    # If attendance was marked in the last 24 hours, set mode to "already marked"
                    modetype = 3
                    counter = 2
                    imgbackground[44:44 + 633, 808:808 + 414] = imgmodlist[modetype]

            # Update UI to show student information
            if modetype != 3:
                if 10 < counter < 20:
                    modetype = 2

                imgbackground[44:44 + 633, 808:808 + 414] = imgmodlist[modetype]

                # Display student's information on the UI
                if counter <= 10:
                    cv2.putText(imgbackground, str(studentinfo['total attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

                    cv2.putText(imgbackground, str(studentinfo['Major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    
                    cv2.putText(imgbackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    
                    cv2.putText(imgbackground, str(studentinfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    cv2.putText(imgbackground, str(studentinfo['Year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    cv2.putText(imgbackground, str(studentinfo['starting year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    # Center the student's name on the UI
                    (w, h), _ = cv2.getTextSize(studentinfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgbackground, str(studentinfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    # Display the student's profile picture
                    imgbackground[175:175 + 216, 909:909 + 216] = imgstudent

            # Increment the counter and reset once it reaches 20
            counter += 1
            if counter >= 20:
                counter = 0
                modetype = 0
                studentinfo = []
                imgstudent = []
                imgbackground[175:175 + 216, 909:909 + 216] = imgstudent
    else:
        # Reset to default mode if no face is detected
        modetype = 0
        counter = 0

    # Display the updated UI
    cv2.imshow("Face Attendance", imgbackground)
    cv2.waitKey(1)
