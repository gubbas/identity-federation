import boto3
import botocore


#############################
# USER DEFINED FUNCTIONS HERE
############################

# just pass the instantiated bucket object
def list_bucket_contents(bucket):
    try:
        for object in bucket.objects.all():
            print('OBJECT KEY', object.key)
            # print(object)
            body = object.get()['Body'].read()

            if object.key=='user_fun/user_doc.txt':
                print('OBJECT BODY: ', body)
                # read_s3_object_contents(object)



    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise



# just pass the instantiated bucket object
def read_s3_object_contents(s3_obj):

    try:
        print('PRINING OBJECT CONTENTS')
        #print('Reading file  ',s3_obj.key)
        body = s3_obj['Body']
        file_content = body.read().decode('utf-8')
        print(file_content)

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

######################
# MAIN LOGIC STARTS HERE
######################

client = boto3.client('sts')

#=============
# Replace XXXX  with AWS account ID
#=============

#Amazon Role ARN
arn = 'arn:aws:iam::XXXXXXXXX:role/WebIdFed_Amazon'
# Google Role ARN
#arn = 'arn:aws:iam::XXXXX:role/WebIdFed_Google'

session_name = 'web-identity-federation'
#Amazon Token
token = 'Atza|IwEBIIGVbWRxxxxxxxxxxxxxxxx'
#Google Token
#token='xxxxxxxxxxxxxx'

creds = client.assume_role_with_web_identity(
    RoleArn=arn,
    RoleSessionName=session_name,
    WebIdentityToken=token,
    ProviderId='www.amazon.com',
)

print (creds)
print('Below are values from AMAZON')
print('ROLE ARN : ', creds['AssumedRoleUser']['Arn'])
print('ROLE ARN : ', creds['AssumedRoleUser']['Arn'])
print('AccessKeyId : ', creds['Credentials']['AccessKeyId'])
print('SecretAccessKey: ', creds['Credentials']['SecretAccessKey'])
print('SessionToken  : ', creds['Credentials']['SessionToken'])



# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=creds['Credentials']['AccessKeyId'],
#     aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
#     aws_session_token=creds['Credentials']['SessionToken'],
# )
# print(s3_client)

session = boto3.Session(
    aws_access_key_id=creds['Credentials']['AccessKeyId'],
    aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
    aws_session_token=creds['Credentials']['SessionToken'],
)



s3_client_from_session = session.client('s3')
s3 = session.resource('s3')


# READ Contents of a bucket
the_bucket = s3.Bucket("web-identity-federation-playground")
list_bucket_contents(the_bucket)


