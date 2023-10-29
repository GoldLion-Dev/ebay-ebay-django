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
  item_id = models.CharField(max_length=255,null=True)
  listing_id = models.CharField(max_length=255,null=True)
  title = models.CharField(max_length=255,null=True)
  price = models.CharField(max_length=255,null=True)
  qty = models.CharField(max_length=255,null=True)
  category_id = models.CharField(max_length=255,null=True)
  condition_id = models.CharField(max_length=255,null=True)
  picture_urls = models.TextField(max_length=10000,null=True)
  item_specifics = models.TextField(max_length=10000,null=True)
  sku = models.CharField(max_length=255,null=True)
  description = models.TextField(max_length=30000,null=True)
  account_token = models.TextField(max_length=1000,null=True)
  class Meta:
        db_table = 'product'         

class Log(models.Model):
  store_name = models.CharField(max_length=255)
  listed_cn = models.CharField(max_length=225)
  class Meta:
        db_table = 'log'           