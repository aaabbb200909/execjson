from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user_id_jsons(models.Model):
    user = models.CharField(max_length=30, primary_key=True) # user1, user2, ...
    saveid = models.CharField(max_length=30, primary_key=True) # 1,2,...
    json = models.TextField() # json
