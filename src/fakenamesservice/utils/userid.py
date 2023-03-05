import jwt
from fastapi import Request


def get_openid_user(request: Request):
    user_id = 'n/a'
    try:
        encoded_jwt = request.headers.get('X-Amzn-Oidc-Accesstoken')
        user_id = jwt.decode(encoded_jwt,
                             algorithms=["RS256"],
                             options={"verify_signature": False}).get("sub")
    finally:
        return user_id
