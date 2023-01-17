import boto3
from datetime import date
from datetime import datetime

day = date(2023, 1, 12)
day = day.strftime("%d%m%Y")

today = datetime.today()
todays_date = today.strftime("%d%m%Y")

def lambda_handler(event, context):

    s3_client = boto3.client('s3')

    bucket_name = "raed-organise-s3-objects"
    list_objects_response = s3_client.list_objects_v2(
        Bucket=bucket_name)

    get_contents = list_objects_response.get("Contents")

    get_all_s3_objects_and_folder_names = []
    for item in get_contents:
        s3_object_name = item.get("Key")
        get_all_s3_objects_and_folder_names.append(s3_object_name)

    day_name = day + "/"
    directory_name = todays_date + "/"

    if directory_name not in get_all_s3_objects_and_folder_names:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=(directory_name))

    if day_name not in get_all_s3_objects_and_folder_names:
        s3_client.put_object(Bucket=bucket_name,
        Key=(day_name))

    for item in get_contents:
        object_creation_date = item.get("LastModified").strftime("%d%m%Y") + "/"
        object_name = item.get("Key")

        if object_creation_date == directory_name and "/" not in object_name:
            s3_client.copy_object(Bucket=bucket_name,
            CopySource=bucket_name+"/"+object_name,
            Key=directory_name+object_name)
            s3_client.delete_object(Bucket=bucket_name,
            Key=object_name)

        if object_creation_date == day_name and "/" not in object_name:
            s3_client.copy_object(Bucket=bucket_name,
            CopySource=bucket_name+"/"+object_name,
            Key=day_name+object_name)
            s3_client.delete_object(Bucket=bucket_name,
            Key=object_name)