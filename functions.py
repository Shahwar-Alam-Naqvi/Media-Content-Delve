from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import json
import ast
import requests

def convert_pdf_to_txt_pages(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    size = 0
    c = 0
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(path):
      interpreter.process_page(page)
      t = retstr.getvalue()
      if c == 0:
        texts.append(t)
      else:
        texts.append(t[size:])
      c = c+1
      size = len(t)
    # text = retstr.getvalue()

    # fp.close()
    device.close()
    retstr.close()
    return texts, nbPages


def convert_pdf_to_txt_file(path):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    # fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    file_pages = PDFPage.get_pages(path)
    nbPages = len(list(file_pages))
    for page in PDFPage.get_pages(path):
      interpreter.process_page(page)
      t = retstr.getvalue()
    # text = retstr.getvalue()

    # fp.close()
    device.close()
    retstr.close()
    return t, nbPages


def confirm_list(content):
    if isinstance(content, str):
        try:
            # Use literal_eval to safely evaluate the string as a list
            actual_list = ast.literal_eval(content)
            return actual_list
        except ValueError as e:
            print(f"Error: {e}")
            print("The string could not be converted to a list.")
            return content
    else:
        print("The variable is not a string.")
        return content
    
def limit_to_4096_characters(input_string):
    if len(input_string) > 4096:
        return input_string[:4096]
    else:
        return input_string
      
      
def save_image_from_url(url, path):
    response = requests.get(url)
    if response.status_code == 200:  # OK
        with open(path, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Error retrieving image from {url}")