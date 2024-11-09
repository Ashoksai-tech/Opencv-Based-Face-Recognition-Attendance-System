import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:/Users/aasho/OneDrive/Desktop/face recognition attendance system/src/serviceaccounts.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://real-time-face-attendanc-142ca-default-rtdb.firebaseio.com/"
})



ref = db.reference('Students')

data = {
    "852741":
    {
        "name": "emly blunt",
        "Major":"Data Science",
        "starting year":2021,
        "total attendance":6,
        "standing":"G",
        "Year":3,
        "last attendance time":"2022-11-25 00:54:34"
        
    },
        "963852":
    {
        "name": "Elon Musk",
        "Major":"Machine Learning",
        "starting year":2019,
        "total attendance":12,
        "standing":"B",
        "Year":3,
        "last attendance time":"2023-11-25 00:54:34"
        
    }
}

for key,value in data.items():
    ref.child(key).set(value)