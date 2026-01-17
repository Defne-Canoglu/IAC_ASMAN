import os
import platform

# --- PROJE ANA DİZİNİ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Klasör Yolları
DATA_DIR = os.path.join(BASE_DIR, "veriler")
OUTPUT_DIR = os.path.join(BASE_DIR, "islenmis_haritalar")
MODEL_PATH = os.path.join(BASE_DIR, "asman_model.h5")
DB_NAME = os.path.join(BASE_DIR, "sar_katalogum.db")  # EKSİK OLAN BU SATIR ARTIK BURADA

# Klasörleri yoksa oluştur
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# SNAP Yolu (MacBook M2 için)
if platform.system() == "Darwin":
    SNAP_GPT_PATH = "/Applications/esa-snap/bin/gpt"
else:
    SNAP_GPT_PATH = "gpt"

# Hedef Bölge
HEDEF_KOORDINATLAR = "31.0,36.5,32.0,37.2"
