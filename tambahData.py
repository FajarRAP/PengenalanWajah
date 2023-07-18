import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    "databaseURL" : "https://basisdatapengenalanwajah-default-rtdb.firebaseio.com/"
    })

ref = db.reference("Orang")

data = {
    "2100018165":
        {
            "nama" : "Fajar Riansyah Aryda Putra",
            "prodi" : "Informatika",
            "ipk" : 3.80,
            "jenis_kelamin" : "Male",
            "angkatan" : 2021,
            "smt" : 4,
            "terakhir_hadir" : "14-7-2023 16:25:13" 
        },
    "2100018157":
        {
            "nama" : "Dimas Thaqif Attaulah",
            "prodi" : "Informatika",
            "ipk" : 3.52,
            "jenis_kelamin" : "Male",
            "angkatan" : 2021,
            "smt" : 4,
            "terakhir_hadir" : "12-7-2023 06:15:33" 
        },
    "2100018152":
        {
            "nama" : "Gagah Aryo Wijoseno",
            "prodi" : "Informatika",
            "ipk" : 3.57,
            "jenis_kelamin" : "Male",
            "angkatan" : 2021,
            "smt" : 4,
            "terakhir_hadir" : "17-8-2023 17:05:37" 
        },
    "2100018170":
        {
            "nama" : "Oktaria Purnamasari",
            "prodi" : "Informatika",
            "ipk" : 3.93,
            "jenis_kelamin" : "Female",
            "angkatan" : 2021,
            "smt" : 4,
            "terakhir_hadir" : "14-7-2023 23:46:44" 
        },
}

for key, value in data.items():
    ref.child(key).set(value)