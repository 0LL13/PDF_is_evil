import os
import pdfplumber

from pathlib import Path


def def_header_and_boxes(page):
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

    bounding_box_right = (0.5 * float(page.width),
                          0.1 * float(page.height),
                          page.width,
                          page.height)

    bounding_box_header = (0,
                           0,
                           page.width,
                           0.1 * float(page.height))

    return bounding_box_header, bounding_box_left, bounding_box_right


def get_text_w_pdfplumber(file_loc: str = None) -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    # bgbl too difficult:
    # file_loc = os.path.join(__location__, "PDFs/bgbl1_2021_75.pdf")  # noqa
    # file_loc = os.path.join(__location__, "PDFs/percentages_float_and_high_numbers.pdf")  # noqa
    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa

    pdf = pdfplumber.open(file_loc)

    inp = input("All pages? y/N - if no, only first page will be extracted")
    if inp == "y":
        text = ''
        for page in pdf.pages:
            header_bbox, left_bbox, right_bbox = def_header_and_boxes(page)

            header = page.crop(header_bbox)
            header_text = header.extract_text()
            if header_text:
                header_text = "\n\nheader:\n" + header_text
            else:
                header_text = "\nheader:\n"

            left_box = page.crop(left_bbox)
            left_box_text = left_box.extract_text()
            if left_box_text:
                left_box_text = "\nleft_box:\n" + left_box_text
            else:
                left_box_text = "\nleft_box:\n"

            right_box = page.crop(right_bbox)
            right_box_text = right_box.extract_text()
            if right_box_text:
                right_box_text = "\nright_box:\n" + right_box_text
            else:
                right_box_text = "\nright_box:\n"

            for text_el in [header_text, left_box_text, right_box_text]:
                if text_el:
                    text = text + text_el
    else:
        text = ''
        page = pdf.pages[0]
        header, left_box, right_box = def_header_and_boxes(page)

        header_text = header.extract_text()
        left_box_text = left_box.extract_text()
        right_box_text = right_box.extract_text()
        text = text + header_text + left_box_text + right_box_text

    pdf.close()

    return text


if __name__ == "__main__":
    from contextlib import redirect_stdout

    text = get_text_w_pdfplumber()
    print(text)
    with open("result.txt", "w") as fout:
        with redirect_stdout(fout):
            print(text)

#     header, left_col, right_col = get_text_w_pdfplumber()
#     print(header)
#     print()
#     print(left_col)
#     print()
#     print(right_col)
