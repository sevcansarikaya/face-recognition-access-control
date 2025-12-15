from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
import os

# Daha önce yazdığımız yüz işleme fonksiyonunu buraya dahil edeceğiz
# Şimdilik hata almamak için dosyanın üstünde dursun

class KisiKayit(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent # Ana panele erişmek ve istatistikleri güncellemek için
        self.secilen_yol = None
        self.arayuz_olustur()

    def arayuz_olustur(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(30)

        # Form Kartı
        form_card = QFrame(); form_card.setObjectName("ContentCard")
        f_lay = QVBoxLayout(form_card)
        f_lay.addWidget(QLabel("YENİ KİŞİ KAYDI", styleSheet="color: white; font-size: 20px; font-weight: bold;"))
        
        self.txt_ad = QLineEdit(); self.txt_ad.setPlaceholderText("Ad Soyad...")
        self.txt_bolum = QLineEdit(); self.txt_bolum.setPlaceholderText("Bölüm...")
        
        btn_foto = QPushButton("📁 Fotoğraf Seç"); btn_foto.setObjectName("ActionBtn")
        btn_foto.clicked.connect(self.foto_sec)
        
        self.btn_kaydet = QPushButton("💾 SİSTEME KAYDET"); self.btn_kaydet.setObjectName("ActionBtn")
        self.btn_kaydet.setStyleSheet("background-color: #27ae60;")
        self.btn_kaydet.clicked.connect(self.veriyi_islemeye_gonder) # Kaydet butonu bağlandı

        f_lay.addWidget(self.txt_ad); f_lay.addWidget(self.txt_bolum); f_lay.addWidget(btn_foto)
        f_lay.addStretch(); f_lay.addWidget(self.btn_kaydet)

        # Önizleme Alanı
        self.lbl_preview = QLabel("FOTOĞRAF ÖNİZLEME")
        self.lbl_preview.setFixedSize(350, 350)
        self.lbl_preview.setStyleSheet("border: 2px dashed #333333; color: #555555; border-radius: 10px;")
        self.lbl_preview.setAlignment(Qt.AlignCenter)

        layout.addWidget(form_card, 2)
        layout.addWidget(self.lbl_preview, 1)

    def foto_sec(self):
        dosya, _ = QFileDialog.getOpenFileName(self, "Personel Fotoğrafı Seç", "", "Resimler (*.jpg *.png *.jpeg)")
        if dosya:
            self.secilen_yol = dosya
            self.lbl_preview.setPixmap(QPixmap(dosya).scaled(350, 350, Qt.KeepAspectRatio))

    def veriyi_islemeye_gonder(self):
        ad = self.txt_ad.text()
        bolum = self.txt_bolum.text()
        
        if not ad or not self.secilen_yol:
            QMessageBox.warning(self, "Hata", "Lütfen isim girin ve bir fotoğraf seçin!")
            return

        # BURASI ÇOK ÖNEMLİ: Yüz tanıma motoruna gidiyoruz
        try:
            # face_core.py dosyasındaki fonksiyonu çağırıyoruz
            import face_core 
            success, mesaj = face_core.register_new_user(ad, bolum, 0, self.secilen_yol)
            
            if success:
                QMessageBox.information(self, "Başarılı", mesaj)
                self.txt_ad.clear()
                self.txt_bolum.clear()
                self.lbl_preview.setText("FOTOĞRAF ÖNİZLEME")
                self.secilen_yol = None
                # Ana sayfadaki sayıyı güncelle
                if self.parent:
                    self.parent.istatistikleri_guncelle()
            else:
                QMessageBox.critical(self, "Hata", mesaj)
                
        except Exception as e:
            QMessageBox.critical(self, "Sistem Hatası", f"Yüz tanıma motoru çalıştırılamadı: {str(e)}")