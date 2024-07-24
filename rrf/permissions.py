from django.http import HttpRequest
from .authentications import get_user_by_token

def AllowAny(request) :     
    return True

def IsAuthenticated (request:HttpRequest) : 
    auth_headers = request.headers.get('Authorization', None)

    if auth_headers is None:
        return False
    
    jwt_token = str(auth_headers).split(' ')[-1]

    try :
        user = get_user_by_token(jwt_token)
        if user:
            return user
        else:
            return False
    except Exception : 
        return False


def IsSuperUser(request) : 
    user = IsAuthenticated(request)

    if not user :
        return False
    
    if user.is_superuser:
        return user
    
    return False