# Creating EC2 Snapshots with Lambda
This will teach you how to create an EC2 Snapshot using Lambda and Cloud9 for your existing EC2 instance

## Setup
1. The first thing you want to do is to create a lambda function by changing the runtime to your Cloud9's python version and call the function `LambdaEC2DailySnapshot`. Leave everything else default in settings.
2. Now create your EC2 instance calling it anything of your choice

## Editing your Lambda in Cloud9
In this step you will be editing your Lambda functions using Cloud <br>
1. Go into your Cloud9 environment
2. Click on the `aws-explorer` button on the left and navigate to your lambda function in the region it's located in
3. Right click and click download
4. Once downloaded, Go into the newly downloaded lambda function and insert this code: <br>
```
import json
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Automating EC2 Backups with Lambda
# Create a lambda function which creates a snapshot on my EC2 instance in regualr intervals
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    current_date = datetime.now().strftime("%Y-%m-%d")
    try:
        response = ec2.create_snapshot(
            VolumeId='vol-09f3bd093842c8678',
            Description='My EC2 Snapshot',
            TagSpecifications=[
                {
                   'ResourceType': 'snapshot',
                   'Tags': [
                       {
                           'Key': 'Name',
                           'Value': f"My EC2 snapshot {current_date}"
                            }
                       ]
                    }
                ]
            )
        logger.info(f"Successfully created snapshot: {json.dumps(response, default=str)}")
    except Exception as e:
        logger.error(f"Error creating snapshot {str(e)}")
```
5. Replace `VolumeId='vol-09f3bd093842c8678'` with your VolumeId of your EC2 instance in this code
6. Now in the terminal navigate to your Lamda function folder and create 2 files called `event.json` and `template.yml`
7. Once created, edit your event.json with this code:
```
{}
```
8. Now edit your template.yml with this code:
```
Resources:
  LambdaEC2DailySnapshot:
    Type: AWS::Serverless::Function
    Properties:
      Handler: lambda_function.lambda_handler
      Runtime: python3.8
      CodeUri: .
```
9. Save all files using `CTRL+S`

## Run your Lambda Function and See it Work!
In this step, you will run your Lambda function to create the EC2 snapshot and you will verify it is created.
1. In your terminal make sure you are in your lambda functions folder. Use `pwd`  command to verify
2. Run this command in your terminal: `sam local invoke -e event.json` <br>
![Alt text](https://images-python-lt.s3.amazonaws.com/runLambda.png)
3. You're done! Now verify that the snapshot has been created. Here is how it should look like: <br>
![Alt text](https://images-python-lt.s3.amazonaws.com/ec2snapshot.png)
