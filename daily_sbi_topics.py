"""
SBI新興国ウィークリーレポートをpdfで取得したあとテキストに変換します
"""
import os
import urllib.request

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def download_pdf(out_folder):
    """sbiのtopicを取得"""
    base_url = "https://search.sbisec.co.jp/v2/popwin/info/stock/market_report_fo_em_topic.pdf"
    urllib.request.urlretrieve(base_url, out_folder + "/" + base_url.split("/")[-1])


def convert_pdf_to_text(input_folder):
    """pdfからtextへ変換"""
    input_path = input_folder + '/market_report_fo_em_topic.pdf'
    output_path = input_path.replace(".pdf", ".txt")
    manager = PDFResourceManager()
    with open(output_path, "wb") as txt_output:
        with open(input_path, 'rb') as pdf_input:
            with TextConverter(manager, txt_output, laparams=LAParams()) as conv:
                interpreter = PDFPageInterpreter(manager, conv)
                for page in PDFPage.get_pages(pdf_input):
                    interpreter.process_page(page)


def edit_text_file(input_folder):
    """textを加工"""
    input_path = input_folder + '/market_report_fo_em_topic.txt'
    with open(input_path, encoding='utf-8', mode='r') as txt_input:
        temp = txt_input.read()
    with open(input_path, encoding='utf-8', mode='w') as txt_output:
        pos = temp.find('【韓国】')
        report_date = temp[:pos-1]
        report_date = report_date.replace('\n', '') + '\n'  # TODO: 日付と記事の間に改行を入れたい
        pos = temp.find('【ベトナム】')
        temp = temp[pos:]
        temp = temp.replace('\n', '')
        pos = temp.find('【インドネシア】')
        temp = temp[:pos-1]
        temp = temp.replace('  ▼指数チャート  ', '')
        pos = temp.find('    ')
        temp = temp[:pos-1]
        txt_output.write(report_date + temp)


work_folder = os.path.dirname(os.path.abspath(__file__)) + '/mysite/vietnam_research/static/vietnam_research/sbi_topics'
download_pdf(work_folder)
convert_pdf_to_text(work_folder)
edit_text_file(work_folder)
