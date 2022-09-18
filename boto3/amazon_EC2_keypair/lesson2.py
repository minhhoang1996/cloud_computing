import boto3
from configs import configs
from source.boto3.manage_EC2_instance.lesson1 import DemoEc2


class ExampleKeypair(DemoEc2):
    def __init__(self, access_key_id, secret_access_key, region):
        DemoEc2.__init__(self, access_key_id, secret_access_key, region)

    def get_keypair_info(self):
        print(self.ec2.describe_key_pairs())

    def create_keypair(self, key_name="keypair_default"):
        response = self.ec2.create_key_pair(KeyName=key_name)
        print(response)

    def delete_keypair(self, key_name="keypair_default"):
        response = self.ec2.delete_key_pair(KeyName=key_name)
        print(response)


if __name__ == "__main__":
    aws_access_key_id = configs.access_key_ID
    aws_secret_access_key = configs.secret_access_key
    region_name = configs.region_name
    keypair = ExampleKeypair(aws_access_key_id,
                             aws_secret_access_key,
                             region_name)

    keypair.get_keypair_info()
    keypair.create_keypair(key_name="demo_keypair")
    keypair.delete_keypair(key_name="demo_keypair")
    keypair.get_keypair_info()
