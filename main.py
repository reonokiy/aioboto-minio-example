import asyncio
import aiobotocore.session
from aiobotocore.config import AioConfig


# MinIO Configuration
MINIO_ENDPOINT_URL = "http://localhost:9000"
MINIO_ACCESS_KEY = "xxx"
MINIO_SECRET_KEY = "xxx"
BUCKET_NAME = "test"
FILE_NAME = "example.txt"
FILE_CONTENT = b"Hello from aiobotocore and MinIO!"
DOWNLOADED_FILE_NAME = "downloaded_example.txt"

# config = AioConfig(signature_version="s3v4", s3={"addressing_style": "path"}) # SUCCESS
config = AioConfig(
    signature_version="s3v4",
    s3={"addressing_style": "virtual"},
)  # !FAIL


async def manage_minio_file():
    session = aiobotocore.session.get_session()
    async with session.create_client(
        "s3",
        endpoint_url=MINIO_ENDPOINT_URL,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=config,  # Use the defined AioConfig
    ) as client:
        await client.put_object(
            Bucket=BUCKET_NAME,
            Key=FILE_NAME,
            Body=FILE_CONTENT,
        )  # type: ignore
        print(f"Uploaded {FILE_NAME} to {BUCKET_NAME}.")

        # get the file
        print(f"Downloading {FILE_NAME} from {BUCKET_NAME}...")
        response = await client.get_object(
            Bucket=BUCKET_NAME,
            Key=FILE_NAME,
        )  # type: ignore

        # Read the content from the response
        file_content_from_minio = await response["Body"].read()
        print(f"Downloaded content: {file_content_from_minio.decode()}")

        # Save the downloaded file
        with open(DOWNLOADED_FILE_NAME, "wb") as f:
            f.write(file_content_from_minio)
        print(f"Saved downloaded content to {DOWNLOADED_FILE_NAME}")


def main():
    asyncio.run(manage_minio_file())


if __name__ == "__main__":
    main()
