import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

class KameraThread(QThread):
    yeni_kare = pyqtSignal(QImage)

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0) # 0: Dahili kamera
        
        mp_face = mp.solutions.face_detection
        with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
            while self.running:
                ret, frame = cap.read()
                if not ret: break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb_frame)

                
                if results.detections:
                    for detection in results.detections:
                        bbox = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), \
                                    int(bbox.width * iw), int(bbox.height * ih)
                        
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, "TARANIYOR...", (x, y - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                h, w, ch = frame.shape
                q_img = QImage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).data, w, h, ch * w, QImage.Format_RGB888)
                self.yeni_kare.emit(q_img)
        
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

class SistemiBaslat(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        # Kamera Kartı
        self.card = QFrame(); self.card.setObjectName("ContentCard")
        l = QVBoxLayout(self.card)
        
        self.lbl_cam = QLabel("KAMERA HAZIR")
        self.lbl_cam.setAlignment(Qt.AlignCenter)
        self.lbl_cam.setMinimumHeight(550)
        self.lbl_cam.setStyleSheet("background-color: #000; border-radius: 15px; color: #444;")
        
        self.btn_start = QPushButton("▶ GÜVENLİK TARAMASINI BAŞLAT")
        self.btn_start.setObjectName("ActionBtn")
        self.btn_start.clicked.connect(self.kamerayi_tetikle)
        
        l.addWidget(self.lbl_cam)
        l.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        layout.addWidget(self.card)

    def kamerayi_tetikle(self):
        self.thread = KameraThread()
        self.thread.yeni_kare.connect(self.goruntu_guncelle)
        self.thread.start()
        self.btn_start.setEnabled(False)
        self.btn_start.setText("SİSTEM AKTİF")

    def goruntu_guncelle(self, image):
        self.lbl_cam.setPixmap(QPixmap.fromImage(image).scaled(
            self.lbl_cam.width(), self.lbl_cam.height(), Qt.KeepAspectRatioByExpanding))