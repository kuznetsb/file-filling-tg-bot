import os
from PyPDF2 import PdfReader
from fpdf import FPDF

OFFER_TEMPLATE = "offer_template.pdf"
TABLE_HEADER = ("№", "Наименование", "Кол-во", "")


def create_table():
    pdf = FPDF()
    pdf.set_font("Times", size=12)
    pdf.add_page()
    with pdf.table() as table:
        header = table.row()
        header.cell()


def read_from_pdf(filename: str) -> str:
    reader = PdfReader(os.path.join("..", "files", "templates", filename))
    page = reader.pages[0]
    return page.extract_text()


def form_pdf_offer(filename: str):
    file_content = read_from_pdf(filename)
    table = create_table()


if __name__ == "__main__":
    form_pdf_offer(OFFER_TEMPLATE)
