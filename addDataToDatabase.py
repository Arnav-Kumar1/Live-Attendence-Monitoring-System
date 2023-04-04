import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://live-attendance-tracker-default-rtdb.firebaseio.com/"})

ref = db.reference('Students')  # this is the oath

data = {
    "52145":
    {
        "name": "Aman Kumar",
        "major": "Data Science",
        "starting year": 2016,
        "total attendance" : 100,
        "last attendance time": "2023-04-04 00:54:34",
        "GPA": 8.9,
        "standing": 3,
        "ID" : 52145,
        "year": 2023

    },

    "65895":

    {
        "name": "Amber heard",
        "major": "Acting",
        "starting year": 2005,
        "total attendance" : 95,
        "last attendance time": "2023-04-04 00:54:34",
        "GPA" : 7.9,
        "standing": 30,
        "ID" : 65895,
        "year": 2023

    },

    "99866":

        {
            "name": "Elon Musk",
            "major": "BS in Physics",
            "starting year": 2004,
            "total attendance" : 9,
            "last attendance time": "2023-04-04 00:54:34",
            "GPA": 10.0,
            "standing": 1,
            "ID" : 99866,
            "year": 2023

        }
}

for k, v in data.items():
    ref.child(k).set(v)
