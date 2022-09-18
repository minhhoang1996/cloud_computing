import boto3
from configs import configs
from source.boto3.manage_EC2_instance.lesson1 import DemoEc2
from botocore.exceptions import ClientError


class ElasticIP(DemoEc2):
    def __init__(self, access_key_id, secret_access_key, region):
        DemoEc2.__init__(self, access_key_id, secret_access_key, region)

    def describe_address(self):
        filters = [
            {'Name': 'domain', 'Values': ['vpc']}
        ]
        response = self.ec2.describe_addresses(Filters=filters)
        return response

    def get_allocation_id(self):
        response = self.describe_address()
        return response.get("Addresses")[0].get("AllocationId")

    def allocate_address(self):
        try:
            allocation = self.ec2.allocate_address(Domain='vpc')
            return allocation
        except ClientError as e:
            print(e)

    def associate_address(self, allocation_id, instance_id):
        try:
            response = self.ec2.associate_address(AllocationId=allocation_id,
                                                  InstanceId=instance_id)
            # print(response)
        except ClientError as e:
            print(e)

    def release_address(self, allocation_id):
        try:
            self.ec2.release_address(AllocationId=allocation_id)
            print('Address released')
        except ClientError as e:
            print(e)


if __name__ == "__main__":
    aws_access_key_id = configs.access_key_ID
    aws_secret_access_key = configs.secret_access_key
    region_name = configs.region_name

    eip = ElasticIP(aws_access_key_id,
                    aws_secret_access_key,
                    region_name)
    # print(eip.describe_address())
    # print(eip.get_allocation_id())
    # eip.associate_address(allocation_id=eip.get_allocation_id(),
    #                       instance_id=eip.get_instance_id())
    eip.release_address(allocation_id=eip.get_allocation_id())

