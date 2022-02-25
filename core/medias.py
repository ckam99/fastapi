from fastapi import Path, UploadFile, File
from fastapi.responses import FileResponse
from typing import List
import shutil
import os
from core.settings import MEDIA_DIR, BASE_DIR
from core.exceptions import FileDoesntExistError


base_dir = BASE_DIR.joinpath(MEDIA_DIR)

if not os.path.exists(base_dir):
    os.mkdir(base_dir)


def upload_file(media: UploadFile = File(...)):
    with open(f'{base_dir}/{media.filename}', 'wb+') as buffer:
        shutil.copyfileobj(media.file, buffer)


def upload_multiple_files(files: List[UploadFile] = File(...)):
    for f in files:
        upload_file(f)


async def get_media(filename: str):
    path = f'{base_dir}/{filename}'
    if os.path.exists(path):
        return FileResponse(path)
    raise FileDoesntExistError('File does not exist!')
