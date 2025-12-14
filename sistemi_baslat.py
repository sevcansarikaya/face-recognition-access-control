from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt5.QtCore import Qt

class SistemiBaslat(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        card = QFrame(); card.setObjectName("ContentCard")
        l = QVBoxLayout(card)
        self.lbl_cam = QLabel("SİSTEM HAZIR\n[ Kamera Akışı ]")
        self.lbl_cam.setAlignment(Qt.AlignCenter)
        self.lbl_cam.setStyleSheet("color: #444444; font-size: 20px; font-weight: bold; border: 2px solid #333333; border-radius: 15px;")
        self.lbl_cam.setMinimumHeight(550)
        
        self.btn_start = QPushButton("▶ GÜVENLİK TARAMASINI BAŞLAT")
        self.btn_start.setObjectName("ActionBtn")
        
        l.addWidget(self.lbl_cam)
        l.addWidget(self.btn_start, alignment=Qt.AlignCenter)
        layout.addWidget(card)