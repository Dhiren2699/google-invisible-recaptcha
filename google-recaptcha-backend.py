import boto3,re
import requests
import json,os
import boto3,time


def validate_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if re.match(email_regex, email):
        return True
    return False


# DynamoDB table details
dynamodb = boto3.resource('dynamodb')
table_name = os.environ["dynamoDBName"]
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    recaptcha_response = body['recaptchaToken']
    
    is_valid = verify_recaptcha(recaptcha_response)
    
    if is_valid:
        try:
            print("INFO: Event received from UI: ",event)
            data = {}
            # name, email, message, ip, timestamp
            if(body['email'] == '' or body['email'] == None ):
                return {
                'statusCode': 404,
                'body': json.dumps({'message':"Enter a valid email!"})
            }
            else:
                if validate_email(body['email']):
                    data['email']= body['email']
                else:
                    return {
                'statusCode': 400,
                'body': json.dumps({'message':"Incorrect email! Enter a valid email!"})
            }
            if(body['name'] == '' or body['name'] == None):
                return {
                'statusCode': 404,
                'body': json.dumps({'message':"Enter a valid name!"})
            }
            else:
                data['name']= body['name']    

            if(body['message'] == '' or body['message'] == None):
                return {
                'statusCode': 404,
                'body': json.dumps({'message':"Enter a valid message!"})
            }
            else:
                data['message']= body['message'] 

            data['ip'] = event['requestContext']['http']['sourceIp']
            data['timestamp'] = int(time.time())
            data['ttl'] =  int(time.time() + (3*30*24*60*60))

            print("INFO: Data to be added in DynamoDB: ",data)
            # Put the data into the DynamoDB table
            table.put_item(
                Item=data
            )
            print("INFO: Data added Successfully!")
            return {
                'statusCode': 200,
                'body': json.dumps({'message':'Your Request has been proceed!'})
            }
        except Exception as e:
            print("ERROR",e)
            return {
                'statusCode': 400,
                'body': json.dumps({'message':e})
            }
    else:
        return {
        "success": 'false',
        "message": "Invalid reCAPTCHA. Please try again."
        }


def verify_recaptcha(response):
    # Make a POST request to the reCAPTCHA API endpoint for verification
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    secret_key = 'your-site-key'
    
    payload = {
        'secret': secret_key,
        'response': response
    }
    
    response = requests.post(verify_url, data=payload)
    verification_result = response.json()
    
    if verification_result['success']:
        return True
    else:
        return False
