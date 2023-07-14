import cv2
import face_recognition
import pickle
import os


lokasi_gambar_wajah = os.listdir("images") # 1. tembak lokasi gambar
list_gambar_wajah = [] # 2. simpan nanti di array ini
nama_orang = [] # 3. untuk menyimpan nama file foto (nama orang)
for lokasi in lokasi_gambar_wajah: # 3. Iterasi setiap elemen di lokasi_gambar_wajah dan masukan ke list_gambar_wajah
    list_gambar_wajah.append(cv2.imread(os.path.join("images", lokasi))) 
    nama_orang.append(os.path.splitext(lokasi)[0]) # 5. fungsi untuk memisahkan ekstensi dari nama file

def encodeGambar(list_gambar_wajah): # 1. membuat fungsi untuk encode agar bisa dibaca oleh face recognition
    hasil_encode = [] # 2. untuk simpan hasil encode
    for gambar in list_gambar_wajah: # 3. iterasi tiap parameter untuk di encode
        gambar = cv2.cvtColor(gambar, cv2.COLOR_BGR2RGB) # 4. konversi format warna bgr(opencv) ke rgb(face_recognition) 
        hasil_encode.append(face_recognition.face_encodings(gambar)[0]) # 5. isi array
    return hasil_encode

print("Encode dimulai ...")
gambar_dikenali = encodeGambar(list_gambar_wajah) # 1. simpan hasil encode
gambar_dikenali_nama = [gambar_dikenali, nama_orang] # 2. simpan gambar_dikenali dengan nama
print("Encode selesai")

file = open("HasilEncode.p", "wb")
pickle.dump(gambar_dikenali_nama, file)
file.close()
