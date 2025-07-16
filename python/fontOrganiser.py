import os
import shutil

# Ana font klasörü
base_dir = "fonts"

# Weight klasörleri (Regular referans alınır)
weights = ["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]

# Kaynak olarak Regular klasörünü kullanacağız
reference_weight = "Regular"
reference_dir = os.path.join(base_dir, reference_weight)

# Önce referans klasör kontrolü
if not os.path.exists(reference_dir):
    print(f"❌ Referans klasör bulunamadı: {reference_dir}")
    exit(1)

# Referans font dosyalarını oku
reference_fonts = [f for f in os.listdir(reference_dir) if f.lower().endswith(".ttf")]

for font_file in reference_fonts:
    # Örneğin: "NotoSansDevanagari-Regular.ttf"
    if "-Regular" not in font_file:
        continue  # Sadece "-Regular" içeren dosyaları dikkate al

    font_name_prefix = font_file.replace("-Regular.ttf", "")  # "NotoSansDevanagari"

    for weight in weights:
        if weight == reference_weight:
            continue  # Kendi klasörünü atla

        target_dir = os.path.join(base_dir, weight)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        target_font_name = f"{font_name_prefix}-{weight}.ttf"
        target_font_path = os.path.join(target_dir, target_font_name)

        if os.path.exists(target_font_path):
            continue  # Zaten varsa geç

        # Kaynak dosya ve kopyalanacak hedef
        source_path = os.path.join(reference_dir, font_file)

        try:
            shutil.copy2(source_path, target_font_path)
            print(f"📁 Kopyalandı: {font_file} → {weight}/{target_font_name}")
        except Exception as e:
            print(f"❌ Hata kopyalanırken: {font_file} → {weight}: {e}")

print("✅ Eksik fontlar tamamlandı.")
