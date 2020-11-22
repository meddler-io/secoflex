from typing import Optional , List
from .dbmodel import DBModelMixin
from ..core.jwt import create_access_token, get_file_from_token
from pydantic import AnyUrl

from .rwmodel import RWModel

class FileMetadata(RWModel):
    filename: str
    filesize: str
    tags: List[str]
    filetype: str

class File(RWModel):
    filename: str
    metadata: FileMetadata
    filepath: str


class FileInDb(RWModel, DBModelMixin):
    filename: str
    metadata: Optional[FileMetadata]
    state: Optional[str] = "CREATED"
    fileid: Optional[str]


class FileInResponse(RWModel):
    filename: str
    metadata: Optional[FileMetadata]
    fileurl: str



class CreateFileInResponse(RWModel):
    filename: str
    token: str
    file_type: str


class FileInCreate(RWModel):
    filename: str
    filetype: Optional[str] = ""
    fileid: Optional[str]
    def createFileId(self):
        import uuid
        fileid = uuid.uuid4().hex
        self.fileid = fileid
        return fileid


class FileInUpdate(RWModel):
    filename: str


class FileCreateInResponse(RWModel):
    fileid: str
    filename: str
    filetype: Optional[str] = ""
    token: Optional[str] = ""

    def createToken(self):
        self.token = create_access_token( data={ "fileid": self.fileid , "filename": self.filename , "filetype": self.filetype }   )



class FilesInResponse(RWModel):
    files: List[FileInDb]


class FileUpload(RWModel):

    token: Optional[str]
    fileInCreate: Optional[FileInCreate]

    def decodeToken(self ) -> FileInCreate:
        decoded_token  = get_file_from_token( token=self.token   )
        self.fileInCreate = FileInCreate(  **decoded_token )
        return self.fileInCreate


class FileRename(RWModel):

    fileid: Optional[str]
    filename: str
    token: Optional[FileInCreate]


class FileUploadResponse(FileInDb):
    pass
    




