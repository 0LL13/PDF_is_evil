import os

from pathlib import Path

import PyPDF3
from PyPDF3 import PdfFileWriter
from PyPDF3 import PdfFileReader


def slice_pdf(file_loc=None):
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    # file_loc = os.path.join(__location__, 'PDFs/Id=MMP16_2F11_598_600.pdf')  # done  # noqa
    file_loc = os.path.join(__location__, 'PDFs/Id=MMP16%2F114_11808_11810.pdf')  # noqa

    input_pdf = PdfFileReader(file_loc)
    output = PdfFileWriter()
    output.addPage(input_pdf.getPage(2))
    # file_name = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # done # noqa
    file_name = os.path.join(__location__, "PDFs/percentages_float_and_high_numbers.pdf")  # noqa
    with open(file_name, "wb") as output_stream:
        output.write(output_stream)


def get_text_w_pypdf3(file_loc=None) -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    # file_loc = os.path.join(__location__, "PDFs/percentages_float_and_high_numbers.pdf")  # noqa
    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # done # noqa

    pdfFileObj = open(file_loc, 'rb')
    pdfReader = PyPDF3.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()

    return text


if __name__ == "__main__":
    text = get_text_w_pypdf3()
    print(text)
