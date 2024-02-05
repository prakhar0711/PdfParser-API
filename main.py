from fastapi import FastAPI
from PyPDF2 import PdfReader

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get texts from pdf
@app.get("/pdf/{file_name}")
async def read_pdf(file_name: str):
    reader = PdfReader(file_name)
    number_of_pages = len(reader.pages)
    text = ''
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text


@app.get("/pdf/metadata/{file_name}")
async def metadata_pdf(file_name: str):
    reader = PdfReader(file_name)
    meta = reader.metadata
    metaFile = {"author": meta.author, "title": meta.title, "subject": meta.subject, "creator": meta.creator,
                " producer": meta.producer, "creation_date": meta.creation_date,
                "modification_date": meta.modification_date}

    return metaFile


@app.get("/pdf/img/{file_name}")
async def getImages(file_name: str):
    reader = PdfReader(file_name)
    number_of_pages = len(reader.pages)
    count = 0
    for i in range(number_of_pages):
        page = reader.pages[i]
        for image_object in page.images:
            with open(str(count) + image_object.name, "wb") as fp:
                fp.write(image_object.data)
                count += 1
