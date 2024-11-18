import cmd
import os
import boto3
from dotenv import load_dotenv
import re
from botocore.exceptions import ClientError

class AWSClient:
    def __init__(self):
        load_dotenv()

        AWS_ACCESS_KEY_ID = 'AKIAVKNBWT6MT5PO2ULP'
        AWS_SECRET_ACCESS_KEY = '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'
        AWS_REGION = 'eu-west-1'

        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            raise EnvironmentError('AWS credentials required!')

        # Initialize the S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )

    def list_files(self, bucket_name, prefix):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                return []
        except ClientError as ce:
            error_code = ce.response['Error']['Code']
            error_message = ce.response['Error']['Message']
            print(f"ClientError: {error_code} - {error_message}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")




class PythonCLI(cmd.Cmd):

    prompt = '>>'
    intro = 'LCloud task Python CLI. Waiting for commands.'

    def __init__(self, aws_client):
        super().__init__()
        self.aws_client = aws_client

    def do_list_files(self, line):

        bucket_name = 'developer-task'
        prefix = 'y-wing/'
        try:
            files = self.aws_client.list_files(bucket_name, prefix)
            if files:
                print("List of files in the 'y-wing' directory:")
                for file in files:
                    print(f" - {file}")
            else:
                print("No files found in the 'y-wing' directory.")
        except Exception as e:
            print(f"Error: {e}")

    def do_upload_file(self, line):
        args = line.split()
        print(args)
        if len(args) != 3:
            print("Error: Usage is upload_file <file-path> <bucket-name> <object-name>")

        _, file_path, object_name = args
        try:
            self.aws_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def do_filter_bucket(self, line):
        args = line.split()
        print(args)
        _, regex_filter = args


    def do_quit(self, line):
        """Exit the CLI."""
        return True




if __name__ == '__main__':
    aws_client = AWSClient()
    PythonCLI(aws_client).cmdloop()