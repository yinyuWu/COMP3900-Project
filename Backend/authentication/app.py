import boto3
import hmac
import hashlib
import base64

USER_POOL_ID = 'ap-southeast-2_VYLstuuWv'
CLIENT_ID = '5o2dcs67a6t6p6aq711ba4llf5'
CLIENT_SECRET = '19cq8t4a2cl0r65qiapoamplo9n6e1olbth3dup0vduk4h0sq2g7'
client = None


def get_secret_hash(username):
    msg = username + CLIENT_ID
    digest = hmac.new(str(CLIENT_SECRET).encode(
        'utf-8'), msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    dec = base64.b64encode(digest).decode()
    return dec


def initiate_auth(username, password):
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': get_secret_hash(username),
                'PASSWORD': password
            },
            ClientMetadata={
                'username': username,
                'password': password
            })
    except client.exceptions.NotAuthorizedException as e:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotFoundException as e:
        return None, "The username or password is incorrect"
    except Exception as e:
        print(e)
        return None, "Unknown error"
    return resp, None


def lambda_handler(event, context):
    global client
    if client == None:
        client = boto3.client('cognito-idp')
    username = event['username']
    if 'password' in event:
        resp, msg = initiate_auth(username, event['password'])

    if msg != None:
        return {
            'status': 'fail',
            'msg': msg
        }

    response = {
        'status': 'success',
        'id_token': resp['AuthenticationResult']['IdToken'],
        'access_token': resp['AuthenticationResult']['AccessToken'],
        'refresh_token': resp['AuthenticationResult']['RefreshToken']
    }

    return response
