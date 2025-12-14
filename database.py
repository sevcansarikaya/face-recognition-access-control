import sqlite3

DATABASE_NAME = "access_control.db"

def setup_database():
    """Veritabanı dosyasını oluşturur ve gerekli tabloları tanımlar."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 1. KULLANICILAR Tablosu (Yetkili Kişiler)
    # Yeni Alan: foto_yolu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS KULLANICILAR (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_soyad TEXT NOT NULL,
        bolum TEXT,
        yuz_encoding TEXT NOT NULL,  
        foto_yolu TEXT,  -- FOTOĞRAFIN DİZİN YOLU BURADA TUTULUR
        yetki_seviyesi INTEGER DEFAULT 0,
        kayit_tarihi TEXT
    );
    """)

    # 2. GIRIS_KAYITLARI Tablosu (Loglar)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS GIRIS_KAYITLARI (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih_saat TEXT NOT NULL,
        durum TEXT NOT NULL,
        giren_kisi_bilgisi TEXT,
        ekran_goruntusu_yolu TEXT
    );
    """)
    
    # 3. ADMIN_KULLANICILARI Tablosu (Masaüstü uygulaması Login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ADMIN_KULLANICILARI (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_adi TEXT UNIQUE NOT NULL,
        sifre_hash TEXT NOT NULL 
    );
    """)

    conn.commit()
    conn.close()
    print(f"Veritabanı '{DATABASE_NAME}' ve tablolar başarıyla kuruldu.")


if __name__ == '__main__':
    setup_database()