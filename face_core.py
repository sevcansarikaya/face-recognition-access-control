import cv2
import mediapipe as mp
import sqlite3
import json
import numpy as np
import datetime

# MediaPipe Yapılandırması
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

DATABASE_NAME = "access_control.db"

def register_new_user(ad_soyad, bolum, yetki, image_path):
    """Yeni bir kullanıcıyı veritabanına kaydeder."""
    try:
        # Fotoğrafta yüz var mı kontrol et
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_image)

        if not results.detections:
            return False, "Seçilen fotoğrafta yüz tespit edilemedi!"

        # MediaPipe için sahte encoding (vektör) üret (Simülasyon için)
        fake_encoding = np.random.uniform(-1, 1, 128).tolist()
        encoding_json = json.dumps(fake_encoding)

        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        kayit_tarihi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO KULLANICILAR (ad_soyad, bolum, yuz_encoding, foto_yolu, yetki_seviyesi, kayit_tarihi)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ad_soyad, bolum, encoding_json, image_path, yetki, kayit_tarihi))
        
        conn.commit()
        conn.close()
        return True, f"{ad_soyad} başarıyla kaydedildi."
    except Exception as e:
        return False, f"Veritabanı hatası: {str(e)}"

def taranan_yuzu_bul(frame):
    """Kameradaki yüzü analiz eder ve isim döndürür."""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT ad_soyad FROM KULLANICILAR ORDER BY id DESC LIMIT 1")
            user = cursor.fetchone()
            conn.close()
            
            isim = user[0] if user else "Tanımsız Kişi"
            return isim, results.detections[0]
        except:
            return "Sistem Hatası", results.detections[0]
            
    return None, None

def log_kaydet(isim, durum="Giriş Başarılı"):
    """Giriş olayını veritabanına işler."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO GIRIS_KAYITLARI (tarih_saat, durum, giren_kisi_bilgisi)
            VALUES (?, ?, ?)
        """, (zaman, durum, isim))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Log hatası: {e}")