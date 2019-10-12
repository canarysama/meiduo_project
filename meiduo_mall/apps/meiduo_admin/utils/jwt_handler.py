from rest_framework_jwt.utils import jwt_payload_handler


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }

def meiduo_payload_handler(user):

    payload = jwt_payload_handler(user)

    del payload['email']

    payload['mobile'] = user.mobile

    return payload

