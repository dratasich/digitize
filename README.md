# OCR - Digitalize Scans

## Dependencies

* [tesseract](https://tesseract-ocr.github.io/tessdoc/)
* [PyPDF2](https://pypdf2.readthedocs.io/en/stable/)

```bash
sudo apt install tesseract-ocr tesseract-ocr-deu
```

Install python env:
```bash
poetry install
```

## Usage

Convert pdfs and images to text files in the current directory:
```bash
poetry run digitize.py .
```

See `digitize.py -h` for more options.
