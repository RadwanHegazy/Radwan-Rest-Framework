from dataclasses import dataclass
from typing import Any
from django.db.models import QuerySet
from rrf.response import Response
from rrf.exeptions import ValidationError
import json

# @dataclass
class BaseSerializer :
    errors=[]
    validated_data={}
    # many:bool=False
    # query:QuerySet=None


    def __init__(self, data=None,context=None) -> None:
        self.data = data
        self.context = context or {}


    def validate (self, attrs) -> dict:...

    def is_valid (self) -> bool:...
        
    
    def validate_method(self) -> bool: 
        try : 
            self.validate(
                attrs=self.validated_data
            )
        except ValidationError as error : 
            print('error : ', error)
            self.errors.clear()
            self.errors += [{
                'error' : error.message
            }]
            return False
        
        return True
    

class Serializer (BaseSerializer) :
    
    def annotation_validation(self) -> bool: 
        if len(self.__annotations__.keys()) == 0 :
            return True
        
        accepted_data = self.data.keys()
        state = True
        self.errors.clear()
        for i in self.__annotations__.keys() : 
            if i not in accepted_data :
                self.errors += [
                    {
                        i:'field not found'
                    }
                ]
                state = False
        
        if not state:
            return state
        
        for key, _type in self.__annotations__.items() :
            self.validated_data[key] = _type(self.data[key])
        self.data = self.validated_data
    
        return state

    def is_valid(self) -> bool:
        return self.annotation_validation() and self.validate_method()

class ModelSerializer (BaseSerializer) :

    class Meta:
        model = None
        fields = None
    
    def __init__(self, query=None, many=None, data=None, context=None) -> None:
        self.query = query or []
        self.many = many or False
        self.context = context or {}
        if data or type(data) == dict:
            self.data = data
        else:
            self.data = self._data
            
        if self.Meta.model is None or self.Meta.fields is None:
            raise NotImplementedError('Meta class not modified')
        

    def is_valid(self) -> bool:

        validate_fields = []

        for i in self.Meta.fields : 
            if i != 'id':
                validate_fields.append(i)

        state = True
        self.errors.clear()

        self.validated_data = {}
        for i in validate_fields :
            if i not in self.data.keys() :
                self.errors += [{
                    i : 'field not found'
                }]
                state = False
            else:
                self.validated_data[i] = self.data[i]
    
        if not state : 
            return state    

        if self.validate_method():
            return True
        
        return False



    def save(self) :
        model = self.Meta.model
        created_model = model.objects.create(**self.validated_data)
        self.data = {}
        for i in self.Meta.fields:
            self.data[i] = getattr(created_model, i)
        return created_model

    @property
    def _data (self) :
        if self.many == False :
            data = {}
            for f in self.Meta.fields:
                data[f] = getattr(self.query, f)
            return data
        
        if self.many == False and len(self.query) > 1:
            raise ValidationError("Too many data")
        
        else:
            data = []
            for q in self.query :
                query_fields = {}
                for f in self.Meta.fields : 
                    query_fields[f] = getattr(q, f)
                data.append(query_fields)
            return data

