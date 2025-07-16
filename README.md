Noto Multilanguage
==================

A cleanly merged, Unicode-rich NotoSans TTF font collection supporting over 70 writing systems from around the world — including Arabic, Japanese, Korean, Hebrew, Devanagari, Tamil, Armenian, Georgian, Ethiopic, and many others.

These fonts are optimized for:

- ✅ Multilingual user interfaces
- ✅ Globalized applications
- ✅ Cross-cultural publishing workflows

Each weight has been carefully subsetted and merged to include only unique characters, minimizing file size while maximizing language coverage.

⚠️ Disclaimer: All source fonts used in this collection are from Google’s official Noto Fonts project (https://github.com/notofonts), which is licensed under the Open Font License (OFL).
This repository is a custom-merged derivative optimized for bundled multilingual usage.

Supported Writing Systems
-------------------------

The following scripts are merged into each weight:

Alphabetical List:

Armenian, Arabic (Kufi, Nastaliq, Standard), Balinese, Bamum, Batak, Bengali, Buginese, Buhid, Canadian Aboriginal, Chakma, Cham, Cherokee, Coptic, Devanagari, Duployan, Ethiopic, Georgian, Glagolitic, Grantha, Gujarati, Gurmukhi, Hanunoo, Hebrew, HK Chinese, Japanese, Javanese, Kannada, Kayah Li, Khmer, Korean, Lao, Lao Looped, Lepcha, Limbu, Lisu, Malayalam, Mandaic, Math Symbols, Meetei Mayek, Mongolian, Myanmar, Nandinagari, New Tai Lue, NKo, Ogham, Ol Chiki, Oriya, Rejang, Runic, Samaritan, Saurashtra, Simplified Chinese, Sinhala, Sundanese, Syloti Nagri, Symbols, Syriac, Tagbanwa, Tai Le, Tai Tham, Tai Viet, Tamil, Telugu, Thaana, Thai, Tifinagh, Vai, Yi, and Nushu.

Font Weights Available
----------------------

Each of the following weights has a full multilingual TTF file:

- Thin
- Light
- Regular
- Medium
- SemiBold
- Bold
- ExtraBold
- Black

Each font is named:

NotoSansMultilanguage-<Weight>.ttf

Merging Strategy
----------------

- Fonts are merged only when they contribute unique Unicode characters.
- No duplicate glyphs are included.
- Complex tables (GSUB, GPOS, GDEF, MATH) are dropped for optimization.

Folder Structure
----------------

fonts/                # Input fonts organized by weight
NotoUniversalOutput/  # Output directory with final merged TTFs
TempSubsetFonts/      # Temporary folder (auto-deleted after process)
merge_log.txt         # Full log of included files and characters
