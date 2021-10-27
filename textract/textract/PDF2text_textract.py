# textract
import os
import textract

from pathlib import Path


def get_text_w_textract(method='') -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa

    byte_text = textract.process(file_loc, language='ger',)  # noqa
    text = byte_text.decode('utf-8')
    print(text)


if __name__ == "__main__":
    get_text_w_textract(method="pdfminer")
    get_text_w_textract(method="pdftotext")
