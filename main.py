import boto3
from dotenv import load_dotenv
import os


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Now boto3 will use them automatically
    client = boto3.client("s3")

    bucket_name = os.getenv("BUCKET_NAME")
    region = os.getenv("AWS_DEFAULT_REGION")

    bucket_response = client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": region},
    )
    print(bucket_response)

    response = client.list_buckets(
        MaxBuckets=123,
        BucketRegion=region,
    )
    print(response)
    print(f"Bucket {bucket_name} created.")


if __name__ == "__main__":
    main()
