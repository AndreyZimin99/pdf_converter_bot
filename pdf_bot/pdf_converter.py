from gtts import gTTS
import pdfplumber
from pathlib import Path


def pdf_to_mp3(file_path='pdf_files/algorithms_1.pdf', language='en'):
    if Path(file_path).is_file() and Path(file_path).suffix == '.pdf':
        print(f'PDF-file {Path(file_path).name} converting to mp3.')
        with pdfplumber.PDF(open(file=file_path, mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        text = ''.join(pages).replace('\n', '')
        my_audio = gTTS(text=text, lang=language)
        file_name = Path(file_path).stem
        my_audio.save(f'{file_name}.mp3')
        print(f'{file_name}.mp3 saved succesfully!')
    else:
        raise 'File not exists, check the file path'
