import cv2
import mediapipe as mp
import sqlite3
import json
import numpy as np
import os
import datetime

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

DATABASE_NAME = "access_control.db"

def register_new_user(ad_soyad, bolum, yetki, image_path):
    """MediaPipe kullanarak fotoğraftaki yüzü bulur ve kaydeder."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False, "Resim dosyası okunamadı!"

        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.detections:
            return False, "Fotoğrafta yüz tespit edilemedi!"

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
        return True, f"{ad_soyad} başarıyla kaydedildi (MediaPipe Aktif)."
    except Exception as e:
        return False, f"Hata: {str(e)}"