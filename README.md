# OCR - Digitalize Scans

## Dependencies

* [tesseract](https://tesseract-ocr.github.io/tessdoc/)
* [poppler](https://github.com/freedesktop/poppler)

```bash
sudo apt install tesseract-ocr tesseract-ocr-deu
sudo apt install poppler-utils
```

## Usage

Install python env:
```bash
poetry install
```

Convert pdfs and images to text files in the current directory:
```bash
poetry run digitize.py .
```

See `digitize.py -h` for more options.
