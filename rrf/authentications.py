from django.conf.global_settings import SECRET_KEY
import jwt
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

from django.conf import settings

User = get_user_model()

def get_token_by_user(user) :

    try : 
        EXPIRE = settings.RRF
        EXPIRE = EXPIRE.get('TOKEN_EXPIRE', timedelta(hours=24))
    except Exception :
        EXPIRE = timedelta(hours=24)
    
    print(EXPIRE)
    data = {
        'user_id' : user.id,
        'expire_at' : (datetime.now() + EXPIRE).timestamp()
    }
    encoded_token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm="HS256",
    
    )
    return encoded_token


def get_user_by_token (token) : 
    decoded_token = jwt.decode(
        token,
        SECRET_KEY,
        algorithms="HS256",
    )
    
    print(decoded_token)
    try :
        expire_at = decoded_token['expire_at']
        if expire_at < datetime.now().timestamp() : 
            user = None
        else:
            user = User.objects.get(id=decoded_token['user_id'])
    except Exception:
        user = None
    
    return user
