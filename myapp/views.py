from locale import currency
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render,get_object_or_404
from ebaysdk import response
from ebaysdk.exception import ConnectionError
from ebaysdk import response
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading
from ebaysdk.policies import Connection as Policies
from ebaysdk.finding import Connection as finding  
from ebaysdk.shopping import Connection as Shopping 
from django.db import connection
from datetime import datetime
from datetime import date
from datetime import timedelta
import json
import csv
import io
from .serializers import *
import sys
import chilkat2
import requests
import base64


listingResult = 'no'
@api_view(['GET','POST'])
def addDescription(request):
    print(request.data)
    serializer = DescriptionSerializer(data=request.data)
    if serializer.is_valid():
            serializer.save()
            return Response({"status": "200", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
            return Response({"status": "500", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def getDescription(request):
        descriptions = Description.objects.all()
        serializer = DescriptionSerializer(descriptions, many=True)
        print(serializer.data)
        return Response({"status": "200", "result": serializer.data}, status=status.HTTP_200_OK) 

@api_view(['GET','POST'])
def deleteDescription(request,id=None):
       input = request.data
       description = get_object_or_404(Description, id=input['id'])
       description.delete()
       return Response({"status": "200", "data": "student Deleted"})

@api_view(['GET','POST'])
def getSellerProfile(request):
    api = Policies(domain='svcs.ebay.com', appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf",certid="PRD-7284ce84eebb-5140-4802-8969-1f50",devid="da34ba40-4ce8-472d-a43a-ab641d551ef7",token="v^1.1#i^1#f^0#r^1#p^3#I^3#t^Ul4xMF8yOjY5MEM4MUNBOTc4NDlGNDQ0RTZGMDk2MjNCMEU3NjVBXzNfMSNFXjI2MA==",config_file=None)
    res = api.execute('getSellerProfiles')
    result = res.dict()
    paymentProfiles = result['paymentProfileList']['PaymentProfile']
    returnProfiles = result['returnPolicyProfileList']['ReturnPolicyProfile']
    shippingProfiles = result['shippingPolicyProfile']['ShippingPolicyProfile']
    paymentlist = []
    returnlist = []
    shippinglist = []
    
    for payment in paymentProfiles:
        paymentRow = {}
        paymentRow['profileId'] = payment['profileId']
        paymentRow['profileName'] = payment['profileName']
        paymentlist.append(paymentRow)
    for returnPolicy in returnProfiles:
        returnRow = {}
        returnRow['profileId'] = returnPolicy['profileId']
        returnRow['profileName'] = returnPolicy['profileName']
        returnlist.append(returnRow)
    for shipping in shippingProfiles:
        shippingRow = {}
        shippingRow['profileId'] = shipping['profileId']
        shippingRow['profileName'] = shipping['profileName']
        shippinglist.append(shippingRow)
    result = {}
    result['paymentlist']   = paymentlist
    result['returnlist']   = returnlist
    result['shippinglist']   = shippinglist
    return Response(result)

def getProductDetail(itemId):
    api_request = {
                    'IncludeSelector':'ItemSpecifics,Details',
                    'ItemID':itemId
                  }
                
    api = Shopping(domain='open.api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf", iaf_token=token,config_file=None)

    try:
        res= api.execute('GetSingleItem', api_request)
        result = res.dict()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        pass
        return False    
    try:
        title = result['Item']['Title']
        qty = result['Item']['Quantity']
        price = result['Item']['ConvertedCurrentPrice']['value']
        categoryId = result['Item']['PrimaryCategoryID']
        conditionId = result['Item']['ConditionID']
        pictureURLs = result['Item']['PictureURL']
        itemSpecifics = result['Item']['ItemSpecifics']['NameValueList']
        
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        pass
        return False
    
    if price !='0':
            try:
                print("hi")
           # addProduct(title,qty,price,categoryId,conditionId,pictureURLs,itemSpecifics)
            except ConnectionError as e:
                print(e)
                print(e.response.dict())
                pass
                return False
    else:
            return False


def addProduct(title,qty,price,categoryId,conditionId,pictureURLs,itemSpecifics):
    
    try:
        api = Trading(domain='api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf",certid="PRD-7284ce84eebb-5140-4802-8969-1f50",devid="da34ba40-4ce8-472d-a43a-ab641d551ef7",token="v^1.1#i^1#f^0#r^1#p^3#I^3#t^Ul4xMF8yOjY5MEM4MUNBOTc4NDlGNDQ0RTZGMDk2MjNCMEU3NjVBXzNfMSNFXjI2MA==",config_file=None,siteid=0)
       
        request = {
                        "Item":{
                                        "Title":"{}".format(title),
                                        "BestOfferDetails":{
                                            "BestOfferEnabled":"true"
                                        },
    
                                        "Description":"{}".format(description),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Japan",
                                        "StartPrice":"{}".format(float(price)*float(profitRate)),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(qty),
                                        "ConditionID":"{}".format(conditionId),
                                        
                                        "ItemSpecifics":{
                                            "NameValueList":itemSpecifics
                                        },
                                        "PaymentMethods":"PayPal",
                                        "PayPalEmailAddress":"kevinzoo.lancer@gmail.com",
                                        "DispatchTimeMax":"1",
                                        "ShipToLocations":"None",
                                        "ReturnPolicy":{
                                            "ReturnsAcceptedOption":"ReturnsAccepted",
                                            "ReturnsWithinOption":"Days_30"
                                        },
                                        "PrimaryCategory":{
                                            "CategoryID":"{}".format(categoryId)
                                        },
                                        "PictureDetails":{
                                            "PictureURL":pictureURLs,
                                        },
                                        "ItemCompatibilityList":{
                                                "Compatibility":{
                                                    "NameValueList":[
                                                        {"Name":"Year","Value":"2010"},
                                                        {"Name":"Make","Value":"Hummer"},
                                                        {"Name":"Model","Value":"H3"}
                                                    ],
                                                    "CompatibilityNotes":"An example compatibility"
                                                }
                                        },

                                        "SellerProfiles":{

                                            "SellerPaymentProfile":{
                                                
                                                    "PaymentProfileName":"{}".format(businessPolicy['payment']['profileName']),  
                                                    "PaymentProfileID":"{}".format(businessPolicy['payment']['profileId'])
                                                    },

                                            "SellerReturnProfile":{
                                        
                                                    "ReturnProfileName":"{}".format(businessPolicy['return']['profileName']),  
                                                    "ReturnProfileID":"{}".format(businessPolicy['return']['profileId'])
                                            },

                                            "SellerShippingProfile":{
                                            
                                                    "ShippingProfileName": "{}".format(businessPolicy['shipping']['profileName']),
                                                    "ShippingProfileID":"{}".format(businessPolicy['shipping']['profileId']) 
                                            },
                                    } ,

        
        
                                        
                                        "Site":"US"

                                }
                                        
                
                    }
        response=api.execute("AddItem", request)
        print(response.dict())
        print(response.reply)
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        pass     

@api_view(['GET','POST'])
def listProduct(request):
   global token
   token =  getOAuthToken()
   print(token)
   
   inputs = request.data
   global businessPolicy
   global description
   global storeName 
   global profitRate
   businessPolicy = inputs['businessPolicy']
   description = inputs['description']
   storeName = inputs['storeName']
   profitRate = inputs['profitRate']
   
   api = finding(domain='svcs.ebay.com',config_file='ebay.yaml')
   listedCount = 0
   pageNumber = 1
   while(listedCount < 100):

        try:
                api_request = {
                            'storeName': storeName,
                            'paginationInput':{
                                'entriesPerPage':100,
                                'pageNumber':pageNumber
                            }
                        }

                response = api.execute('findItemsIneBayStores', api_request)
                res = response.dict()
        except ConnectionError as e:
                print(e)
                print(e.response.dict())
                return Response({'status':'500','message':'error'})
        searchResult = []
        if 'searchResult' in res:
                for row in res['searchResult']['item']:
                        itemId = row['itemId']
                        print(itemId)
                        listingType = row['listingInfo']['listingType']
                        if(listingType == 'FixedPrice'):
                            searchResult.append(itemId)
                            result = Product.objects.filter(item_id=itemId).first()
                            if result is None:
                                serializer = ProductSerializer(data={'item_id':itemId})
                                if serializer.is_valid():
                                        try:
                                            result = getProductDetail(itemId)
                                            if result != False:
                                                listedCount = listedCount + 1
                                                print(listedCount)
                                                serializer.save()
                                                if(listedCount > 100):
                                                    break
                                        except:
                                              pass                                                
                                else:
                                    pass
                            else:
                                 pass  
                if(pageNumber < 100):
                     pageNumber = pageNumber + 1    
                else:
                     break
                
                if(listedCount > 100):
                     break                                                    
                
        else:
                print("no exist")  
                return Response({'status':'300','message':'item is not existed in store'}) 

   serializer = LogSerializer(data = {'store_name':storeName,'listed_cn':listedCount})
   if serializer.is_valid():
        serializer.save()
   else:
        pass
   logs = Log.objects.all()
   serializer = LogSerializer(logs, many=True)
   print(serializer.data)
   global listingResult   
   listingResult = 'success'
   return Response({"status": "200", "result": serializer.data}, status=status.HTTP_200_OK) 


@api_view(['GET','POST'])
def getLog(request):
   logs = Log.objects.all()
   serializer = LogSerializer(logs, many=True)
   print(serializer.data)
   return Response({"status": "200", "result": serializer.data}, status=status.HTTP_200_OK) 


def getOAuthToken():
    # This example assumes the Chilkat API to have been previously unlocked.
    # See Global Unlock Sample for sample code.

    http = chilkat2.Http()

    # Implements the following CURL command:

    # curl -X POST 'https://api.sandbox.ebay.com/identity/v1/oauth2/token' \
    #   -H 'Content-Type: application/x-www-form-urlencoded' \
    #   -H 'Authorization: Basic UkVTVFRlc3...wZi1hOGZhLTI4MmY=' \
    #   -d 'grant_type=client_credentials&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope'

    # Use the following online tool to generate HTTP code from a CURL command
    # Convert a cURL Command to HTTP Source Code

    req = chilkat2.HttpRequest()
    req.HttpVerb = "POST"
    req.Path = "/identity/v1/oauth2/token"
    req.ContentType = "application/x-www-form-urlencoded"
    req.AddParam("grant_type","client_credentials")

    # The scope query param indicates the access to be provided by the token.
    # Multiple scopes can be specified by separating each with a SPACE char.
    # See the Ebay OAuth scopes documentation

    scope = "https://api.ebay.com/oauth/api_scope"

    req.AddParam("scope",scope)

    # Setting these properties causes the Authorization: Basic UkVTVFRlc3...wZi1hOGZhLTI4MmY=
    # header to be added.
    http.Login = "ronaldha-getItems-PRD-87284ce84-5ae3d9bf"
    http.Password = "PRD-7284ce84eebb-5140-4802-8969-1f50"
    http.BasicAuth = True

    # resp is a CkHttpResponse
    resp = http.PostUrlEncoded("https://api.ebay.com/identity/v1/oauth2/token",req)
    if (http.LastMethodSuccess == False):
        print(http.LastErrorText)
        sys.exit()

    sbResponseBody = chilkat2.StringBuilder()
    resp.GetBodySb(sbResponseBody)
    jResp = chilkat2.JsonObject()
    jResp.LoadSb(sbResponseBody)
    jResp.EmitCompact = False

    print("Response Body:")
    print(jResp.Emit())

    respStatusCode = resp.StatusCode
    print("Response Status Code = " + str(respStatusCode))
    if (respStatusCode >= 400):
        print("Response Header:")
        print(resp.Header)
        print("Failed.")


    # Sample JSON response:
    # (Sample code for parsing the JSON response is shown below)

    # {
    #   "access_token": "v^1.1#i^1#p^1#r^0#I^3#f^0#t^H4s ... wu67e3xAhskz4DAAA",
    #   "expires_in": 7200,
    #   "token_type": "Application Access Token"
    # }

    # Sample code for parsing the JSON response...
    # Use the following online tool to generate parsing code from sample JSON:
    # Generate Parsing Code from JSON

    access_token = jResp.StringOf("access_token")
    return access_token
   

@api_view(['GET','POST'])
def getStatus(request):
     global listingResult
     if(listingResult == 'success'):
          return Response({'status':'success'})
     else:
          return Response({'status':'no'})

