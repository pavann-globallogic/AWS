import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Function to create a session and connect to S3
def create_s3_session():
    try:
        # Create a session using your AWS credentials
        session = boto3.Session(
            aws_access_key_id='YOUR_ACCESS_KEY',
            aws_secret_access_key='YOUR_SECRET_KEY',
            region_name='YOUR_REGION'  # e.g., 'us-west-1'
        )
        # Connect to the S3 service
        s3 = session.resource('s3')
        return s3
    except NoCredentialsError:
        print("Credentials not found.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"Error creating session: {e}")
    return None

# Function to create S3 bucket
def create_s3_bucket(s3, bucket_name, region='us-east-1'):
    try:
        # Create the S3 bucket
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Bucket '{bucket_name}' created successfully.")
        return response
    except Exception as e:
        print(f"Error creating bucket: {e}")

# Function to upload a file to S3
def upload_file(s3, bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        s3.Bucket(bucket_name).upload_file(file_name, object_name)
        print(f"{file_name} has been uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Failed to upload {file_name} to {bucket_name}/{object_name}: {e}")

# Function to download a file from S3
def download_file(s3, bucket_name, object_name, file_name=None):
    if file_name is None:
        file_name = object_name

    try:
        s3.Bucket(bucket_name).download_file(object_name, file_name)
        print(f"{object_name} has been downloaded from {bucket_name} to {file_name}")
    except Exception as e:
        print(f"Failed to download {object_name} from {bucket_name}: {e}")

# Function to list objects in S3 bucket
def list_objects(s3, bucket_name):
    try:
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            print(obj.key)
    except Exception as e:
        print(f"Failed to list objects in {bucket_name}: {e}")

# Function to delete a file from S3
def delete_file(s3, bucket_name, object_name):
    try:
        s3.Object(bucket_name, object_name).delete()
        print(f"{object_name} has been deleted from {bucket_name}")
    except Exception as e:
        print(f"Failed to delete {object_name} from {bucket_name}: {e}")

# Function to read data from an S3 object
def read_s3_object(s3, bucket_name, object_key):
    try:
        # Get the object from the specified bucket
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # The content of the object (file) is stored in the 'Body' field
        data = response['Body'].read().decode('utf-8')

        # Print or return the content
        print(data)
        return data
    except Exception as e:
        print(f"Error reading object {object_key}: {e}")

# Function to add tags to an S3 object
def add_tags_to_object(s3, bucket_name, object_key):
    try:
        response = s3.put_object_tagging(
            Bucket=bucket_name,
            Key=object_key,
            Tagging={'TagSet': [
                {'Key': 'tag1', 'Value': 'value1'},
                {'Key': 'tag2', 'Value': 'value2'},
            ]}
        )
        print(f"Tags added to object {object_key}")
    except Exception as e:
        print(f"Error adding tags to object {object_key}: {e}")

# Main function
def main():
    s3 = create_s3_session()
    if not s3:
        return  # Exit if session creation fails

    bucket_name = "my-example-bucket"
    region = 'us-east-1'

    # Create an S3 bucket
    create_s3_bucket(s3, bucket_name, region)

    # Upload a file
    file_name = "testfile.txt"
    upload_file(s3, bucket_name, file_name)

    # Download a file
    download_file(s3, bucket_name, "uploaded-testfile.txt", "downloaded-testfile.txt")

    # List objects in the bucket
    list_objects(s3, bucket_name)

    # Read data from an object
    read_s3_object(s3, bucket_name, "uploaded-testfile.txt")

    # Delete a file from the bucket
    delete_file(s3, bucket_name, "uploaded-testfile.txt")

    # Add tags to an object
    add_tags_to_object(s3, bucket_name, "uploaded-testfile.txt")

# Run the main function
if __name__ == "__main__":
    main()
