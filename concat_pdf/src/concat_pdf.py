from PyPDF2 import PdfMerger
import os
import re

from pathlib import Path
from icecream import ic


class ConcatPdf:
    def __init__(self):
        self.dir_path = Path(__file__).resolve().parents[1]
        self.read_raw_pdf_files()
        self.read_res_pdf_files()

    def read_raw_pdf_files(self):
        """
        PDF ファイルの名前は {prefix}_{number}.pdf という形式で保存されていることを前提とする。
        """
        self.raw_pdf_dir = self.dir_path / "raw_pdf"
        self.raw_pdf_files = os.listdir(self.raw_pdf_dir)

    def read_res_pdf_files(self):
        self.res_pdf_dir = self.dir_path / "res_pdf"
        self.merged_pdf_files = os.listdir(self.res_pdf_dir)

    def is_created(self, prefix):
        return f"{prefix}_merged.pdf" in self.merged_pdf_files

    def get_unique_raw_prefixes(self):
        return set([file_name.split("_")[0] for file_name in self.raw_pdf_files])

    def get_unique_merged_prefixes(self):
        return set([file_name.split("_")[0] for file_name in self.merged_pdf_files])

    def get_target_pdfs(self, prefix):
        target_pdfs = []
        for file_name in self.raw_pdf_files:
            if re.match(f"{prefix}_\d+.pdf", file_name):
                target_pdfs.append(file_name)
        return target_pdfs

    def merge_pdf(self, target_pdfs):
        merger = PdfMerger()

        for pdf in target_pdfs:
            merger.append(self.raw_pdf_dir / pdf)
        return merger

    def save_pdf(self, prefix, merger):
        output_file = self.res_pdf_dir / f"{prefix}_merged.pdf"
        merger.write(output_file)
        merger.close()
        print(f"結合されたPDFは {output_file} に保存されました。")

    def concat_pdf(self):

        unique_prefixes = set(
            [file_name.split("_")[0] for file_name in self.raw_pdf_files]
        )
        ic(unique_prefixes)

        for prefix in unique_prefixes:
            if self.is_created(prefix):
                print(f"{prefix}_merged.pdf はすでに存在しています。")
                continue

            target_pdfs = self.get_target_pdfs(prefix)
            ic(target_pdfs)

            # 結合したPDFを保存
            merger = self.merge_pdf(target_pdfs)
            self.save_pdf(prefix, merger)


if __name__ == "__main__":
    cp = ConcatPdf()
    cp.concat_pdf()
