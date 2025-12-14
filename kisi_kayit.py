from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class KisiKayit(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)

        # Form
        form_card = QFrame(); form_card.setObjectName("ContentCard")
        f_lay = QVBoxLayout(form_card)
        f_lay.addWidget(QLabel("YENİ KİŞİ KAYDI", styleSheet="color: white; font-size: 20px; font-weight: bold;"))
        
        self.txt_ad = QLineEdit(); self.txt_ad.setPlaceholderText("Ad Soyad...")
        self.txt_bolum = QLineEdit(); self.txt_bolum.setPlaceholderText("Bölüm...")
        btn_foto = QPushButton("📁 Fotoğraf Seç"); btn_foto.setObjectName("ActionBtn")
        btn_foto.clicked.connect(self.foto_sec)
        
        self.btn_kaydet = QPushButton("💾 SİSTEME KAYDET"); self.btn_kaydet.setObjectName("ActionBtn")
        self.btn_kaydet.setStyleSheet("background-color: #27ae60;")

        f_lay.addWidget(self.txt_ad); f_lay.addWidget(self.txt_bolum); f_lay.addWidget(btn_foto)
        f_lay.addStretch(); f_lay.addWidget(self.btn_kaydet)

        # Önizleme
        self.lbl_preview = QLabel("FOTOĞRAF ÖNİZLEME")
        self.lbl_preview.setFixedSize(350, 350)
        self.lbl_preview.setStyleSheet("border: 2px dashed #333333; color: #555555; border-radius: 10px;")
        self.lbl_preview.setAlignment(Qt.AlignCenter)

        layout.addWidget(form_card, 2)
        layout.addWidget(self.lbl_preview, 1)

    def foto_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Seç", "", "Resimler (*.jpg *.png)")
        if dosya:
            self.lbl_preview.setPixmap(QPixmap(dosya).scaled(350, 350, Qt.KeepAspectRatio))
            self.secilen_yol = dosya