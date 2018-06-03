import boto3 
from boto3.dynamodb.conditions import Key

def db_set_item(table, item):
    # create a session for boto to access the credentials that the ec2 holds
    #my_ses = boto3.Session(region_name = 'us-east-1')
    # connect to the resource dynmodb using the session
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # refer to the table
    table = dynamodb.Table(table)

    print(item)
    # insert the item
    table.put_item(Item=item)