import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("C:/Users/aasho/OneDrive/Desktop/image recognition project/src/serviceaccounts.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://real-time-face-attendanc-142ca-default-rtdb.firebaseio.com/",
    'storageBucket':"real-time-face-attendanc-142ca.appspot.com"
})
   


#importing the student images 

folderpath = 'images'
imgpathlist = os.listdir(folderpath)
print(imgpathlist)
imglist = []
stids = []
for path in imgpathlist:
    imglist.append(cv2.imread(os.path.join(folderpath,path)))
    # print(os.path.splitext(path)[0])
    stids.append(os.path.splitext(path)[0])



    filename =  f'{folderpath}/{path}'
    bucket  = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
 


# func to generate encode and split out list 

def encodings(imglist):
    encodelist = []
    for img in imglist:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #convert bgr to rgb beacuse face recognition only accepts rgb but in opencv it is bgr format
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist

print("encoded started")
encodelistknown = encodings(imglist)
encodelistknownwithids = [encodelistknown,stids]
 
print("fully encoded")

file = open("encode.p",'wb')
pickle.dump(encodelistknownwithids,file)
file.close()
print('file saved')