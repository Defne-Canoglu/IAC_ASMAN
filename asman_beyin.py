import tensorflow as tf
from tensorflow.keras import layers, models, Input
import os
import config

def model_olustur():
    print("\n ASMAN Yapay Zeka Modeli İnşa Ediliyor...")
    
    # --- GÖRSEL GİRİŞ (Uydu Görüntüsü) ---
    img_input = Input(shape=(256, 256, 1), name="Uydu_Goruntusu")
    
    x = layers.Conv2D(32, (3, 3), activation='relu')(img_input)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Conv2D(64, (3, 3), activation='relu')(x)
    x = layers.Flatten()(x)
    
    # --- SAYISAL GİRİŞ (Hava Durumu) ---
    sensor_input = Input(shape=(4,), name="Sensor_Verileri")
    y = layers.Dense(16, activation='relu')(sensor_input)
    
    # --- BİRLEŞTİRME ---
    combined = layers.concatenate([x, y])
    
    # --- KARAR ---
    z = layers.Dense(64, activation='relu')(combined)
    output = layers.Dense(1, activation='sigmoid', name="Yangin_Riski")(z)
    
    model = models.Model(inputs=[img_input, sensor_input], outputs=output)
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print(" Model Mimarisi Oluşturuldu!")
    return model

if __name__ == "__main__":
    # GPU kontrolü
    print(f" Aktif GPU Sayısı: {len(tf.config.list_physical_devices('GPU'))}")
    
    model = model_olustur()
    model.summary()
    
    model.save(config.MODEL_PATH)
    print(f"💾 Model taslağı şuraya kaydedildi: {config.MODEL_PATH}")
