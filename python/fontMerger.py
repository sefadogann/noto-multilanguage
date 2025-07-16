import os
import shutil
from fontTools.ttLib import TTFont
from fontTools.merge import Merger, Options
from gftools.fix import rename_font
from fontTools.subset import Subsetter, Options as SubsetOptions

base_input_dir = "fonts"
output_dir = "NotoUniversalOutput"
temp_subset_dir = "TempSubsetFonts"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(temp_subset_dir, exist_ok=True)

weights = ["Thin", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]

def is_valid_font(path):
    name = os.path.basename(path).lower()
    return "condensed" not in name and name.endswith(".ttf")

# Log dosyası başlat
log_lines = []

for weight in weights:
    weight_dir = os.path.join(base_input_dir, weight)
    if not os.path.exists(weight_dir):
        print(f"⚠️  {weight} klasörü yok, atlanıyor.")
        continue

    font_paths_all = [os.path.join(weight_dir, f) for f in os.listdir(weight_dir) if is_valid_font(f)]
    if len(font_paths_all) < 2:
        print(f"❌ Yeterli font yok, {weight} için atlanıyor.")
        continue

    valid_fonts = []
    rejected_fonts = []
    for path in font_paths_all:
        try:
            font = TTFont(path)
            upem = font["head"].unitsPerEm
            if upem == 1000:
                valid_fonts.append(path)
            else:
                rejected_fonts.append((os.path.basename(path), upem))
        except Exception as e:
            print(f"⚠️  {os.path.basename(path)} okunamadı: {e}")

    if rejected_fonts:
        print(f"⚠️  {weight} için unitsPerEm uyumsuz fontlar atlandı:")
        for name, upem in rejected_fonts:
            print(f"   - {name} → unitsPerEm = {upem}")

    print(f"\n🔢 {weight} için fontların glif sayıları ve karakter kümeleri:")

    cumulative_codepoints = set()
    subset_fonts = []

    for path in valid_fonts:
        font = TTFont(path)
        cmap_table = next((t for t in font["cmap"].tables if t.isUnicode()), None)
        if not cmap_table:
            print(f"⚠️  {os.path.basename(path)} için Unicode cmap bulunamadı, atlanıyor.")
            continue

        cps = set(cmap_table.cmap.keys())
        unique_cps = cps - cumulative_codepoints
        if not unique_cps:
            print(f"   - {os.path.basename(path)} tamamen tekrar, atlanıyor.")
            continue

        cumulative_codepoints.update(unique_cps)

        # Subset işlemi
        subset_font = TTFont(path)
        options = SubsetOptions()
        options.drop_tables += ['GSUB', 'GPOS', 'GDEF']
        subsetter = Subsetter(options=options)
        subsetter.populate(unicodes=unique_cps)
        subsetter.subset(subset_font)

        subset_path = os.path.join(temp_subset_dir, f"subset_{os.path.basename(path)}")
        subset_font.save(subset_path)
        subset_fonts.append(subset_path)

        print(f"   - {os.path.basename(path)}: {len(unique_cps)} unique karakter alındı")
        log_lines.append(f"{weight} → {os.path.basename(path)} → {len(unique_cps)} karakter")

    print(f"🔢 {weight} için toplam unique karakter sayısı: {len(cumulative_codepoints)}")
    print(f"🔁 Birleştiriliyor: {weight} ({len(subset_fonts)} alt küme font)...")

    if not subset_fonts:
        print(f"❌ Hiçbir yeni karakter kalmadı, {weight} için atlandı.")
        continue

    try:
        merger = Merger(options=Options(drop_tables=["vmtx", "vhea", "MATH"]))
        merged_font = merger.merge(subset_fonts)

        new_name = f"NotoSans Multilanguage {weight}"
        rename_font(merged_font, new_name)

        output_path = os.path.join(output_dir, f"NotoSansMultilanguage-{weight}.ttf")
        merged_font.save(output_path)
        print(f"✅ Kaydedildi: {output_path}")
        log_lines.append(f"✅ {weight} font başarıyla kaydedildi: {output_path}")
    except Exception as e:
        print(f"❌ Hata: {weight} için birleştirme başarısız oldu. Sebep: {e}")
        log_lines.append(f"❌ {weight} için hata: {e}")

# 📄 Log dosyasını yaz
log_path = os.path.join(output_dir, "merge_log.txt")
with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write("\n".join(log_lines))
print(f"\n📄 Log dosyası yazıldı: {log_path}")

# 🧹 Temp klasörünü sil
try:
    shutil.rmtree(temp_subset_dir)
    print(f"🧹 TempSubsetFonts klasörü silindi: {temp_subset_dir}")
except Exception as e:
    print(f"⚠️ TempSubsetFonts silinemedi: {e}")
