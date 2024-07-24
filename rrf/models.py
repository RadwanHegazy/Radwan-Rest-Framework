from django.db import models


class DocModel (models.Model) : 
    method = models.CharField(max_length=100)
    url = models.CharField(max_length=225)
    fields = models.CharField(max_length=225)
    permissions = models.CharField(max_length=225)


    def __str__(self) -> str:
        return f"{self.method} : {self.url}"