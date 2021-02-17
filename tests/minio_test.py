from datetime import timedelta
from minio import Minio

from minio.error import S3Error



def generate_upload_url( bucket ):
    client = Minio(
        "localhost:9000",
        access_key="MEDDLER",
        secret_key="SUPERDUPERSECRET",
        secure=False
    )

    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)
    url = client.get_presigned_url(
                "PUT",
                bucket,
                "my-object",
                expires=timedelta(days=1),
            )
    return url



def main():
    url  = generate_upload_url("dsadsa")
    print(url)
    return
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "localhost:9000",
        access_key="MEDDLER",
        secret_key="SUPERDUPERSECRET",
        secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("asiatrip")
    if not found:
        client.make_bucket("asiatrip")
    else:
        print("Bucket 'asiatrip' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "asiatrip", "asiaphotos-2015.zip", "./test_file.tar",
    )
    print(
        "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
        "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)