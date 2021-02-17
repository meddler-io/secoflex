from datetime import timedelta
import minio as minio_client
from minio.commonconfig import ENABLED
from minio.versioningconfig import VersioningConfig
from app.core.config import FILESTORAGE_PATH, MINIO_REGION, MINIO_URL, MINIO_ACCESSKEY, MINIO_SECRET


def init():
    MINIO_CLIENT = minio_client.Minio(
        MINIO_URL,
        access_key=MINIO_ACCESSKEY,
        secret_key=MINIO_SECRET,
        secure=False,
        region=MINIO_REGION
    )
    return MINIO_CLIENT


def generate_upload_url(bucket: str, object: str):
    MINIO_CLIENT = init()
    found = MINIO_CLIENT.bucket_exists(bucket)
    if not found:
        MINIO_CLIENT.make_bucket(bucket, location=MINIO_REGION)
    # MINIO_CLIENT.set_bucket_versioning( bucket,VersioningConfig(DISABLED)  )
    url = MINIO_CLIENT.get_presigned_url(
        "PUT",
        bucket,
        object ,
        expires=timedelta(days=1),
    )
    return url

def generate_download_url(bucket: str, object: str):
    MINIO_CLIENT = init()
    found = MINIO_CLIENT.bucket_exists(bucket)
    if not found:
        MINIO_CLIENT.make_bucket(bucket, location=MINIO_REGION)
    # MINIO_CLIENT.set_bucket_versioning( bucket,VersioningConfig(DISABLED)  )
    url = MINIO_CLIENT.get_presigned_url(
        "GET",
        bucket,
        object ,
        expires=timedelta(days=1),
    )
    return url
