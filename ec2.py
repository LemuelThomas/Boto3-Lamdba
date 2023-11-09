#  This script manages Amazon EC2 instances using boto3 Python SDK
import boto3

#  Create ec2 resource and instance name
ec2 = boto3.resource('ec2')
instance_name = 'dct-ec2-hol'

#  Store instance id
instance_id = None

#  Check if instance already exists
#  And only work with an instance that hasn't been terminated
instances = ec2.instances.all()
instance_exists = False

for instance in instances: #  Looping through all the instances
    for tag in instance.tags: #  Looping through all the tags in the instances
        if tag['Key'] == 'Name' and tag['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f"An instance named '{instance_name}' with id '{instance_id}' already exists")
            break
    if instance_exists:
        break

#  Launch a new EC2 instance if it hasn't already been created
if not instance_exists:

    new_instance = ec2.create_instances(
        ImageId='ami-05c13eab67c5d8861',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='EC2PPK',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )
    instance_id = new_instance[0].id
    print(f"An instance named '{instance_name}' with id '{instance_id}' already exists")

#  Stop an instance
ec2.instance(instance_id).stop()
print(f"Instance '{instance_name}-{instance_id}' stopped.")

#  Start an instance
ec2.instance(instance_id).start()
print(f"Instance '{instance_name}-{instance_id}' started.")

#  Terminate an instance
ec2.instance(instance_id).terminate()
print(f"Instance '{instance_name}-{instance_id}' terminated.")