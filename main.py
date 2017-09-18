import boto3
import os
import json

# Before run script export env vars
# export AWS_KEY=THE_KEY
# export AWS_S_KEY=THE_S_KEY

# run script:
# python main.py

KEY = os.environ.get('AWS_KEY')
S_KEY = os.environ.get('AWS_S_KEY')

def connect(k, sk):
    client = boto3.client('iam', aws_access_key_id=k, aws_secret_access_key=sk)
    return client

def get_users():
    iam = connect(KEY, S_KEY)
    users = iam.list_users()['Users']
    return users

def get_access_key(username):
    iam = connect(KEY, S_KEY)
    pag = iam.get_paginator('list_access_keys')
    for res in pag.paginate(UserName=username):
        if len(res['AccessKeyMetadata']) != 0:
            return [keys['AccessKeyId'] for keys in res['AccessKeyMetadata']]

def get_json():
    u_json = {}
    users = get_users()
    for user in users:
        if get_access_key(user['UserName']) is not None:
            u_json[user['UserName']] = get_access_key(user['UserName'])
    return json.dumps(u_json)

if __name__ == '__main__':
    print(get_json())

