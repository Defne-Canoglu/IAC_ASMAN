import os
import glob
import sys
# SNAP yolunu kod çalışmadan önce sisteme zorla tanıtıyoruz
# Bu satır sayesinde "SNAP not found" hatası çözülecek.
snap_path = "/Applications/esa-snap/bin"
os.environ["PATH"] += os.pathsep + snap_path

from pyroSAR import identify, Archive
from pyroSAR.snap.util import geocode
import config

def sar_verilerini_isle():
    print("🔍 Veriler taranıyor...")
    print(f"🛠️  SNAP Yolu Ayarlandı: {snap_path}")

    # .zip ve .SAFE dosyalarını bul
    zip_dosyalari = glob.glob(os.path.join(config.DATA_DIR, "*.zip"))
    safe_klasorleri = glob.glob(os.path.join(config.DATA_DIR, "*.SAFE"))
    tum_dosyalar = zip_dosyalari + safe_klasorleri
    
    if not tum_dosyalar:
        print(f"❌ HATA: '{config.DATA_DIR}' klasöründe veri bulunamadı!")
        return

    print(f"📦 Toplam {len(tum_dosyalar)} adet veri bulundu. İşlem başlıyor...")

    with Archive(config.DB_NAME) as arsiv:
        for dosya_yolu in tum_dosyalar:
            dosya_adi = os.path.basename(dosya_yolu)
            print(f"\n🔄 İşleniyor: {dosya_adi}")
            
            try:
                # 1. Veritabanına Ekle
                sahne = identify(dosya_yolu)
                arsiv.insert(sahne)
                print("   ✅ Veritabanına kaydedildi.")

                # 2. SNAP ile İşle
                print("   ⏳ SNAP Geocoding başlatılıyor...")
                print("   ☕ Bu işlem M2 işlemcide bile dosya başına 3-5 dakika sürebilir. Lütfen kapatma!")
                
                # SNAP'i çalıştır
                geocode(
                    infile=dosya_yolu,
                    outdir=config.OUTPUT_DIR,
                    t_srs=4326,       
                    spacing=10,       
                    polarizations=['VH', 'VV'], 
                    cleanup=True
                )
                print("   ✅ Başarıyla işlendi ve harita oluşturuldu!")
                
            except Exception as e:
                print(f"   ❌ HATA OLUŞTU: {e}")

    print(f"\n🎉 Tüm işlemler bitti! Çıktılar: {config.OUTPUT_DIR}")

if __name__ == "__main__":
    sar_verilerini_isle()