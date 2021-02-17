from datetime import timedelta
from fastapi.encoders import jsonable_encoder
import minio
from pydantic import BaseModel
from starlette.responses import JSONResponse
from .config import FILESTORAGE_PATH, MINIO_URL, MINIO_ACCESSKEY, MINIO_SECRET
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable

from fastapi import UploadFile


def create_aliased_response(model: BaseModel) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(model, by_alias=True))


def save_upload_file(upload_file: UploadFile, destinationFilename: str) -> None:

    destination = Path(FILESTORAGE_PATH).joinpath(destinationFilename)
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def generate_upload_url(bucket: str, object: str):
    client = minio(
        MINIO_URL,
        access_key=MINIO_ACCESSKEY,
        secret_key=MINIO_SECRET,
        secure=False
    )

    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(object)
    url = client.get_presigned_url(
        "PUT",
        bucket,
        "my-object",
        expires=timedelta(days=1),
    )
    return url
