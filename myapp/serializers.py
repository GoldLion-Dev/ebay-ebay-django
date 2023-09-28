from rest_framework import serializers
from .models import *
class MyappSerializer(serializers.ModelSerializer):
   class Meta:
       model = Myapp
       fields = ('id','title','description')

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'            

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'             