from django.urls import path
from . import views
urlpatterns = [
   
    path('getSellerProfile',views.getSellerProfile),
    path('addDescription',views.addDescription),
    path('getDescription',views.getDescription),
    path('deleteDescription',views.deleteDescription),
    path('listProduct',views.listProduct),
    path('getLog',views.getLog)

]
