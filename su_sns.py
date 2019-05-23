import boto3
import json
import os
sqs = boto3.client('sqs')
s3 = boto3.resource('s3')



response = sqs.receive_message(
    QueueUrl='https://sqs.ap-south-1.amazonaws.com/054390801093/myq',
    AttributeNames=[
        'All',
    ],
    MessageAttributeNames=[
        'All',
    ],
    )
for x in response['Messages']:
    y=x['Body']
    j= json.loads(y)
    pj=j['Message']
    print(pj)
file=open("hello.txt",'a')
file.write(pj)
s3.Bucket('kalaipy').upload_file('D:\\working\\hello.txt', 'hello.txt')

    

    
    