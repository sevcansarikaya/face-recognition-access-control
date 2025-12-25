import cv2
import mediapipe as mp
import sqlite3
import numpy as np
import datetime
import os
import shutil

# MediaPipe Yapılandırması
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.3)

DATABASE_NAME = "access_control.db"
DATASET_PATH = "yuz_verileri" # Fotoğrafların tutulacağı ana klasör

if not os.path.exists(DATASET_PATH):
    os.makedirs(DATASET_PATH)

def register_new_user(ad_soyad, bolum, yetki, image_path):
    """Kullanıcıyı kaydeder ve fotoğrafı klasörüne kopyalar."""
    try:
        # Kullanıcıya özel klasör oluştur (Örn: yuz_verileri/Sevcan)
        user_dir = os.path.join(DATASET_PATH, ad_soyad)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Fotoğrafı yeni isimlendirerek kopyala (zaman damgasıyla çakışmayı önle)
        dosya_adi = f"{datetime.datetime.now().strftime('%Y%H%M%S')}.jpg"
        hedef_yol = os.path.join(user_dir, dosya_adi)
        shutil.copy(image_path, hedef_yol)

        # Veritabanına sadece bir kez ana kaydı yap (zaten varsa yapma)
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM KULLANICILAR WHERE ad_soyad = ?", (ad_soyad,))
        if not cursor.fetchone():
            kayit_tarihi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                INSERT INTO KULLANICILAR (ad_soyad, bolum, foto_yolu, yetki_seviyesi, kayit_tarihi)
                VALUES (?, ?, ?, ?, ?)
            """, (ad_soyad, bolum, user_dir, yetki, kayit_tarihi))
        
        conn.commit()
        conn.close()
        return True, f"{ad_soyad} için yeni fotoğraf eklendi."
    except Exception as e:
        return False, f"Hata: {str(e)}"

def taranan_yuzu_bul(frame):
    """Kameradaki yüzü klasördeki tüm fotoğraflarla kıyaslar."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        try:
            # Kameradaki yüzü hazırla
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = gray_frame.shape
            face_zone = cv2.resize(gray_frame[h//6:5*h//6, w//6:5*w//6], (128, 128))
            
            best_overall_score = -1
            recognized_name = "Bilinmeyen Kişi"

            # Tüm kullanıcı klasörlerini tara
            for user_name in os.listdir(DATASET_PATH):
                user_dir = os.path.join(DATASET_PATH, user_name)
                if os.path.isdir(user_dir):
                    # Klasördeki her fotoğrafı tek tek dene
                    for img_name in os.listdir(user_dir):
                        img_path = os.path.join(user_dir, img_name)
                        kayitli_img = cv2.imread(img_path, 0)
                        if kayitli_img is None: continue
                        
                        kayitli_img = cv2.resize(kayitli_img, (128, 128))
                        res = cv2.matchTemplate(face_zone, kayitli_img, cv2.TM_CCOEFF_NORMED)
                        score = res[0][0]
                        
                        if score > best_overall_score:
                            best_overall_score = score
                            recognized_name = user_name

            # Eşik değerini biraz daha esnetebiliriz (0.07 gibi)
            if best_overall_score > 0.07:
                return recognized_name, results.detections[0]
            else:
                return "Bilinmeyen Kişi", results.detections[0]
                
        except Exception as e:
            print(f"Hata: {e}")
            return "Hata", results.detections[0]
            
    return None, None

def log_kaydet(isim, durum="Giriş Başarılı"):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO GIRIS_KAYITLARI (tarih_saat, durum, giren_kisi_bilgisi) VALUES (?, ?, ?)", (zaman, durum, isim))
        conn.commit(); conn.close()
    except: pass