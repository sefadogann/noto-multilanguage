import os
import shutil

source_base_dir = r"tmpFonts"
target_base_dir = r"fonts"
weights = ["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]
weights_lower = [w.lower() for w in weights]
skip_keyword = "condensed"

def find_and_copy_fonts():
    for font_folder_name in os.listdir(source_base_dir):
        font_folder_path = os.path.join(source_base_dir, font_folder_name)
        if not os.path.isdir(font_folder_path):
            continue

        for root, dirs, files in os.walk(font_folder_path):
            for file in files:
                if not file.lower().endswith(".ttf"):
                    continue
                
                filename_lower = file.lower()
                if skip_keyword in filename_lower:
                    print(f"Atlandı (Condensed): {file}")
                    continue
                
                # Dosya adını parçalara ayırıyoruz (örn: 'notosans-bold.ttf' → ['notosans', 'bold.ttf'])
                # '-' ve '_' kullanıyoruz
                parts = []
                for sep in ['-', '_']:
                    if sep in filename_lower:
                        parts = filename_lower.replace('.ttf', '').split(sep)
                        break
                if not parts:
                    # Parçalama olmazsa bütün dosya adı (uzantısız) tek parça olur
                    parts = [filename_lower.replace('.ttf', '')]

                matched_weight = None
                for w_lower, w in zip(weights_lower, weights):
                    # Tam eşleşme arıyoruz (parçalardan biri weight ile aynı olmalı)
                    if w_lower in parts:
                        matched_weight = w
                        break
                
                if not matched_weight:
                    print(f"Atlandı (Weight bulunamadı): {file}")
                    continue
                
                target_dir = os.path.join(target_base_dir, matched_weight)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(target_dir, file)

                if os.path.exists(target_file_path):
                    print(f"Zaten var: {target_file_path}")
                    continue
                
                shutil.copy2(source_file_path, target_file_path)
                print(f"Kopyalandı: {file} → {target_dir}")

if __name__ == "__main__":
    find_and_copy_fonts()
    print("İşlem tamamlandı.")
