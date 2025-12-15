import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class KameraThread(QThread):
    yeni_kare = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        mp_face = mp.solutions.face_detection
        with mp_face.FaceDetection(min_detection_confidence=0.5) as face_detection:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break

                # Yüz Tespiti
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb_frame)

                if results.detections:
                    for detection in results.detections:
                        # Yüzün etrafına kutu çiz
                        bbox = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, "Taraniyor...", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Qt Formatına Çevir
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                q_img = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
                self.yeni_kare.emit(q_img.scaled(800, 600, Qt.KeepAspectRatio))
        cap.release()

class SistemiBaslat(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.card = QFrame(); self.card.setObjectName("ContentCard")
        l = QVBoxLayout(self.card)
        self.lbl_cam = QLabel("KAMERA HAZIR")
        self.lbl_cam.setAlignment(Qt.AlignCenter)
        self.lbl_cam.setMinimumHeight(500)
        self.lbl_cam.setStyleSheet("background-color: black; border-radius: 10px;")
        self.btn = QPushButton("▶ SİSTEMİ BAŞLAT"); self.btn.setObjectName("ActionBtn")
        self.btn.clicked.connect(self.baslat)
        l.addWidget(self.lbl_cam); l.addWidget(self.btn, alignment=Qt.AlignCenter)
        layout.addWidget(self.card)

    def baslat(self):
        self.thread = KameraThread()
        self.thread.yeni_kare.connect(lambda img: self.lbl_cam.setPixmap(QPixmap.fromImage(img)))
        self.thread.start()
        self.btn.setEnabled(False)