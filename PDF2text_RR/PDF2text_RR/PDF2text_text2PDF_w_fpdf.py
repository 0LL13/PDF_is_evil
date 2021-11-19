import os
import pdfplumber
import textwrap3
import textract

from fpdf import FPDF
from pathlib import Path


class PDF2TextRR:
    """
    This is a somewhat cumbersome thing to do:
        - change PDF (header, two columns) to text using pdfplumber
        - change text to PDF using fpdf
    The reason is that this way I can create a PDF that I can then extract with
    textract, which somehow creates a perfect dehyphened text. Since textract
    is missing lines when extracting the original PDF format, this detour is
    the best I came up with.
    """

    def __init__(self, fin_name: str = None):
        text = self.get_text_w_pdfplumber(fin_name)
        self.text_to_pdf(text)
        self.text = self.get_text_w_textract()

    def def_header_and_boxes(self, page: pdfplumber.page.Page) -> tuple:

        # ## bounding_box parameters ###########################
        #
        # x0: distance left border of page to left border of box
        # top: distance top of page to top of box
        # x1: distance left border of page to right border of box
        # bottom: distance top of page to bottom of box
        #
        # bounding_box: (x0, top, x1, bottom)
        # #######################################################

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

    def get_text_w_pdfplumber(self, fin_name: str = None) -> str:
        # https://stackoverflow.com/a/4060259/6597765
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
        path = Path(__location__)
        __location__ = path.parent.parent.absolute()

        if fin_name:
            file_loc = "PDFs/" + fin_name
            file_loc = os.path.join(__location__, file_loc)
        else:
            # file_loc = os.path.join(__location__, "PDFs/Id=MMP16%2F76_7798_7800.pdf")  # noqa
            file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa
        # The bounding_box values defined in def_header_and_boxes are tailored
        # to fit the "Landtag NRW" session protocols!
        pdf = pdfplumber.open(file_loc)

        text = ''
        for page in pdf.pages:
            header_bbox, left_bbox, right_bbox = self.def_header_and_boxes(page)  # noqa

            header = page.crop(header_bbox)
            header_text = header.extract_text()
            if header_text:
                header_text = "\n\nheader\n" + header_text
            else:
                header_text = "\nheader\n"

            left_box = page.crop(left_bbox)
            left_box_text = left_box.extract_text()
            if left_box_text:
                left_box_text = "\npage\n" + left_box_text
            else:
                left_box_text = "\npage\n"

            right_box = page.crop(right_bbox)
            right_box_text = right_box.extract_text()
            if right_box_text:
                right_box_text = right_box_text
            else:
                right_box_text = "\n"

            for text_el in [header_text, left_box_text, right_box_text]:
                if text_el:
                    text = text + text_el
        pdf.close()

        return text

    def text_to_pdf(self, text: str) -> None:
        text = text.encode('utf-8')

        # It's absolutely necessary to provide a ttf, otherwise fpdf will do
        # some shenanigans in method "normalize_text" which checks if text is a
        # subset of unifont and if not, tries to do a decode("latin-1") on the
        # text, which results in a UnicodeEncodeError.
        # The ttf used here ("Arimo") came from:
        # https://www.fontsquirrel.com/fonts/list/language/german/50

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
        ttf_loc = os.path.join(__location__, "Arimo.ttf")  # noqa

        # Defining location and name for the PDF file (will be always overwritten).  # noqa
        path = Path(__location__)
        __location__ = path.parent.parent.absolute()
        fout_loc = os.path.join(__location__, "PDFs/output.pdf")  # noqa

        # https://stackoverflow.com/a/64877141/6597765
        a4_width_mm = 210
        pt_to_mm = 0.35
        fontsize_pt = 10
        fontsize_mm = fontsize_pt * pt_to_mm
        margin_bottom_mm = 10
        character_width_mm = 7 * pt_to_mm
        width_text = a4_width_mm / character_width_mm

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_auto_page_break(True, margin=margin_bottom_mm)
        pdf.add_page()
        pdf.add_font('Arimo', '', ttf_loc, uni=True)
        pdf.set_font('Arimo', '', 10)

        splitted = text.splitlines()
        for line in splitted:
            line = line.decode('utf-8')
            lines = textwrap3.wrap(line, width_text)

            if len(lines) == 0:
                pdf.ln()

            for wrap in lines:
                pdf.cell(0, fontsize_mm, wrap, ln=1)

        pdf.output(fout_loc, 'F')

    def get_text_w_textract(method='') -> str:
        # https://stackoverflow.com/a/4060259/6597765
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
        path = Path(__location__)
        __location__ = path.parent.parent.absolute()

        file_loc = os.path.join(__location__, "PDFs/output.pdf")  # noqa

        byte_text = textract.process(file_loc, language='ger',)  # noqa
        text = byte_text.decode('utf-8')

        return text


if __name__ == "__main__":
    from contextlib import redirect_stdout

    rinse = PDF2TextRR()
    text = rinse.text
    print(text)
    with open("result.txt", "w") as fout:
        with redirect_stdout(fout):
            print(text)
