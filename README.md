# Radwan-Rest-Framework (RRF)

<p>RRF is a RESTFUL APIs framework like Django Rest Framework (DRF), this packge not like DRF , this packge is samller than DRF and not have the same futures of DRF, but i build this lib for <b>learning and educational purposes</b>. </p>


# Documentation and how it works
<p> 
first of all this package is very look like drf in somethings, or all things 😂
<p> 

<p> we talk in these topics: <p>

- add rrf in core project
- serializers
- create your first rrf endpoint
- User Permissions with rrf
- APIs documentation with rrf


## Add rrf in core Project
First all u will do is to install this package and add it in **INSTALLED_APPS**

```python
INSTALLED_APPS = [
    ...
    "rrf"
    ...
]
````


## Serializers
the same thing u was do on drf you will do the same thing on rrf serializers
but without some changes.

```python
# you_app/serializers.py
from rrf import serializers


# non-model serializer implemntation
class TestSerializers (serializers.Serializer):
    # Add your fields
    first_name:str
    last_name:str
    email:str
    password:str
    

    # implement your custom validation here [OPTIONAL]
    def validate(self, attrs):
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        email = attrs['email']
        password = attrs['password']



# model serializer 
class RegisterSerialier (serializers.ModelSerializer) : 
    class Meta:
        model = YourModel
        fields = ['filed1','field2','field3']

    # write custom validation here [OPTIONAL]
    def validate(self, attrs) :
        field1 = attrs['field1']
        field2 = attrs['field2']
        field3 = attrs['field3']

    # write custom save here [OPTIONAL]
    def save(self):
        pass

```


## Create your first rrf endpoint
```python
# your_app/views.py
from rrf.views import api_view
from rrf.response import Response

# build and endpoint with method 'GET'
@api_view(['GET'])  # method type
def rrf_first_endpoint (request) : 
    data = {
        "message" : "it works !"
    }
    return Response(data, status_code=200)
    
```



## Permissions with rrf
<p>Now let's use rrf permissions for our endpoint to make it more secure <p>

```python

from rrf.permissions import IsAuthenticated
from rrf.response import Response
from rrf.views import api_view

@api_view(['GET'], permissions=[IsAuthenticated])
def profile_view (request) : 
    user = request.user
    data = {
        'id' : user.id,
        'username' : user.username,
        'email' : user.email,
    }
    return Response(data, status_code=200)

```

We Have a 3 types of permissions in rrf :

- IsAuthenticated [For only authenticated users]
- IsSuperUser [For only Superuser]
- AllowAny [any one of users]

You can build custom user permissions like

```python
# your_app/permissions.py


# it's neccessry to take your method to take one parameter which is the request
def CustomUserPermission (request) : 
    
    # on success of your logic return user else return False
    
    if your_logic :
        return request.user
    else:
        return False 

```


## Authentication with rrf
for authentication and tokenization i use JWT for this process, the default time for token expiration is 24 hours and u can edit it in your settings.py file like : 
```python

# Let's Modifiy the expiration date to 2 days
from datetime import timedelta
RRF = {
    'TOKEN_EXPIRE' : timedelta(days=2),
}

```

### How we can do a JWT token for specific User ?

```python

from rrf.authentications import get_token_by_user

User = Your_User_Model()

user = User.objects.get(id=1)
created_token = get_token_by_user(user) # this is the token that return for client

```

## APIs documentation with rrf
creating docs is important and for any back-end developer, and createing APIs docs in rrf is very easy and simlpe, only with two steps you implement documentation for your API.

First : Migrate the docModel
```terminal
py manage.py migrate rrf
```

Secend : Add doc endpoint 
```python
# your_project/urls.py

from django.urls import include, path

urlpatterns = [
    ...
    path("my_docs/", include("rrf.docs"))
    ...
]
```

Then go to the url you define and you will see your endpoints docs

NOTE: If you didn't see your endpoints you can test it and re-open the docs page


# And this is all About the RRF and i hope you enjoy reading ❤