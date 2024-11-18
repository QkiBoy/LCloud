import cmd
import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

class PythonCLI(cmd.Cmd):

    def __init__(self):
        super().__init__()

        load_dotenv()

        AWS_ACCESS_KEY_ID = 'AKIAVKNBWT6MT5PO2ULP'
        AWS_SECRET_ACCESS_KEY = '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'
        AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')

        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
            raise EnvironmentError('AWS credentials required!')

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )


    prompt = '>>'
    intro = 'LCloud task Python CLI. Waiting for commands.'

    def do_list_files(self, line):

        bucket_name = 'developer-task'
        prefix = 'y-wing'
        if not bucket_name:
            print("Error: Bucket name is required!")
            return

        try:
            print(f"Bucket {bucket_name} fetching data:")
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix = prefix)
            if 'Contents' in response:
                print("List of files in the bucket:")
                for obj in response['Contents']:
                    print(f"{obj['Key']}")
            else:
                print("The bucket is empty or doesn't exist")
        except ClientError:
            print("Client Error")
        except Exception:
            print("Unexpected Error")

    def do_upload_file(self, line):

        pass



    def do_quit(self, line):
        """Exit the CLI."""
        return True




if __name__ == '__main__':
    PythonCLI().cmdloop()