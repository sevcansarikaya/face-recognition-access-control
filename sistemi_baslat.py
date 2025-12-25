import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
import face_core 

class KameraThread(QThread):
    yeni_kare = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        son_kaydedilen_isim = ""

        while self.running:
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1)
            isim, detection = face_core.taranan_yuzu_bul(frame)

            if detection:
                gecersiz = ["Tanımsız Kişi", "Bilinmeyen Kişi", "Sistem Hatası"]
                renk = (0, 0, 255) if isim in gecersiz else (0, 255, 0)

                if isim not in gecersiz and isim != son_kaydedilen_isim:
                    face_core.log_kaydet(isim)
                    son_kaydedilen_isim = isim
                
                bbox = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), renk, 3) 
                cv2.putText(frame, isim, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.0, renk, 3)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            q_img = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
            self.yeni_kare.emit(q_img)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()

class SistemiBaslat(QWidget):
    def __init__(self):
        super().__init__()
        self.is_camera_on = False  # HATA VEREN isRunning YERİNE BU BAYRAĞI KULLANACAĞIZ
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        self.card = QFrame(); self.card.setObjectName("ContentCard")
        l = QVBoxLayout(self.card)
        
        self.lbl_cam = QLabel("KAMERA HAZIR"); self.lbl_cam.setAlignment(Qt.AlignCenter)
        self.lbl_cam.setMinimumHeight(550); self.lbl_cam.setStyleSheet("background-color: #000; border-radius: 15px;")
        
        self.btn_start = QPushButton("▶ GÜVENLİK TARAMASINI BAŞLAT")
        self.btn_start.setObjectName("ActionBtn")
        self.btn_start.clicked.connect(self.kamerayi_tetikle)
        
        l.addWidget(self.lbl_cam); l.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        layout.addWidget(self.card)

    def kamerayi_tetikle(self):
        # Eğer kamera kapalıysa başlat
        if not self.is_camera_on:
            self.thread = KameraThread()
            self.thread.yeni_kare.connect(self.goruntu_guncelle)
            self.thread.start()
            self.is_camera_on = True # Bayrağı güncelle
            self.btn_start.setText("🔴 SİSTEMİ DURDUR")
            self.btn_start.setStyleSheet("background-color: #c0392b; color: white;")
        else:
            # Eğer kamera açıksa durdur
            if hasattr(self, 'thread'):
                self.thread.stop()
            self.is_camera_on = False # Bayrağı güncelle
            self.btn_start.setText("▶ GÜVENLİK TARAMASINI BAŞLAT")
            self.btn_start.setStyleSheet("")
            self.lbl_cam.clear()
            self.lbl_cam.setText("KAMERA DURDURULDU")

    def goruntu_guncelle(self, image):
        self.lbl_cam.setPixmap(QPixmap.fromImage(image).scaled(self.lbl_cam.width(), self.lbl_cam.height(), Qt.KeepAspectRatio))