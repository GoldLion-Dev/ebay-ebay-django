from django.db import models

# Create your models here.
class Myapp(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    
    def _str_(self):
        return self.title

  

class Description(models.Model):
  title = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  class Meta:
        db_table = 'description' 

class Product(models.Model):
  item_id = models.CharField(max_length=255)
  class Meta:
        db_table = 'product'         

class Log(models.Model):
  store_name = models.CharField(max_length=255)
  listed_cn = models.CharField(max_length=225)
  class Meta:
        db_table = 'log'           