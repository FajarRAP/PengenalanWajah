import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" : "https://basisdatapengenalanwajah-default-rtdb.firebaseio.com/"
    })

ref = db.reference("Orang")

data = {
    "191102":
        {
            "nama" : "Fajar Riansyah Aryda Putra",
            "nim" : "2100018165",
            "prodi" : "Informatika",
            "smt" : 4,
            "terakhir_hadir" : "14-7-2023 16:25:13" 
        },
    "090403":
        {
            "nama" : "Dimas Thaqif Attaulah",
            "nim" : "2100018157",
            "prodi" : "Informatika",
            "smt" : 4,
            "terakhir_hadir" : "12-7-2023 06:15:33" 
        },
    "999999":
        {
            "nama" : "Gagah Aryo Wijoseno",
            "nim" : "2100018152",
            "prodi" : "Informatika",
            "smt" : 4,
            "terakhir_hadir" : "17-8-2023 17:05:37" 
        },
}

for key, value in data.items():
    ref.child(key).set(value)