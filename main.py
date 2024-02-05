from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfReader
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get texts from pdf
@app.get("/pdf/{filename}")
async def read_pdf(filename: str):
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text


@app.get("/pdf/metadata/{filename}")
async def metadata_pdf(filename: str):
    reader = PdfReader(filename)
    meta = reader.metadata
    metaFile = {"author": meta.author, "title": meta.title, "subject": meta.subject, "creator": meta.creator,
                " producer": meta.producer, "creation_date": meta.creation_date,
                "modification_date": meta.modification_date}

    return metaFile


@app.get("/pdf/img/{filename}")
async def getImages(filename: str):
    reader = PdfReader(filename)
    number_of_pages = len(reader.pages)
    count = 0
    for i in range(number_of_pages):
        page = reader.pages[i]
        for image_object in page.images:
            with open(str(count) + image_object.name, "wb") as fp:
                fp.write(image_object.data)
                count += 1


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {"filename": file.filename}
