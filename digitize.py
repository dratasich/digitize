#!/usr/bin/env python3

# %%
import argparse
import glob
import os

import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# %%
desc = "Digitize scans and pdfs - convert images and pdfs to text files."
parser = argparse.ArgumentParser(description=desc)
parser.add_argument(
    "path",
    default=".",
    type=str,
    help=f"""Directory of files to digitize.""",
)
parser.add_argument(
    "-r",
    "--recursive",
    action="store_true",
    default=False,
    help=f"""Recursively search the directory for files to convert.""",
)
parser.add_argument(
    "-e",
    "--extension",
    type=str,
    nargs="+",
    default=["jpg", "png", "pdf"],
    help=f"""Extensions of files to search for.""",
)
args = parser.parse_args()

# %% get inputs for OCR (images in directory)
files = []
for ext in args.extension:
    files.extend(glob.glob(f"{args.path}/**/*.{ext}", recursive=args.recursive))

# %% save text:
def save(text: str, to: str) -> bool:
    with open(to, "w") as o:
        o.write(text)
    print(f"Wrote {to}")


# %% convert pdf
def pdf2text(path: str) -> str:
    print(f"Run pdf reader on {f}...")
    reader = PyPDF2.PdfReader(f)
    print(
        f"File '{f}': {len(reader.pages)} page(s) {reader.metadata} {reader.pdf_header}"
    )
    text = "".join(reader.pages[0].extract_text())
    if len(text) < 5:
        # no text in pdf -> convert to image and try with ocr
        doc = convert_from_path(path)
        text = "".join([pytesseract.image_to_string(page) for page in doc])
    return text


# %% convert all files
for f in files:
    try:
        outputfile = f"{os.path.splitext(f)[0]}_ocr.txt"
        if str(f).endswith(".pdf"):
            text = pdf2text(f)
        else:
            print(f"Run tesseract on {f}...")
            image = Image.open(f)
            print(f"File '{f}': {image.format_description} {image.mode} {image.info}")
            text = pytesseract.image_to_string(image, lang="eng+deu")
        if len(text) > 5:
            save(text, outputfile)
    except Exception as e:
        print(f"Failed to digitize {f}: {e}")
