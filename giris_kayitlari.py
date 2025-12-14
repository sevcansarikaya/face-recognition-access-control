from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt
import sqlite3

class GirisKayitlari(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        button_layout = QHBoxLayout()
        self.btn_personel = QPushButton("Personel Listesi")
        self.btn_personel.setObjectName("ActionBtn")
        self.btn_personel.clicked.connect(self.personelleri_listele)

        self.btn_loglar = QPushButton("Giriş Logları")
        self.btn_loglar.setObjectName("ActionBtn")
        self.btn_loglar.clicked.connect(self.loglari_listele)

        button_layout.addWidget(self.btn_personel)
        button_layout.addWidget(self.btn_loglar)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        card = QFrame(); card.setObjectName("ContentCard")
        l = QVBoxLayout(card)
        self.lbl_baslik = QLabel("VERİ LİSTESİ")
        self.lbl_baslik.setStyleSheet("color: white; font-weight: bold; font-size: 16px; margin-bottom: 10px;")
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        l.addWidget(self.lbl_baslik)
        l.addWidget(self.table)
        layout.addWidget(card)

    def personelleri_listele(self):
        self.lbl_baslik.setText("KAYITLI PERSONEL LİSTESİ")
        self.table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "Bölüm", "Kayıt Tarihi"])
        self.verileri_yukle("SELECT id, ad_soyad, bolum, kayit_tarihi FROM KULLANICILAR")

    def loglari_listele(self):
        self.lbl_baslik.setText("SİSTEM ERİŞİM KAYITLARI")
        self.table.setHorizontalHeaderLabels(["Zaman", "Durum", "Kişi", "ID"])
        self.verileri_yukle("SELECT tarih_saat, durum, giren_kisi_bilgisi, id FROM GIRIS_KAYITLARI")

    def verileri_yukle(self, sorgu):
        try:
            conn = sqlite3.connect("access_control.db")
            cursor = conn.cursor()
            cursor.execute(sorgu)
            veriler = cursor.fetchall()
            self.table.setRowCount(0)
            for row_idx, row_data in enumerate(veriler):
                self.table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem(str(value)) # Artık hata vermez
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)
            conn.close()
        except Exception as e:
            print(f"Hata: {e}")