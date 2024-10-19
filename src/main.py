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



cred = credentials.Certificate("C:/Users/aasho/OneDrive/Desktop/image recognition project/src/serviceaccounts.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://real-time-face-attendanc-142ca-default-rtdb.firebaseio.com/",
    'storageBucket':"real-time-face-attendanc-142ca.appspot.com"
})

# set the width and height of frame
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


#importing the mode images into list

imgbackground = cv2.imread("Resources/background.png")

foldermodespath = 'Resources/Modes'
modepathlist = os.listdir(foldermodespath)
imgmodlist = []
for path in modepathlist:
    imgmodlist.append(cv2.imread(os.path.join(foldermodespath,path)))

# print(len(imgmodlist))

#load the encoding file

print("loading encode file...")
file = open('encode.p','rb')
encodelistknownwithids = pickle.load(file)
file.close()
encodelistknown,stids = encodelistknownwithids
#print(stids)
print("encode file loaded")

modetype = 0
counter = 0
id = -1








#display the web cam
while True:
    sucess,img = cap.read()

    #squeeze the image
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    #convert bgr to rgb format
    imgs = img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    facecurframe = face_recognition.face_locations(imgs)
    encodecurframe = face_recognition.face_encodings(imgs,facecurframe)

    # add webcam to background
    imgbackground[162:162+480,55:55+640] = img
    imgbackground[44:44+633,808:808+414] = imgmodlist[0]


#check for generated encoding whether there are any matches
    for encodeface,facelocation in zip(encodecurframe,facecurframe):
        matches = face_recognition.compare_faces(encodelistknown,encodeface)
        facedis = face_recognition.face_distance(encodelistknown,encodeface)
        # print("matches",matches)
        # print("facedis",facedis)


        matchindex = np.argmin(facedis)
        #print("Match Index",matchindex)


        if matches[matchindex]:
            print("known face detected")
            print(stids[matchindex])
            y1,x2,y2,x1 = facelocation
            y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1,162+y1,x2-x1,y2-y1
            imgbackground = cvzone.cornerRect(imgbackground,bbox,rt=0)
            id = stids[matchindex]
            print(id)

            if counter==0:
                counter=1
                modetype=1


    if counter!=0:
        if counter ==1:
            studentinfo = db.reference(f'Students/{id}').get()
            print(studentinfo)







    #cv2.imshow("Display",img)
    cv2.imshow("Face Attendance",imgbackground)
    cv2.waitKey(1)