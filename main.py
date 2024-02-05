from fastapi import FastAPI
from PyPDF2 import PdfReader
from pathlib import Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get texts from pdf
@app.get("/pdf/{file_path:path}")
async def read_pdf(file_path: Path):
    # Convert the Path to a string
    file_path_str = str(file_path)

    reader = PdfReader(file_path_str)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text


@app.get("/pdf/metadata/{file_path:path}")
async def metadata_pdf(file_path: Path):
    # Convert the Path to a string
    file_path_str = str(file_path)

    reader = PdfReader(file_path_str)
    meta = reader.metadata
    metaFile = {"author": meta.author, "title": meta.title, "subject": meta.subject, "creator": meta.creator,
                " producer": meta.producer, "creation_date": meta.creation_date,
                "modification_date": meta.modification_date}

    return metaFile


@app.get("/pdf/img/{file_path:path}")
async def getImages(file_path: Path):
    # Convert the Path to a string
    file_path_str = str(file_path)

    reader = PdfReader(file_path_str)
    number_of_pages = len(reader.pages)
    count = 0
    for i in range(number_of_pages):
        page = reader.pages[i]
        for image_object in page.images:
            with open(str(count) + image_object.name, "wb") as fp:
                fp.write(image_object.data)
                count += 1

    return {"message": "Images extracted successfully"}
