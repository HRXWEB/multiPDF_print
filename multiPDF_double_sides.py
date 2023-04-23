import sys
import os
import logging
from typing import List, Any

from pdfrw import PdfReader, PdfWriter, PdfName, PdfDict

"""
usage: python multiPDF_double_sides.py dir print_type out_f
example: python multiPDF_double_sides.py ./ [0, 1, 0, 1] demo
Creates: out_f.pdf
additionally, the order of the pdf files is sorted by alphabetical order, maybe not same as the order in your operating system, please check it.
"""

def blankPage(template):
    x = PdfDict()
    x.Type = PdfName.Page
    x.Contents = PdfDict(stream="")
    x.MediaBox = template.inheritable.MediaBox
    return x

class multiPdfPrint:
    """print mulitple pdf files in one time
    """
    def __init__(self, dir:str, print_type:List[int], out_f:str) -> None:
        """
        Args:
            dir (str): the directory of the pdf files
            print_type (List[int]): 0 means print in double sides, 1 means print in single sides. example: [0, 1, 0, 1]
            out_f (str): the output pdf file name
        """
        self.dir = dir
        self.print_type = print_type
        if out_f.endswith('.pdf'):
            self.out_f = PdfWriter(out_f)
        else:
            self.out_f = PdfWriter(out_f + '.pdf')
        self.logger = self._init_logger()
    
    def _init_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        return logger

    def sort_by_name(self, files:List[str]) -> List[str]:
        return sorted(files, key=lambda x: x.split('.pdf')[0])

    def get_pdf_files(self) -> List[str]:
        pdf_files = []
        other_files = False

        for f in os.listdir(self.dir):
            if f.endswith('.pdf'):
                pdf_files.append(os.path.join(self.dir, f))
            else:
                other_files = True
        if other_files:
            print('There are other format files in the directory, but dont worry. Only pdf file will be processed.')
        pdf_files = self.sort_by_name(pdf_files)
        self.logger.warning('The order of the pdf files is sorted by alphabetical order, maybe not same as the order in your operating system, please check it.')
        self.logger.info('The oeder of pdf files are: {}'.format(pdf_files))
        return pdf_files
    
    def add_file(self, print_type:int, inp_f:str) -> None:
        inp_f = PdfReader(inp_f)
        pages:List = inp_f.pages
        if print_type == 0:
            if len(pages) % 2 == 1:
                pages.append(blankPage(pages[0]))
            self.out_f.addpages(pages)
        elif print_type == 1:
            for i in range(len(pages)):
                self.out_f.addpage(pages[i])
                self.out_f.addpage(blankPage(pages[i]))
        else:
            raise ValueError('The print type should be 0 or 1')
    
    def get_out_f(self, ):
        pdf_files = self.get_pdf_files()
        assert len(pdf_files) == len(self.print_type), 'The number of pdf files should be same as the number of print type'
        for inp_f, p_type in zip(pdf_files, self.print_type):
            self.add_file(p_type, inp_f)
        self.out_f.write()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.get_out_f()

def main():
    dir = sys.argv[-3]
    print_type = sys.argv[-2]
    outp_f = sys.argv[-1]

    print_type = [int(i) for i in print_type.split(',')]
    printPDF = multiPdfPrint(dir, print_type, outp_f)
    printPDF()

if __name__ == '__main__':
    main()
