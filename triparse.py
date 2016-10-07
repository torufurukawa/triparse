"""Parse PDF that contains triathlon race result"""

import sys
from io import StringIO
from PyPDF2 import PdfFileReader


def main():
    reader = PdfFileReader(open(sys.argv[1], 'rb'))
    page_count = reader.getNumPages()
    page = reader.getPage(0)


if __name__ == '__main__':
    main()
