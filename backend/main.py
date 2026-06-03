from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.middleware.cors import CORSMiddleware

import os

# Drive integration removed — storing uploads locally

app = FastAPI()

# Allow CORS from frontend during local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@app.post("/upload")
async def upload_invoice(
    invoice: UploadFile = File(...)
):

    file_path = (
        f"{UPLOAD_FOLDER}/{invoice.filename}"
    )

    with open(file_path, "wb") as f:

        contents = await invoice.read()

        f.write(contents)

    size = os.path.getsize(file_path)

    return {
        "message": "Uploaded Successfully (stored locally)",
        "filename": invoice.filename,
        "path": file_path,
        "size": size
    }