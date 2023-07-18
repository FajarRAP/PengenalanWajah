import cv2
import os
import pickle
import face_recognition
import numpy
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL" : "https://basisdatapengenalanwajah-default-rtdb.firebaseio.com/",
    "storageBucket" : "basisdatapengenalanwajah.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0) # argumen 0 untuk webcam bawaan
cap.set(3, 848)
cap.set(4, 480)

gambar_latarbelakang = cv2.imread("Resources/background.png") # set gambar latar belakang
lokasi_gambar = os.listdir("Resources/Modes") # set path parent dari gambar
list_gambar_mode = [] # array untuk menyimpan nama file gambar mode beserta ekstensinya

for lokasi in lokasi_gambar: # iterasi untuk nambahin elemen ke array dengan konkatenasi string
    list_gambar_mode.append(cv2.imread(os.path.join("Resources/Modes", lokasi)))

# muat hasil encode
file = open("HasilEncode.p", "rb")
gambar_dikenali_nama = pickle.load(file)
file.close()
gambar_dikenali, nama_orang = gambar_dikenali_nama
# print(nama_orang)

counter = 0
index_mode_latar_belakang = 0

while True:
    sukses, img = cap.read()
    gambar_latarbelakang[162:162 + 480, 55:55 + 640] = img # posisikan kamera webcam ke tengah background
    gambar_latarbelakang[44:44 + 633, 808:808 + 414] = list_gambar_mode[index_mode_latar_belakang]
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    
    wajah_dari_webcam = face_recognition.face_locations(img_small)
    encode_wajah_dari_webcam = face_recognition.face_encodings(img_small, wajah_dari_webcam)
    
    for encode, wajah in zip(encode_wajah_dari_webcam, wajah_dari_webcam):
        cocok = face_recognition.compare_faces(gambar_dikenali, encode) # dicocokan antara gambar dari webcam dengan hasil muat tadi
        jarak = face_recognition.face_distance(gambar_dikenali, encode) # maksud jarak di sini seberapa persis antara gambar webcam dengan hasil muat tadi
        index_yang_cocok = numpy.argmin(jarak)
        
        
        if cocok[index_yang_cocok]:
            y1, x2, y2, x1 = wajah
            x1, y1, x2, y2 = x1 * 4, y1 * 4, x2 *4, y2 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            cvzone.cornerRect(gambar_latarbelakang, bbox, rt = 0)
            
            nim_yang_cocok = nama_orang[index_yang_cocok]
            
            if counter == 0:
                counter = 1
                index_mode_latar_belakang = 1
                
    if counter != 0:
        if counter == 1:
            data_orang = db.reference(f'Orang/{nim_yang_cocok}').get()
            blob = bucket.get_blob(f'images/{nim_yang_cocok}.png')
            gambar_format_opencv = numpy.frombuffer(blob.download_as_string(), numpy.uint8)
            gambar_yang_cocok = cv2.imdecode(gambar_format_opencv, cv2.COLOR_BGRA2BGR)
            # print(data_orang)
        cv2.putText(gambar_latarbelakang, str(data_orang['ipk']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1) # tampilin semester
        cv2.putText(gambar_latarbelakang, str(nim_yang_cocok), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1) # tampilin nim
        cv2.putText(gambar_latarbelakang, str(data_orang['prodi']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1) # tampilin prodi
        cv2.putText(gambar_latarbelakang, str(data_orang['jenis_kelamin']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1) # tampilin jenis kelamin
        cv2.putText(gambar_latarbelakang, str(data_orang['smt']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1) # tampilin semester
        cv2.putText(gambar_latarbelakang, str(data_orang['angkatan']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1) # tampilin angkatan
        
        # posisi x, y dari kiri ke kanan
        # (910, 1025, 1125), 625 
        
        (lebar, tinggi), _ = cv2.getTextSize(data_orang['nama'], cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
        offset = (414 - lebar) // 2
        cv2.putText(gambar_latarbelakang, str(data_orang['nama']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 0.7, (50, 50, 50), 1) # tampilin nama
        gambar_latarbelakang[175:175 + 209, 909:909 + 216] = gambar_yang_cocok
        counter = counter + 1
            
    cv2.imshow("Pengenalan Wajah", gambar_latarbelakang)
    cv2.waitKey(1)
