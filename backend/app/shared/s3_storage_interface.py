import mimetypes
from typing import BinaryIO

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile

from app.core.aws_clients import s3_client
from app.core.settings import settings


class S3StorageInterface:
    # =======================================================
    # ================= EDU ARTICLE IMAGES ==================
    # =======================================================
    ARTICLE_PREFIX = "edu-articles"

    @staticmethod
    def put_article_img(article_id: int, article_img: UploadFile) -> str | None:
        return S3StorageInterface._upload_file_stream(
            prefix=S3StorageInterface.QUALIFICATION_PREFIX,
            file_name=str(article_id),
            file_obj=article_img.file,
            content_type=article_img.content_type,
        )

    # =====================================================
    # ================ QUALIFICATIONS =====================
    # =====================================================
    QUALIFICATION_PREFIX = "qualifications"

    @staticmethod
    def put_qualification_img(user_id: int, qualification_img: UploadFile) -> str | None:
        return S3StorageInterface._upload_file_stream(
            prefix=S3StorageInterface.QUALIFICATION_PREFIX,
            file_name=str(user_id),
            file_obj=qualification_img.file,
            content_type=qualification_img.content_type,
        )

    @staticmethod
    def put_qualification_img_from_filepath(user_id: int, qualification_img_filepath: str) -> str | None:
        return S3StorageInterface._put_img_from_filepath(
            file_name=str(user_id),
            img_filepath=qualification_img_filepath,
            prefix=S3StorageInterface.QUALIFICATION_PREFIX,
        )

    # =====================================================
    # =================== PROFILES ========================
    # =====================================================
    PROFILE_PREFIX = "profile-images"

    @staticmethod
    def put_profile_img(user_id: int, profile_img: UploadFile) -> str | None:
        return S3StorageInterface._upload_file_stream(
            prefix=S3StorageInterface.PROFILE_PREFIX,
            file_name=str(user_id),
            file_obj=profile_img.file,
            content_type=profile_img.content_type,
        )

    @staticmethod
    def put_profile_img_from_filepath(user_id: int, profile_img_filepath: str) -> str | None:
        return S3StorageInterface._put_img_from_filepath(
            file_name=str(user_id),
            img_filepath=profile_img_filepath,
            prefix=S3StorageInterface.PROFILE_PREFIX,
        )

    # =====================================================
    # ==================== COMMON ========================
    # ====================================================
    @staticmethod
    def get_presigned_url(obj_key: str) -> str | None:
        """
        Generates a temporary, presigned URL for a private S3 object.

        Args:
            obj_key: The full object key (e.g., "profile-images/user-id.jpg").

        Returns:
            A string containing the presigned URL, or None if the
            obj_key was empty or an error occurred.
        """
        try:
            url: str = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": settings.S3_BUCKET_NAME, "Key": obj_key},
                ExpiresIn=900,  # URL is valid for 15 minutes (900 seconds)
            )
            return url
        except (BotoCoreError, ClientError) as e:
            print(f"Error generating presigned URL for {obj_key}: {e}")
            return None

    @staticmethod
    def _put_img_from_filepath(file_name: str, img_filepath: str, prefix: str) -> str | None:
        content_type, _ = mimetypes.guess_type(img_filepath)  # Guess the type from file path
        if not content_type:
            content_type = "application/octet-stream"  # Default generic type

        try:
            with open(img_filepath, "rb") as f:
                return S3StorageInterface._upload_file_stream(
                    prefix=prefix,
                    file_name=file_name,
                    file_obj=f,
                    content_type=content_type,
                )
        except FileNotFoundError:
            print(f"Error: File not found at path: {img_filepath}")
            return None
        except IOError as e:
            print(f"Error opening or reading file: {e}")
            return None

    @staticmethod
    def _upload_file_stream(prefix: str, file_name: str, file_obj: BinaryIO, content_type: str) -> str | None:
        try:
            extension = mimetypes.guess_extension(content_type)
            if not extension:
                if "jpeg" in content_type:
                    extension = ".jpg"
                elif "png" in content_type:
                    extension = ".png"
                else:
                    extension = ".jpg"

            obj_key = f"{prefix}/{file_name}{extension}"
            # print("S3StorageInterface, Obj Key: ", obj_key)
            s3_client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=settings.S3_BUCKET_NAME,
                Key=obj_key,
                ExtraArgs={"ContentType": content_type},
            )
            return obj_key
        except (BotoCoreError, ClientError) as e:
            print(f"Error uploading file stream: {e}")
            return None
