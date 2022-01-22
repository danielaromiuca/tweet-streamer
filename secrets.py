import boto3
from ec2_metadata import ec2_metadata

session = boto3.Session(region_name=ec2_metadata.region)
ssm = session.client("ssm")
parameters = ssm.get_parameters(
    Names=[
        "api_access_token",
        "api_access_token_secret",
        "api_consumer_secret",
        "api_consumer_key",
    ],
    WithDecryption=True,
)

API_ACCESS_TOKEN, API_ACCESS_TOKEN_SECRET, API_CONSUMER_SECRET, API_CONSUMER_KEY = [
    param["Value"] for param in parameters["Parameters"]
]
