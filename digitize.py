#!/usr/bin/env python3

# %%
import argparse
import glob
import os

import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from PIL.ExifTags import TAGS

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
default_extensions = ["jpg", "png", "pdf"]
parser.add_argument(
    "-e",
    "--extension",
    type=str,
    nargs="+",
    default=default_extensions,
    help=f"""Extensions of files to search for (default: {default_extensions}).""",
)
default_exclude = ["IMG", "IMAG", "DSC"]
parser.add_argument(
    "--exclude",
    type=str,
    nargs="+",
    default=default_exclude,
    help=f"""Exclude files that contain default: {default_exclude}.""",
)
args = parser.parse_args()

# %% get inputs for OCR (images in directory)
# collect all files with the specified extensions
files = []
for ext in args.extension:
    files.extend(glob.glob(f"{args.path}/**/*.{ext}", recursive=args.recursive))
print(f"{len(files)} with extensions {args.extension}")
# exclude files given some patterns
for filename in files:
    for s in args.exclude:
        if s in filename:
            print(f"Drop {filename} because '{s}' is contained in the filename")
            files.remove(filename)
            break
print(f"{len(files)} files after excluding {args.exclude}")


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


# %% get all meta data fields from an image
def image_metadata(img: Image):
    """
    https://www.thepythoncode.com/article/extracting-image-metadata-in-python
    """
    exifdata = image.getexif()
    meta = {}
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        meta[tag] = data
    return meta


# %% convert all files
print("---")
for f in files:
    try:
        outputfile = f"{os.path.splitext(f)[0]}_ocr.txt"
        if str(f).endswith(".pdf"):
            text = pdf2text(f)
        else:
            print(f"Run tesseract on {f}...")
            image = Image.open(f)
            meta = image_metadata(image)
            print(f"File '{f}': {image.format_description} {image.mode} {meta}")
            text = pytesseract.image_to_string(image, lang="eng+deu")
        if len(text) > 5:
            save(text, outputfile)
    except Exception as e:
        print(f"Failed to digitize {f}: {e}")
