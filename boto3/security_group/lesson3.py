import boto3
from configs import configs
from source.boto3.manage_EC2_instance.lesson1 import DemoEc2
from botocore.exceptions import ClientError


class SecurityGroup(DemoEc2):
    def __init__(self, access_key_id, secret_access_key, region):
        DemoEc2.__init__(self, access_key_id, secret_access_key, region)

    def describe_group(self, group_id):
        try:
            response = self.ec2.describe_security_groups(GroupIds=[group_id])
            print(response)
        except ClientError as e:
            print(e)

    def create_group(self, group_name, description):
        vpc_id = self.get_vpc_id()
        try:
            response = self.ec2.create_security_group(GroupName=group_name,
                                                      Description=description,
                                                      VpcId=vpc_id)
            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

            data = self.ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            print('Ingress Successfully Set %s' % data)
        except ClientError as e:
            print(e)

    def delete_group(self, group_id):
        try:
            response = self.ec2.delete_security_group(GroupId=group_id)
            print('Security Group Deleted')
        except ClientError as e:
            print(e)


if __name__ == "__main__":
    aws_access_key_id = configs.access_key_ID
    aws_secret_access_key = configs.secret_access_key
    region_name = configs.region_name
    sg_name = "example_sg"

    sg = SecurityGroup(aws_access_key_id,
                       aws_secret_access_key,
                       region_name)
    print(sg.get_groups())
    sg.create_group(group_name=sg_name, description="example_3/3/2022")
    sg.describe_group(group_id=sg.get_groups()[sg_name])
    sg.delete_group(group_id=sg.get_groups()[sg_name])
