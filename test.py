import unittest
from unittest.mock import patch
from moto import mock_s3
import boto3
import os
from S3_api import create_s3_bucket, upload_file, download_file, list_objects, delete_file, read_s3_object  # Replace 'your_script' with the name of your Python file

class TestS3Operations(unittest.TestCase):

    @mock_s3
    def test_create_s3_bucket(self):
        bucket_name = "test-bucket-12345"
        region = "us-east-1"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name=region)
        
        # Call the function
        create_s3_bucket(bucket_name, region)
        
        # Verify that the bucket is created
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        self.assertIn(bucket_name, bucket_names)
        print("test_create_s3_bucket passed.")

    @mock_s3
    def test_upload_file(self):
        bucket_name = "test-bucket-12345"
        file_name = "testfile.txt"
        object_name = "uploaded-testfile.txt"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=bucket_name)
        
        # Create a temporary file to upload
        with open(file_name, 'w') as f:
            f.write("Hello, world!")
        
        # Call the function
        upload_file(bucket_name, file_name, object_name)
        
        # Verify the file was uploaded
        response = s3.list_objects(Bucket=bucket_name)
        object_keys = [obj['Key'] for obj in response.get('Contents', [])]
        self.assertIn(object_name, object_keys)
        print("test_upload_file passed.")
    
    @mock_s3
    def test_download_file(self):
        bucket_name = "test-bucket-12345"
        object_name = "uploaded-testfile.txt"
        file_name = "downloaded-testfile.txt"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload a file to S3
        s3.put_object(Bucket=bucket_name, Key=object_name, Body="Hello, world!")
        
        # Call the function
        download_file(bucket_name, object_name, file_name)
        
        # Verify the file was downloaded
        self.assertTrue(os.path.exists(file_name))
        with open(file_name, 'r') as f:
            content = f.read()
            self.assertEqual(content, "Hello, world!")
        print("test_download_file passed.")
    
    @mock_s3
    def test_list_objects(self):
        bucket_name = "test-bucket-12345"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload a file
        s3.put_object(Bucket=bucket_name, Key="uploaded-testfile.txt", Body="Hello, world!")
        
        # Call the function
        objects = list_objects(bucket_name)
        self.assertIn("uploaded-testfile.txt", objects)
        print("test_list_objects passed.")
    
    @mock_s3
    def test_delete_file(self):
        bucket_name = "test-bucket-12345"
        object_name = "uploaded-testfile.txt"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload a file
        s3.put_object(Bucket=bucket_name, Key=object_name, Body="Hello, world!")
        
        # Call the function
        delete_file(bucket_name, object_name)
        
        # Verify the file was deleted
        response = s3.list_objects(Bucket=bucket_name)
        object_keys = [obj['Key'] for obj in response.get('Contents', [])]
        self.assertNotIn(object_name, object_keys)
        print("test_delete_file passed.")
    
    @mock_s3
    def test_read_s3_object(self):
        bucket_name = "test-bucket-12345"
        object_key = "example_file.txt"
        
        # Mock the AWS S3 service
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket=bucket_name)
        
        # Upload a file
        s3.put_object(Bucket=bucket_name, Key=object_key, Body="Hello, world!")
        
        # Call the function
        data = read_s3_object(bucket_name, object_key)
        self.assertEqual(data, "Hello, world!")
        print("test_read_s3_object passed.")
    
if __name__ == '__main__':
    unittest.main()