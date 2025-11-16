import boto3

from app.core.settings import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION,
    # If LOCALSTACK_ENDPOINT_URL is set, use it.
    # In production, this will be None, and boto3 will use the default AWS URL.
    endpoint_url=settings.LOCALSTACK_ENDPOINT_URL,
)
