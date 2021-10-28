import os
import pdfplumber

from pathlib import Path


def get_text_w_pdfplumber(file_loc: str = None) -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    # file_loc = os.path.join(__location__, "PDFs/percentages_float_and_high_numbers.pdf")  # noqa
    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa

    pdf = pdfplumber.open(file_loc)
    page = pdf.pages[0]
    # print(page.extract_text())

    # ## bounding_box parameters ###
    #
    # x0: distance left border of page to left border of box
    # top: distance top of page to top of box
    # x1: distance left border of page to right border of box
    # bottom: distance top of page to bottom of box
    #
    # bounding_box: (x0, top, x1, bottom)
    # ##

    bounding_box_left = (0,
                         0.1 * float(page.height),
                         0.48 * float(page.width),
                         page.height)
    left_box = page.crop(bounding_box_left)
    left_box_text = left_box.extract_text()

    bounding_box_right = (0.5 * float(page.width),
                          0.1 * float(page.height),
                          page.width,
                          page.height)
    right_box = page.crop(bounding_box_right)
    right_box_text = right_box.extract_text()

    bounding_box_header = (0,
                           0,
                           page.width,
                           0.1 * float(page.height))
    header = page.crop(bounding_box_header)
    header_text = header.extract_text()

    pdf.close()

    return header_text, left_box_text, right_box_text


if __name__ == "__main__":
    header, left_col, right_col = get_text_w_pdfplumber()
    print(header)
    print()
    print(left_col)
    print()
    print(right_col)
