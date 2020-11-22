from typing import Optional
from ....core.utils import save_upload_file
from fastapi import APIRouter, Body, Depends ,HTTPException
from fastapi import FastAPI, File, UploadFile, Query
from ....core.jwt import get_current_user_authorizer
from ....db.mongodb import AsyncIOMotorClient, get_database
from starlette.responses import FileResponse
from ....models.files import FileInCreate, FileInResponse, FileMetadata, CreateFileInResponse, FilesInResponse, FileCreateInResponse, FileUpload, FileUploadResponse ,FileRename
from ....crud.file import create_file as save_file
from ....crud.file import get_files , init_file_upload , failed_file_upload , finished_file_upload, get_file_from_db, rename_file_db, get_file_from_db, delete_file_from_db
router = APIRouter()
from ....core.config import FILESTORAGE_PATH

from pathlib import PurePath

# Create/Touch file 
@router.post("/file/create", response_model=FileCreateInResponse, tags=["file"])
async def create_file(
            file: FileInCreate = Body(...,),
            db: AsyncIOMotorClient = Depends(get_database),
        ):

    file_in_response = await save_file(db ,file)
    return file_in_response


# Upload file 
@router.post("/file/upload" , response_model= FileUploadResponse , tags=["file"])
async def upload_file(
            token: str,
            file: UploadFile = File(...),
            db: AsyncIOMotorClient = Depends(get_database),
           
        ):

    decoded_token = FileUpload( token=token  ).decodeToken()
    fileid = decoded_token.fileid
    if await init_file_upload( db , fileid ) == False:
        raise HTTPException(status_code=401, detail="File upload has already been started/ finished. ")

    try:
        # save_upload_file(file , fileid  +   PurePath( file.filename ).suffix )
        save_upload_file(file , fileid  )
        await finished_file_upload(db, fileid)
    except:
        await failed_file_upload(db, fileid)

    return await get_file_from_db(db, fileid=fileid)


# Change Filename 
@router.post("/file/rename" , response_model= FileUploadResponse , tags=["file"])
async def rename_file(
            file_rename: FileRename ,
            db: AsyncIOMotorClient = Depends(get_database),
           
        ):
    
    if await rename_file_db(db, file_rename.fileid, file_rename.filename) == False:
        raise HTTPException(status_code=401, detail="Coud not change filename. ")

    return await get_file_from_db(db, fileid=file_rename.fileid)





# Get file details
@router.get("/file", response_model=FilesInResponse, tags=["file"])
async def get_file(
            db: AsyncIOMotorClient = Depends(get_database),
             ):
    files = await get_files( db  )
    return files



# Update file's meta data
@router.put("/file/update", response_model=FileInResponse, tags=["file"])
async def update_file():
    return FileInResponse()


# Download file
# Upload file 
@router.get("/file/download/{fileid}"  , tags=["file"])
async def download_file(
            fileid: str,
            db: AsyncIOMotorClient = Depends(get_database),

        ):
        file_data = await get_file_from_db(db, fileid=fileid)
        file_path = PurePath( FILESTORAGE_PATH ).joinpath( file_data.fileid )
        return FileResponse(file_path, media_type='application/octet-stream',filename=file_data.filename)


# Delete file
@router.delete("/file/{fileid}"  , tags=["file"])
async def delete_file(
            fileid: str,
            db: AsyncIOMotorClient = Depends(get_database),

        ):
        await delete_file_from_db(db, fileid)
        return

