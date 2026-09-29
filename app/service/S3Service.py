from fastapi import UploadFile
from uuid import uuid4
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import logging
from app.repository.message_repository import MessageRepository


class FileDeliveryError(Exception):
    pass


class S3BucketService:
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
        message: MessageRepository,
    ) -> None:
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint
        self.message = message

        self.s3 = boto3.client(
            service_name="s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            verify=False,
            config=Config(signature_version="s3v4"),
        )

    async def upload_file_object(
        self, file: UploadFile, user_id: str, receiver_id: str
    ):

        key = f"messages/{uuid4()}"

        try:
            self.s3.upload_fileobj(
                file.file,
                self.bucket_name,
                key,
                ExtraArgs={
                    "ContentType": file.content_type or "application/octet-stream",
                },
            )

            result = await self.message.add_attachment(
                user_id,
                receiver_id,
                key,
                # content_type=file.content_type,
            )

            return result

        except ClientError as e:
            logging.exception("S3 upload error: %s", e)
            raise FileDeliveryError("Ошибка загрузки файла")

    def generate_file_url(self, key: str):
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                },
                ExpiresIn=3600,
            )
            return url

        except ClientError as e:
            logging.exception("S3 upload error: %s", e)
            raise FileDeliveryError("Ошибка загрузки файла")

