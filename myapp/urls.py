from django.urls import path
from . import views
urlpatterns = [
   
    path('getSellerProfile',views.getSellerProfile),
    path('addDescription',views.addDescription),
    path('getDescription',views.getDescription),
    path('deleteDescription',views.deleteDescription),
    path('listProduct',views.listProduct),
    path('getLog',views.getLog),
    path('getStatus',views.getStatus),
    path('getDetail',views.getDetail),
    path('update',views.update),
    path('getProducts',views.getProducts),
    path('getListStatus',views.getListStatus),
    path('titleUpdate',views.titleUpdate),

]
