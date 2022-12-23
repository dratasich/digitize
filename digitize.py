#!/usr/bin/env python3

# %%
import argparse
import glob
import os

import pytesseract
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
args = parser.parse_args()

# %% get inputs for OCR (images in directory)
files = glob.glob(f"{args.path}/**/*.jpg", recursive=args.recursive)

# %% load images
for f in files:
    try:
        image = Image.open(f)
        print(f"File '{f}': {image.format_description} {image.mode} {image.info}")
        print(f"Run tesseract on {f}...")
        text = pytesseract.image_to_string(image, lang="eng+deu")
        outputfile = f"{os.path.splitext(f)[0]}_ocr.txt"
        with open(outputfile, "w") as o:
            o.write(text)
        print(f"Wrote {outputfile}")
    except:
        print(f"Failes to digitize {f}")
