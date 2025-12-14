import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QMessageBox, QFrame, QHBoxLayout, QAction)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QCursor, QIcon

class LoginEkranı(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Güvenlik Paneli | Giriş")
        self.setFixedSize(500, 650)
        self.sifre_gorunur = False
        self.arayuz_hazirla()

    def arayuz_hazirla(self):
        # Ana Layout
        ana_layout = QVBoxLayout()
        ana_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(ana_layout)

        # Stil Sayfası (QSS) - Profesyonel Renk Paleti
        self.setStyleSheet("""
            QWidget { background-color: #121212; }
            QFrame#MainCard { 
                background-color: #1e1e1e; 
                border-radius: 15px; 
                border: 1px solid #333333;
            }
            QLabel#Baslik { 
                color: #ffffff; 
                font-size: 24px; 
                font-weight: bold; 
                margin-bottom: 5px;
            }
            QLabel#Etiket { 
                color: #aaaaaa; 
                font-size: 13px; 
                font-weight: bold; 
                margin-top: 10px;
            }
            QLineEdit {
                border: 1px solid #333333;
                border-radius: 6px;
                padding: 12px;
                font-size: 14px;
                background-color: #252525;
                color: #ffffff;
            }
            QLineEdit:focus { border: 1px solid #0056b3; }
            
            QPushButton#GirisBtn {
                background-color: #004a99;
                color: white;
                border-radius: 6px;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton#GirisBtn:hover { background-color: #005bc1; }
            
            QLabel#UnuttumLink {
                color: #888888;
                font-size: 12px;
            }
            QLabel#UnuttumLink:hover { color: #ffffff; }
        """)

        # Arka Plan Hizalama
        merkez_layout = QVBoxLayout()
        merkez_layout.setAlignment(Qt.AlignCenter)
        ana_layout.addLayout(merkez_layout)

        # Ana Kart (Giriş Kutusu)
        self.kart = QFrame()
        self.kart.setObjectName("MainCard")
        self.kart.setFixedSize(400, 520)
        kart_layout = QVBoxLayout(self.kart)
        kart_layout.setContentsMargins(40, 40, 40, 40)
        kart_layout.setSpacing(8)

        # Üst İkon
        self.label_icon = QLabel("🛡️")
        self.label_icon.setFont(QFont("Arial", 45))
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.label_icon.setStyleSheet("margin-bottom: 10px; background: transparent; border: none;")
        kart_layout.addWidget(self.label_icon)

        # Başlık
        self.label_baslik = QLabel("YÖNETİCİ GİRİŞ PANELİ")
        self.label_baslik.setObjectName("Baslik")
        self.label_baslik.setAlignment(Qt.AlignCenter)
        self.label_baslik.setStyleSheet("background: transparent; border: none;")
        kart_layout.addWidget(self.label_baslik)

        # Kullanıcı Adı
        self.lbl_user = QLabel("Kullanıcı Adı")
        self.lbl_user.setObjectName("Etiket")
        self.lbl_user.setStyleSheet("background: transparent; border: none;")
        kart_layout.addWidget(self.lbl_user)
        
        self.input_kullanici = QLineEdit()
        self.input_kullanici.setPlaceholderText("Kullanıcı adınızı yazın")
        kart_layout.addWidget(self.input_kullanici)

        # Şifre
        self.lbl_pass = QLabel("Şifre")
        self.lbl_pass.setObjectName("Etiket")
        self.lbl_pass.setStyleSheet("background: transparent; border: none;")
        kart_layout.addWidget(self.lbl_pass)
        
        self.input_sifre = QLineEdit()
        self.input_sifre.setPlaceholderText("••••••••")
        self.input_sifre.setEchoMode(QLineEdit.Password)
        
        # Şifre Göz İkonu (Action)
        self.goz_aksiyon = QAction(self)
        self.goz_aksiyon.setIcon(QIcon()) # İkonu aşağıda unicode ile set edeceğiz
        self.input_sifre.addAction(self.goz_aksiyon, QLineEdit.TrailingPosition)
        self.goz_aksiyon.triggered.connect(self.sifre_goster_gizle)
        self.goz_guncelle()
        
        kart_layout.addWidget(self.input_sifre)

        # Giriş Butonu
        self.btn_giris = QPushButton("SİSTEME GİRİŞ YAP")
        self.btn_giris.setObjectName("GirisBtn")
        self.btn_giris.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_giris.clicked.connect(self.veritabani_kontrol)
        kart_layout.addWidget(self.btn_giris)

        # Şifremi Unuttum (Yazı Link)
        self.label_unuttum = QLabel("<a href='#' style='color: #888888; text-decoration: none;'>Şifremi Unuttum</a>")
        self.label_unuttum.setObjectName("UnuttumLink")
        self.label_unuttum.setAlignment(Qt.AlignCenter)
        self.label_unuttum.setStyleSheet("margin-top: 15px; background: transparent; border: none;")
        self.label_unuttum.linkActivated.connect(self.sifremi_unuttum_aksiyon)
        kart_layout.addWidget(self.label_unuttum)

        merkez_layout.addWidget(self.kart)

    def goz_guncelle(self):
        # Unicode göz simgeleri (İmaj dosyasına ihtiyaç duymaz)
        ikon = "👁️" if self.sifre_gorunur else "🙈"
        self.goz_aksiyon.setText(ikon)

    def sifre_goster_gizle(self):
        if self.sifre_gorunur:
            self.input_sifre.setEchoMode(QLineEdit.Password)
            self.sifre_gorunur = False
        else:
            self.input_sifre.setEchoMode(QLineEdit.Normal)
            self.sifre_gorunur = True
        self.goz_guncelle()

    def veritabani_kontrol(self):
        kullanici = self.input_kullanici.text()
        sifre = self.input_sifre.text()

        if not kullanici or not sifre:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        try:
            conn = sqlite3.connect("access_control.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ADMIN_KULLANICILARI WHERE kullanici_adi = ? AND sifre_hash = ?", 
                           (kullanici, sifre))
            if cursor.fetchone():
                QMessageBox.information(self, "Başarılı", "Erişim onaylandı. Giriş yapılıyor...")
                # Buraya Ana Panel açılış kodu gelecek
            else:
                QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")

    def sifremi_unuttum_aksiyon(self):
        QMessageBox.information(self, "Bilgi", "Şifre sıfırlama talebiniz için destek ile iletişime geçin.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = LoginEkranı()
    pencere.show()
    sys.exit(app.exec_())