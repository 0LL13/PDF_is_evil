import os
import requests

from pathlib import Path

import PyPDF3
from PyPDF3 import PdfFileWriter
from PyPDF3 import PdfFileReader


def slice_pdf(file_loc=None):
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    file_loc = os.path.join(__location__, 'Id=MMP16_2F11_598_600.pdf')

    input_pdf = PdfFileReader(file_loc)
    output = PdfFileWriter()
    output.addPage(input_pdf.getPage(0))
    with open("first_page.pdf", "wb") as output_stream:
        output.write(output_stream)


def get_sample_pdfs():
    base = 'https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument?'
    URLS = {
        # "url1": '{}Id=MMP14%2F138|16018|16019'.format(base),

        # Fragezeichen, Ausrufezeichen, 18.400, Dr., 8. Februar
        "url2": '{}Id=MMP16%2F139|14617|14630'.format(base),

        # zahlreiche Unterbrechungen, ein einzelnes Wort ("immer") ohne Kontext
        "url3": '{}Id=MMP16%2F140|14760|14768'.format(base),

        # linke Spalte und rechte Spalte nicht auf der gleichen Höhe
        # --> Abruszat's Rede rechte Spalte mit Sätzen aus linker Spalte
        "url4": '{}Id=MMP15%2F57|5694|5696'.format(base),

        # Zwei Nachnamen, ein Zitat - verliert einen Absatz (des Vorredners)
        # Einzelnes Wort ("intensiver") ohne Kontext
        "url5": '{}Id=MMP16%2F8|542|544'.format(base),

        # der obere Teil der rechten Spalte wird zu früh wiedergegeben: linke
        # und rechte Spalte werden gemischt
        "url6": '{}Id=MMP14%2F4|175|187'.format(base),

        # "url7": '{}Id=MMP14%2F149|17408|17423'.format(base),
        # will miss out first sentence on page 8324 if _fill_boxes has
        # y0 >= Y_HEADER --> changed to y0 > Y_HEADER works
        # "url8": '{}Id=MMP14%2F72|8323|8332'.format(base),
        # "url9": '{}Id=MMP14%2F149|17408|17423'.format(base),

        # will return empty lists for columns
        "url10": '{}Id=MMP14%2F56|6267|6269'.format(base),

        # "url11": '{}Id=MMP14%2F120|13963|13967'.format(base),
        # "url12": '{}Id=MMP14%2F56|6272|6277'.format(base),
    }
    urls = ["url" + str(i+1) for i in range(12)]

    URLs = []
    for url in urls:
        URL = URLS[url]
        URLs.append(URL)

    return URLs


def download_pdfs(URLs):
    for url in URLs:
        response = requests.get(url)
        file_name = f'{url}' + '.pdf'
        with open(file_name, 'wb') as fout:
            fout.write(response.content)


def get_text_w_pypdf3(file_loc=None) -> str:
    # https://stackoverflow.com/a/4060259/6597765
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))  # noqa
    path = Path(__location__)
    __location__ = path.parent.parent.absolute()

    file_loc = os.path.join(__location__, "PDFs/left_col_bottom_to_right_col_top.pdf")  # noqa

    pdfFileObj = open(file_loc, 'rb')
    pdfReader = PyPDF3.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()

    return text


if __name__ == "__main__":
    text = get_text_w_pypdf3()
    print(text)
