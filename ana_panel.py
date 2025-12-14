import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Kendi dosyalarımızı çekiyoruz
from kontrol_paneli import KontrolPaneli
from kisi_kayit import KisiKayit
from sistemi_baslat import SistemiBaslat
from giris_kayitlari import GirisKayitlari

class AnaPanel(QMainWindow):
    def __init__(self, kullanici_adi="Admin"):
        super().__init__()
        self.kullanici_adi = kullanici_adi
        self.resize(1280, 850)
        self.DATABASE = "access_control.db"
        self.arayuz_hazirla()
        self.istatistikleri_guncelle()

    def arayuz_hazirla(self):
        self.ana_widget = QWidget()
        self.setCentralWidget(self.ana_widget)
        self.ana_layout = QHBoxLayout(self.ana_widget)
        self.ana_layout.setContentsMargins(0,0,0,0)
        self.ana_layout.setSpacing(0)

        # Stil (Karanlık Tema)
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QFrame#Sidebar { background-color: #1e1e1e; border-right: 1px solid #333333; min-width: 250px; }
            QPushButton#MenuBtn { background-color: transparent; color: #888888; border: none; text-align: left; padding: 18px 25px; font-weight: bold; }
            QPushButton#MenuBtn:checked { background-color: #252525; color: #004a99; border-left: 4px solid #004a99; }
            QFrame#ContentCard { background-color: #1e1e1e; border-radius: 12px; border: 1px solid #333333; }
            QLabel#StatVal { color: white; font-size: 32px; font-weight: bold; }
            QLabel#StatTitle { color: #888888; font-size: 12px; font-weight: bold; }
            QLineEdit { background-color: #252525; border: 1px solid #333333; border-radius: 6px; padding: 10px; color: white; }
            QPushButton#ActionBtn { background-color: #004a99; color: white; border-radius: 6px; padding: 10px; font-weight: bold; }
        """)

        # Sidebar
        self.sidebar = QFrame(); self.sidebar.setObjectName("Sidebar")
        s_lay = QVBoxLayout(self.sidebar)
        s_lay.addWidget(QLabel("🛡️ SECURE GATE", styleSheet="color:white; font-size:20px; font-weight:bold; margin:20px;"))
        
        self.menu_buttons = []
        menus = ["Kontrol Paneli", "Kişi Kayıt", "Sistemi Başlat", "Giriş Kayıtları"]
        for i, m in enumerate(menus):
            btn = QPushButton(m); btn.setObjectName("MenuBtn"); btn.setCheckable(True); btn.setAutoExclusive(True)
            if i==0: btn.setChecked(True)
            btn.clicked.connect(self.sayfa_degistir)
            s_lay.addWidget(btn); self.menu_buttons.append(btn)
        s_lay.addStretch()

        # Stacked Pages
        self.pages = QStackedWidget()
        self.p_dashboard = KontrolPaneli(self)
        self.p_kayit = KisiKayit()
        self.p_kamera = SistemiBaslat()
        self.p_loglar = GirisKayitlari()
        
        self.pages.addWidget(self.p_dashboard)
        self.pages.addWidget(self.p_kayit)
        self.pages.addWidget(self.p_kamera)
        self.pages.addWidget(self.p_loglar)

        self.ana_layout.addWidget(self.sidebar)
        self.ana_layout.addWidget(self.pages)

    def sayfa_degistir(self):
        btn = self.sender()
        idx = self.menu_buttons.index(btn)
        self.pages.setCurrentIndex(idx)
        if idx == 0: self.istatistikleri_guncelle()

    def yonlendir(self, idx): # Kartlara tıklayınca burası çalışır
        self.menu_buttons[idx].setChecked(True)
        self.pages.setCurrentIndex(idx)

    def istatistikleri_guncelle(self):
        try:
            conn = sqlite3.connect(self.DATABASE); cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM KULLANICILAR")
            self.p_dashboard.card_personel.v_lbl.setText(str(cursor.fetchone()[0]))
            conn.close()
        except: pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AnaPanel()
    ex.show()
    sys.exit(app.exec_())