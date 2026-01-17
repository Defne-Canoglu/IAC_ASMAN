import os
import glob
import numpy as np
import rasterio
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
import config

def dosyalari_otomatik_bul():
    """
    İşlenmiş haritalar klasöründeki dosyaları bulur ve tarihe göre sıralar.
    """
    print("🔍 Haritalar taranıyor...")
    
    # Klasördeki tüm .tif dosyalarını bul
    dosyalar = glob.glob(os.path.join(config.OUTPUT_DIR, "*.tif"))
    
    # Eğer .tif yoksa hata ver
    if len(dosyalar) < 2:
        print(f"❌ HATA: '{config.OUTPUT_DIR}' klasöründe yeterli harita yok!")
        print("Lütfen önce 'islemi_baslat.py' kodunu çalıştırıp tamamlanmasını bekle.")
        return None, None

    # Dosyaları ismine (içindeki tarihe) göre sırala
    dosyalar.sort()
    
    # Tarihi eski olan -> Yangın Öncesi (0)
    # Tarihi yeni olan -> Yangın Sonrası (1)
    pre_fire = dosyalar[0]
    post_fire = dosyalar[-1]
    
    print(f"✅ Yangın Öncesi (Güvenli): {os.path.basename(pre_fire)}")
    print(f"🔥 Yangın Sonrası (Yanmış): {os.path.basename(post_fire)}")
    
    return pre_fire, post_fire

def goruntu_parcala(tif_path, label, tile_size=256):
    """
    Uydu görüntüsünü modelin anlayacağı küçük karelere böler.
    """
    print(f"🔄 Veri Hazırlanıyor: {os.path.basename(tif_path)}")
    
    images = []
    weather_data = []
    labels = []

    with rasterio.open(tif_path) as src:
        img = src.read(1) 
        img = np.nan_to_num(img) # Boş değerleri temizle
        
        # Normalizasyon (0-1 arası)
        img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-7)

        rows, cols = img.shape
        # Kare kare kes (Adım adım)
        for r in range(0, rows - tile_size, tile_size):
            for c in range(0, cols - tile_size, tile_size):
                tile = img[r:r+tile_size, c:c+tile_size]
                
                # Sadece dolu kareleri al (Siyah kenarlıkları atla)
                if np.mean(tile) > 0.01:
                    images.append(np.expand_dims(tile, axis=-1))
                    labels.append(label)
                    
                    # --- HAVA DURUMU SİMÜLASYONU ---
                    if label == 1: # Yangın Anı (Sıcak, Kuru, Rüzgarlı)
                        w = [np.random.uniform(35, 45), np.random.uniform(10, 25), np.random.uniform(20, 40), 0.1]
                    else: # Normal (Ilıman)
                        w = [np.random.uniform(20, 30), np.random.uniform(40, 60), np.random.uniform(5, 15), 0.4]
                    
                    weather_data.append(w)

    return np.array(images), np.array(weather_data), np.array(labels)

def egitimi_baslat():
    # 1. Dosyaları Bul
    pre_path, post_path = dosyalari_otomatik_bul()
    if not pre_path: return

    # 2. Verileri Parçala
    print("\n📊 Veri Seti Oluşturuluyor (RAM Kullanılıyor)...")
    X_img_0, X_weath_0, y_0 = goruntu_parcala(pre_path, label=0)
    X_img_1, X_weath_1, y_1 = goruntu_parcala(post_path, label=1)

    # Birleştir
    X_img = np.concatenate([X_img_0, X_img_1])
    X_weath = np.concatenate([X_weath_0, X_weath_1])
    y = np.concatenate([y_0, y_1])

    print(f"✅ Toplam Eğitim Karesi: {len(y)} adet")

    # Train/Test Ayrımı
    X_img_train, X_img_test, X_weath_train, X_weath_test, y_train, y_test = train_test_split(
        X_img, X_weath, y, test_size=0.2, random_state=42
    )

    # 3. Modeli Yükle ve Eğit
    if not os.path.exists(config.MODEL_PATH):
        print("❌ Model dosyası yok! Önce 'asman_beyin.py' çalıştır.")
        return

    print("🧠 Model Yükleniyor...")
    model = load_model(config.MODEL_PATH)

    print("\n🚀 EĞİTİM BAŞLIYOR (M2 GPU Devrede)...")
    print("------------------------------------------------")
    history = model.fit(
        [X_img_train, X_weath_train], y_train,
        epochs=15,            # 15 Tur dönecek
        batch_size=32,
        validation_data=([X_img_test, X_weath_test], y_test)
    )

    # 4. Kaydet
    kayit_yolu = os.path.join(config.BASE_DIR, "asman_egitilmis_model.h5")
    model.save(kayit_yolu)
    print(f"\n🎉 TEBRİKLER! ASMAN eğitildi ve göreve hazır.\n💾 Kayıt: {kayit_yolu}")

if __name__ == "__main__":
    egitimi_baslat()