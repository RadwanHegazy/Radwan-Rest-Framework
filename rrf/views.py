from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .response import Response
from django.contrib.auth.models import AnonymousUser
import json
from .models import DocModel


def api_view (methods:list=[], permissions:list=[]) :
    def decorator(func) :

        @csrf_exempt
        def wrapper (request:HttpRequest, *args, **kwargs):
            method = request.method
            
            # check for content type
            accept_content_type = ['application/json','text/plain']
            if request.content_type not in accept_content_type  :
                return Response({
                    'error' : 'content type not accepted'
                }, status_code=400)


            # check for permissions
            str_permission = ''
            for permission in permissions : 
                user = permission(request)
                if not user:
                    return Response(
                        data={
                            'message' : "Permissions Error"
                        },
                        status_code=401
                    )
                else:
                    if user :
                        request.user = AnonymousUser() if type(user) == bool else user
                str_permission = permission.__name__

            # check for method
            if method not in methods:
                return Response(
                    data={
                        'error' : f'{method} method not allowed'
                    },
                    status_code=405
                )
            
            # parse requested body to json and invoke to the request
            fields_data = ''
            if request.body :
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)                
                request.data = body
                fields_data = body
            fun = func(request, *args, **kwargs )

            docs_data = {
                "method":method,
                "permissions":str_permission,
                "url":request.path,
            }


            if fields_data:
                docs_data['fields'] = ', '.join([i for i in list(fields_data.keys())])
            
            doc, _ = DocModel.objects.get_or_create(**docs_data)

            return fun
    
        return wrapper
    return decorator


