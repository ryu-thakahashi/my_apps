from PyPDF2 import PdfMerger
import os
import re

from pathlib import Path
from icecream import ic


dir_path = Path(__file__).resolve().parents[1]
raw_pdf_dir = dir_path / "raw_pdf"
res_pdf_dir = dir_path / "res_pdf"

raw_pdf_files = os.listdir(raw_pdf_dir)

unique_prefixes = set([file_name.split("_")[0] for file_name in raw_pdf_files])
ic(unique_prefixes)

merged_pdf_files = os.listdir(res_pdf_dir)
merged_pdf_prefixes = set([file_name.split("_")[0] for file_name in merged_pdf_files])

for prefix in unique_prefixes:
    if f"{prefix}_merged.pdf" in merged_pdf_files:
        print(f"{prefix}_merged.pdf はすでに存在しています。")
        continue

    target_pdfs = []
    for file_name in raw_pdf_files:
        if re.match(f"{prefix}_\d+.pdf", file_name):
            target_pdfs.append(file_name)
    ic(target_pdfs)

    # PdfMergerオブジェクトを作成
    merger = PdfMerger()

    # 各PDFを結合
    for pdf in target_pdfs:
        merger.append(raw_pdf_dir / pdf)

    # 結合したPDFを保存
    output_file = res_pdf_dir / f"{prefix}_merged.pdf"
    merger.write(output_file)
    merger.close()

    print(f"結合されたPDFは {output_file} に保存されました。")
