import boto3
from botocore.exceptions import ClientError

class DemoEc2:
    ec2 = None

    def __init__(self, access_key_id, secret_access_key, region):
        # Describe instances
        self.ec2 = boto3.client('ec2',
                                aws_access_key_id=access_key_id,
                                aws_secret_access_key=secret_access_key,
                                region_name=region)

    def get_vpc_id(self):
        response = self.ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        return vpc_id

    def get_instance_id(self):
        response = self.describe_instance()
        return response.get("Reservations")[0].get("Instances")[0].get("InstanceId")

    def get_groups(self):
        groups = {}
        for group in range(len(self.ec2.describe_security_groups().get("SecurityGroups"))):
            sg_name = self.ec2.describe_security_groups().get("SecurityGroups")[group].get("GroupName")
            sg_id = self.ec2.describe_security_groups().get("SecurityGroups")[group].get("GroupId")

            groups[sg_name] = sg_id
        return groups

    def describe_instance(self):
        response = self.ec2.describe_instances()
        return response

    def monitor_instance(self, state="OFF"):
        # Monitor and unmonitor instances
        instance_id = self.get_instance_id()
        if state == "ON":
            response = self.ec2.monitor_instances(InstanceIds=[instance_id])
        else:
            response = self.ec2.unmonitor_instances(InstanceIds=[instance_id])
        print("State of monitor_instance: {}".format(response["InstanceMonitorings"]
                                                     [0]["Monitoring"]["State"]))

    def start_instance(self):
        instance_id = self.get_instance_id()
        try:
            self.ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

        # Dry run successded, run start_instances without dryrun
        try:
            response = self.ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def stop_instance(self):
        instance_id = self.get_instance_id()
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

            # Dry run succeeded, call stop_instances without dryrun
        try:
            response = self.ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)

    def reboot_instance(self):
        instance_id = self.get_instance_id()
        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise

        try:
            response = self.ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
            print('Success', response)
        except ClientError as e:
            print('Error', e)


if __name__ == "__main__":
    # These information should not be in the code.
    aws_access_key_id = ""
    aws_secret_access_key = ""
    region_name = ""

    ec2_example = DemoEc2(access_key_id=aws_access_key_id,
                          secret_access_key=aws_secret_access_key,
                          region=region_name)
    print("instance_id = {}".format(ec2_example.get_instance_id()))
    ec2_example.monitor_instance("OFF")
    # ec2_example.start_instance()
    ec2_example.stop_instance()
