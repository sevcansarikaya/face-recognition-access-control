from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
from PyQt5.QtCore import Qt

class KontrolPaneli(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent # Ana panele erişmek için
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        self.card_personel = self.make_card("KAYITLI PERSONEL", "0", 3) 
        self.card_girisler = self.make_card("BUGÜNKÜ GİRİŞLER", "0", 3)
        self.card_uyari = self.make_card("YETKİSİZ DENEME", "0", 3)
        self.card_durum = self.make_card("SİSTEM DURUMU", "AKTİF", 2)

        grid.addWidget(self.card_personel, 0, 0)
        grid.addWidget(self.card_girisler, 0, 1)
        grid.addWidget(self.card_uyari, 1, 0)
        grid.addWidget(self.card_durum, 1, 1)
        
        layout.addLayout(grid)
        layout.addStretch()

    def make_card(self, title, val, index):
        card = QFrame()
        card.setObjectName("ContentCard")
        card.setFixedHeight(140)
        card.setCursor(Qt.PointingHandCursor)
        l = QVBoxLayout(card)
        v = QLabel(val); v.setObjectName("StatVal")
        t = QLabel(title); t.setObjectName("StatTitle")
        l.addWidget(v); l.addWidget(t)
        card.mousePressEvent = lambda event: self.parent.yonlendir(index)
        card.v_lbl = v
        return card