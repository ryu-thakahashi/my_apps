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
        if not os.path.exists(self.raw_pdf_dir):
            raise FileNotFoundError(f"{self.raw_pdf_dir} が存在しません。")
        self.raw_pdf_files = os.listdir(self.raw_pdf_dir)

    def read_res_pdf_files(self):
        self.res_pdf_dir = self.dir_path / "res_pdf"
        if not os.path.exists(self.res_pdf_dir):
            os.makedirs(self.res_pdf_dir)
        self.merged_pdf_files = os.listdir(self.res_pdf_dir)

    def get_unique_prefixes(self):
        return self.get_unique_raw_prefixes() - self.get_unique_merged_prefixes()

    def get_unique_raw_prefixes(self):
        return set([file_name.split("_")[0] for file_name in self.raw_pdf_files])

    def get_unique_merged_prefixes(self):
        return set([file_name.split("_")[0] for file_name in self.merged_pdf_files])

    def get_target_pdfs(self, prefix):
        return [
            file_name
            for file_name in self.raw_pdf_files
            if re.match(f"{prefix}_\d+.pdf", file_name)
        ]

    def merge_pdf(self, target_pdfs):
        merger = PdfMerger()
        for pdf in target_pdfs:
            merger.append(self.raw_pdf_dir / pdf)
        return merger

    def save_pdf(self, prefix, merger):
        output_file = self.res_pdf_dir / f"{prefix}_merged.pdf"
        merger.write(output_file)
        merger.close()
        print(f"結合されたPDFが保存されました。(prefix: {prefix}, path: {output_file})")

    def concat_pdf(self):
        for prefix in self.get_unique_prefixes():
            target_pdfs = self.get_target_pdfs(prefix)
            merger = self.merge_pdf(target_pdfs)
            self.save_pdf(prefix, merger)


if __name__ == "__main__":
    cp = ConcatPdf()
    cp.concat_pdf()
