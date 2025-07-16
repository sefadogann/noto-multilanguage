import os
from fontTools.ttLib import TTFont

def auto_fix_vertical_metrics(font_path, ascent=900, descent=-250, linegap=0):
    font = TTFont(font_path)

    # hhea tablosunu güncelle
    font["hhea"].ascent = ascent
    font["hhea"].descent = descent
    font["hhea"].lineGap = linegap

    # OS/2 tablosunu güncelle
    os2 = font["OS/2"]
    os2.sTypoAscender = ascent
    os2.sTypoDescender = descent
    os2.sTypoLineGap = linegap
    os2.usWinAscent = ascent
    os2.usWinDescent = abs(descent)

    # head tablosunu güncelle
    font["head"].yMax = ascent
    font["head"].yMin = descent

    font.save(font_path)
    print(f"✔ Updated: {font_path}")

def process_all_fonts_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(".ttf"):
            full_path = os.path.join(directory, filename)
            try:
                auto_fix_vertical_metrics(full_path)
            except Exception as e:
                print(f"⚠️ Error processing {filename}: {e}")

if __name__ == "__main__":
    folder_path = r"E:\Projects\exwalt\noto-multilanguage\NotoMultilanguageFonts"
    process_all_fonts_in_directory(folder_path)
