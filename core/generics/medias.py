from fastapi import Path, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List
import shutil
import os
from core.settings import MEDIA_DIR

base_dir = os.path.join(os.getcwd(), MEDIA_DIR)

if not os.path.exists(base_dir):
    os.mkdir(base_dir)


def upload_file(media: UploadFile = File(...)):
    with open(f'{base_dir}/{media.filename}', 'wb+') as buffer:
        shutil.copyfileobj(media.file, buffer)
    # file_name = os.getcwd()+"/images/"+image.filename.replace(" ", "-")
    # with open(file_name, 'wb+') as f:
    #     f.write(image.file.read())
    #     f.close()


def upload_multiple_files(files: List[UploadFile] = File(...)):
    for f in files:
        upload_file(f)


async def get_media(filename: str):
    path = f'{base_dir}/{filename}'
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(404, detail='File does not exist!')
