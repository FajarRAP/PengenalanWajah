import cv2
import os
import pickle
import face_recognition
import numpy
import cvzone

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
print(nama_orang)

while True:
    sukses, img = cap.read()
    gambar_latarbelakang[162:162 + 480, 55:55 + 640] = img # posisikan kamera webcam ke tengah background
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
            
    cv2.imshow("Pengenalan Wajah", gambar_latarbelakang)
    cv2.waitKey(1)
