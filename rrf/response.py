"""
    Base Respoonse For return only json data
"""

from django.http import HttpResponse
import json

class Response(HttpResponse):
    """
        Attrs : 
            data[dic]: the returned data for end user
            status_code[int] : the status code number
    """    
    def __init__(self, data={}, status_code:int=200, *args, **kwargs) -> None:
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        kwargs['status'] = status_code
        super().__init__(content,*args, **kwargs)
        
