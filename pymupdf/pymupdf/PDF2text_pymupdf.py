import fitz
import os

from pathlib import Path


def get_text_w_pymupdf(file_loc=None) -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    # file_loc = os.path.join(__location__, "PDFs/bgbl1_2021_75.pdf")  # noqa
    # file_loc = os.path.join(__location__, "PDFs/percentages_float_and_high_numbers.pdf")  # noqa
    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa

    doc = fitz.open(file_loc)  # open document

    inp = input("All pages? y/N - if no, only first page will be extracted")
    if inp == "y":
        text = ''
        for page in doc:
            text += page.get_text()
    else:
        page = doc[0]
        text = page.get_text()

    doc.close()

    return text


if __name__ == "__main__":
    from contextlib import redirect_stdout

    text = get_text_w_pymupdf()
    with open("result.txt", "w") as fout:
        with redirect_stdout(fout):
            print(text)
    print(text)
