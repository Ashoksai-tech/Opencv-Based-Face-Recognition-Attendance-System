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



cred = credentials.Certificate("C:/Users/aasho/OneDrive/Desktop/image recognition project/src/serviceaccounts.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://real-time-face-attendanc-142ca-default-rtdb.firebaseio.com/",
    'storageBucket':"real-time-face-attendanc-142ca.appspot.com"
})
bucket = storage.bucket()

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
imgstudent = []








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
    imgbackground[44:44+633,808:808+414] = imgmodlist[modetype]


#check for generated encoding whether there are any matches
    if facecurframe:
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
                # get the data
                studentinfo = db.reference(f'Students/{id}').get()
                print(studentinfo)
                
                #get the image from storage

                blob = bucket.get_blob(f'images\{id}.png')
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgstudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

                #update data of attendance
                datetimeobject = datetime.strptime(studentinfo['last attendance time'],
                                            "%Y-%m-%d %H:%M:%S")
                seconds = (datetime.now() - datetimeobject).total_seconds()
                print(seconds)
                if seconds > 86400:
                    ref =db.reference(f'Students/{id}')
                    studentinfo['total attendance'] +=1
                    ref.child('total attendance').set(studentinfo['total attendance'])
                    ref.child('last attendance time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modetype = 3
                    counter = 2
                    imgbackground[44:44 + 633, 808:808 + 414] = imgmodlist[modetype]



            if modetype!=3:
                if 10<counter<20:
                    modetype=2

                imgbackground[44:44 + 633, 808:808 + 414] = imgmodlist[modetype]

                if counter<=10:

                    cv2.putText(imgbackground,str(studentinfo['total attendance']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    
                    cv2.putText(imgbackground,str(studentinfo['Major']),(1006,550),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgbackground,str(id),(1006,493),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgbackground,str(studentinfo['standing']),(910,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgbackground,str(studentinfo['Year']),(1025,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgbackground,str(studentinfo['starting year']),(1125,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    
                    (w, h), _ = cv2.getTextSize(studentinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset = (414-w)//2
                    

                    cv2.putText(imgbackground,str(studentinfo['name']),(808+offset,445),
                                cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)
                    

                    imgbackground[175:175+216,909:909+216] = imgstudent


            counter +=1

            if counter>=20:
                counter = 0
                modetype = 0
                studentinfo = []
                imgstudent = []
                imgbackground[175:175+216,909:909+216] = imgstudent

    
    else:
        modetype = 0
        counter = 0
        








    #cv2.imshow("Display",img)
    cv2.imshow("Face Attendance",imgbackground)
    cv2.waitKey(1)