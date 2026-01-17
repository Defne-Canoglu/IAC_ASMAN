import asf_search as asf
import config
import os

# --- NASA EARTHDATA KULLANICI BİLGİLERİN ---
# Buraya kullanıcı adını ve şifreni yazmalısın!
# Eğer hesabın yoksa: https://urs.earthdata.nasa.gov/users/new
KULLANICI_ADI = "BURAYA_KULLANICI_ADINI_YAZ"
SIFRE = "BURAYA_SIFRENI_YAZ"

def veri_indir_manavgat():
    print("📡 NASA Sunucularına Bağlanılıyor...")
    
    try:
        session = asf.ASFSession().auth_with_creds(KULLANICI_ADI, SIFRE)
    except Exception as e:
        print("❌ Giriş Başarısız! Kullanıcı adı ve şifreni koda yazdın mı?")
        print(f"Hata: {e}")
        return

    print("✅ Giriş Başarılı. Manavgat Yangını verileri aranıyor...")

    # Aranan Alan: Manavgat (WKT Formatında)
    aoi = "POINT(31.45 36.79)"

    # 1. Yangın Öncesi (Temmuz 2021)
    results_pre = asf.search(
        platform=asf.PLATFORM.SENTINEL1,
        intersectsWith=aoi,
        start="2021-07-20",
        end="2021-07-25",
        processingLevel=asf.PRODUCT_TYPE.GRD_HD,
        beamMode=asf.BEAMMODE.IW,
        maxResults=1
    )

    # 2. Yangın Sonrası (Ağustos 2021)
    results_post = asf.search(
        platform=asf.PLATFORM.SENTINEL1,
        intersectsWith=aoi,
        start="2021-08-14",
        end="2021-08-18",
        processingLevel=asf.PRODUCT_TYPE.GRD_HD,
        beamMode=asf.BEAMMODE.IW,
        maxResults=1
    )

    tum_sonuclar = results_pre + results_post
    
    if len(tum_sonuclar) < 2:
        print("❌ Veriler bulunamadı. Tarihleri veya koordinatları kontrol et.")
        return

    print(f"📦 {len(tum_sonuclar)} adet veri bulundu. İndirme başlıyor (Yaklaşık 1.5 - 2 GB)...")
    print("☕ Bu işlem internet hızına göre zaman alabilir, lütfen bekle.")

    # İndirme İşlemi
    try:
        asf.download_urls(
            urls=[r.properties['url'] for r in tum_sonuclar],
            path=config.DATA_DIR,
            session=session
        )
        print("\n🎉 İndirme Tamamlandı! Dosyalar 'veriler' klasöründe.")
        
    except Exception as e:
        print(f"❌ İndirme Hatası: {e}")

if __name__ == "__main__":
    if KULLANICI_ADI == "BURAYA_KULLANICI_ADINI_YAZ":
        print("⚠️ Lütfen kodu açıp KULLANICI_ADI ve SIFRE kısımlarını doldur!")
    else:
        veri_indir_manavgat()