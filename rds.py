#  This script creates, modifies, and deletes an Aurora RDS Database

import boto3
import time

#  Instantiate a boto3 client for RDS
rds = boto3.client('rds')
rdsData = boto3.client('rds-data')

#  User defined variables
username = 'lemstry'
password = 'randompassword'
db_subnet_group = 'default-vpc-01d545a502cf0fe53'
db_cluster_id = 'rds-hol-cluster'
your_region = 'us-east-1'
your_account_id = '231442145948'
cluster_identifier = 'rds-hol-cluster'
#  Create DB Cluster
try:
    response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
    print(f"The DB cluster named '{db_cluster_id}' already exists. Skipping creation.")
except rds.exceptions.DBClusterNotFoundFault:
    response = rds.create_db_cluster(
        Engine='aurora-mysql',
        EngineVersion='5.7.mysql_aurora.2.08.3',
        DBClusterIdentifier=db_cluster_id,
        MasterUsername=username,
        MasterUserPassword=password,
        DatabaseName='rds_hol_db',
        DBSubnetGroupName = db_subnet_group,
        EngineMode = 'serverless',
        EnableHttpEndpoint = True,
        ScalingConfiguration = {
            'MinCapacity': 1, # Min ACU
            'MaxCapacity': 8, # Max ACU
            'AutoPause': True,
            'SecondsUntilAutoPause': 300  # Pause after 5 minutes of inactivity
        }
    )
    print(f"The DB cluster named '{db_cluster_id}' has been created.")

    #  Wait for the DB Cluster to become available
    while True:
        response = rds.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
        status = response['DBClusters'][0]['Status']
        print(f"The status of the cluster is '{status}'")
        if status == 'available':
            break
        print("Waiting for the DB Cluster to become available")
        time.sleep(40)

# Modify the DB Cluster. Update the scaling configuration for the cluster.
response = rds.modify_db_cluster(
        DBClusterIdentifier=db_cluster_id,
        ScalingConfiguration = {
            'MinCapacity': 1, # Min ACU
            'MaxCapacity': 16, # Max ACU
            'AutoPause': True,
            'SecondsUntilAutoPause': 600  # Pause after 10 minutes of inactivity
        }
    )
print(f"Updated the scaling configuration for DB cluster '{db_cluster_id}'")

#  Delete the DB cluster
response = rds.delete_db_cluster(
        DBClusterIdentifier=db_cluster_id,
        SkipFinalSnapshot=True
    )
print(f"{db_cluster_id} is being deleted.")

