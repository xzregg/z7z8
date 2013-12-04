#coding:utf-8
from django.db import models

from utils import WarpClass

#@WarpClass
class doc(models.Model):
    name = models.CharField(max_length=5,verbose_name='名字')


    def me(cls):
        return  cls.objects.all()