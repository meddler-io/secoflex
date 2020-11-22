from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.files import (
    File,
    FileInCreate,
    FileInResponse,
    FileMetadata,
    FileInDb,
    FileCreateInResponse,
    FilesInResponse,
    FileUploadResponse
)

from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, files_collection_name




async def create_file(conn: AsyncIOMotorClient, file: FileInCreate) -> FileCreateInResponse:
    file.createFileId()
    dbfile = FileInDb( **file.dict()  )
    row = await conn[database_name][files_collection_name].insert_one(dbfile.dict())
    row = await conn[database_name][files_collection_name].find_one( {"_id": row.inserted_id} )

    fileResponse = FileCreateInResponse(**row)
    fileResponse.createToken()
    return fileResponse



async def get_file_from_db(conn: AsyncIOMotorClient, fileid: str) -> FileUploadResponse:
    row = await conn[database_name][files_collection_name].find_one( {"fileid": fileid} )
    fileResponse = FileUploadResponse(**row)
    return fileResponse



async def delete_file_from_db(conn: AsyncIOMotorClient, fileid: str) :
    await conn[database_name][files_collection_name].delete_one( {"fileid": fileid} )



async def init_file_upload(conn: AsyncIOMotorClient, fileid: str) -> FileCreateInResponse:

    row = await conn[database_name][files_collection_name].update_one( { "fileid": fileid , "state": "CREATED" } , { "$set" : { "state": "UPLOADING" } } )
    if row.modified_count == 1:
        return True
    return False


async def finished_file_upload(conn: AsyncIOMotorClient, fileid: str) -> FileCreateInResponse:

    row = await conn[database_name][files_collection_name].update_one( { "fileid": fileid  } , { "$set" : { "state": "UPLOADED" } } )
    if row.modified_count == 1:
        return True
    return False


async def failed_file_upload(conn: AsyncIOMotorClient, fileid: str) -> FileCreateInResponse:

    row = await conn[database_name][files_collection_name].update_one( { "fileid": fileid  } , { "$set" : { "state": "FAILED" } } )
    if row.modified_count == 1:
        return True
    return False



async def rename_file_db(conn: AsyncIOMotorClient, fileid: str , filename: str) -> FileCreateInResponse:

    row = await conn[database_name][files_collection_name].update_one( { "fileid": fileid  } , { "$set" : { "filename": filename  } } )
    if row.modified_count == 1:
        return True
    return False





async def get_files(conn: AsyncIOMotorClient ) -> FilesInResponse:

    cursor = conn[database_name][files_collection_name].find( {  "state": "UPLOADED" })
    files: List[FileInDb] = []

    for document in await cursor.to_list(length=100):
        files.append(document)

    return FilesInResponse(files=files)




async def update_file(conn: AsyncIOMotorClient ) -> FilesInResponse:

    cursor = conn[database_name][files_collection_name].find()
    files: List[FileInDb] = []

    for document in await cursor.to_list(length=100):
        files.append(document)

    return FilesInResponse(files=files)


