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
import time
import pytz
import math

listResult = 'no'
extractResult = 'no'
descriptionFlagResult = ''
data = ''
productCountPerExtract = ''
systemStatus = 'process'
previousCallTime = ''
listedCount = 0
productCount = 0
productList_cn = 0
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
       return Response({"status": "200", "data": "description Deleted"})

@api_view(['GET','POST'])
def getSellerProfile(request):
    print(request.data)
    inputs = request.data
    api = Policies(domain='svcs.ebay.com', appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf",certid="PRD-7284ce84eebb-5140-4802-8969-1f50",devid="da34ba40-4ce8-472d-a43a-ab641d551ef7",token=inputs['token'], config_file=None)
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
    global data
    api_request = {
                    'IncludeSelector':'ItemSpecifics,Details,Description,ShippingCosts',
                    'ItemID':itemId
                  }
                
    api = Shopping(domain='open.api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf", iaf_token=token,config_file=None)

    try:
        res= api.execute('GetSingleItem', api_request)
        result = res.dict()
        
        
        
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        data = e.response.dict()
        pass
        return False    
    try:
        if 'Title' in result['Item'] and 'Description' in result['Item'] and 'Quantity' in result['Item'] and 'ConvertedCurrentPrice' in result['Item'] and 'PrimaryCategoryID' in result['Item'] and 'ConditionID' in result['Item'] and  'PictureURL' in result['Item'] and 'ItemSpecifics' in result['Item']:
            title = result['Item']['Title']
            qty = result['Item']['Quantity']
            price = result['Item']['ConvertedCurrentPrice']['value']
            categoryId = result['Item']['PrimaryCategoryID']
            conditionId = result['Item']['ConditionID']
            pictureURLs = result['Item']['PictureURL']
            itemSpecifics = result['Item']['ItemSpecifics']['NameValueList']
            description = result['Item']['Description']
            if 'SKU' in result['Item']:
                sku = result['Item']['SKU']
            else:
                sku = '存在しない'

                
            if 'ShippingCostSummary' in result['Item'] and 'ShippingServiceCost' in result['Item']['ShippingCostSummary'] and 'value' in result['Item']['ShippingCostSummary']['ShippingServiceCost']:       
                shippingCost = result['Item']['ShippingCostSummary']['ShippingServiceCost']['value']
            else:
                shippingCost = '存在しない'   
            print(shippingCost)     
            if type(itemSpecifics) == list:
                for itemSpecific in itemSpecifics:
                    itemSpecific['Name'] = itemSpecific['Name'].replace("&","&amp;")
                    if type(itemSpecific['Value']) == list:
                        temp_list = []
                        for value in itemSpecific['Value']:
                            value = value.replace("&","&amp;")
                            temp_list.append(value)
                        itemSpecific['Value']   = temp_list  
                    else:
                        itemSpecific['Value'] = itemSpecific['Value'].replace("&","&amp;")
            else:
                itemSpecifics['Name'] = itemSpecifics['Name'].replace("&","&amp;")
                if type(itemSpecifics['Value']) == list:
                    temp_list = []
                    for value in itemSpecifics['Value']:
                        value = value.replace("&","&amp;")
                        temp_list.append(value)
                    itemSpecifics['Value']   = temp_list  
                else:
                    itemSpecifics['Value'] = itemSpecifics['Value'].replace("&","&amp;")                
        
        else:
            return False       
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return False

    print(qty)
    if qty !='0':
            return [title,qty,price,categoryId,conditionId,pictureURLs,itemSpecifics,sku,description,shippingCost]
    else:
            return False


def addProduct(product_id,title,qty,price,profitRate,categoryId,conditionId,pictureURLs,itemSpecifics,sku,businessPolicy,templateDescription,bestofferFlag,accountToken,descriptionFlag,description):
    
    try:
        if descriptionFlag == True:
            listDescription = description
        else:
            listDescription = templateDescription

        if sku == '存在しない':
            sku = ''    
        print(businessPolicy['payment']['profileName'])
        print(businessPolicy['payment']['profileId'])
        print(businessPolicy['return']['profileName'])
        print(businessPolicy['return']['profileId'])
        print(businessPolicy['shipping']['profileName'])
        print(businessPolicy['shipping']['profileId'])
        api = Trading(domain='api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf",certid="PRD-7284ce84eebb-5140-4802-8969-1f50",devid="da34ba40-4ce8-472d-a43a-ab641d551ef7",token=accountToken,config_file=None,siteid=0)
       
        request = {
                        "Item":{
                                        "Title":"<![CDATA[{0}]]>".format(title),
                                        "BestOfferDetails":{
                                            "BestOfferEnabled":"{}".format(bestofferFlag)
                                        },
                                        "Description":"<![CDATA[{0}]]>".format(listDescription),
                                        "ListingDuration":"GTC",
                                        "ListingType":"FixedPriceItem",
                                        "Location":"Japan",
                                        "StartPrice":"{}".format(float(price)*float(profitRate)),
                                        "Country":"JP",
                                        "Currency":"USD",
                                        "Quantity":"{}".format(qty),
                                        "ConditionID":"{}".format(conditionId),
                                        "SKU":"{}".format(sku),
                                        "ItemSpecifics":{
                                            "NameValueList":itemSpecifics,
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
        if ('ItemID' in response.dict()):
            res  = response.dict()
            listed_item_id = res['ItemID']
            obj = Product.objects.get(id=product_id)
            obj.listed_item_id = listed_item_id
            obj.save()


    
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        pass     

@api_view(['GET','POST'])
def getProducts(request):
   global token
   token =  getOAuthToken()
   print(token)
   
   inputs = request.data
   global storeName    
   storeName = inputs['storeName']
   
   api = finding(domain='svcs.ebay.com',config_file='ebay.yaml')
   global listedCount
   global productCountPerExtract
   global systemStatus
   global previousCallTime
   global extractResult   
   global productCount
   extractResult = 'no'
   listedCount = 0
   pageNumber = 1
   productCount = 0
    # current date and time
   date_time = datetime.now(tz=pytz.timezone('Asia/Tokyo'))

    # format specification
   format = '%Y-%m-%d %H:%M:%S'

    
    # applying strftime() to format the datetime
   string = date_time.strftime(format)
   serializer = LogSerializer(data = {'store_name':storeName,'listed_cn':string})
   if serializer.is_valid():
        serializer.save()
   else:
        pass

   t1 = datetime.now()
   previousCallTime = t1
        
   while(listedCount <= 1000):
      
        try:
                api_request = {
                            'storeName': storeName,
                            'paginationInput':{
                                'entriesPerPage':100,
                                'pageNumber':pageNumber
                            },
                            'sortOrder':'StartTimeNewest'
                        }

                response = api.execute('findItemsIneBayStores', api_request)
                res = response.dict()
                total_entry = res['paginationOutput']['totalEntries']
                
                total_page = math.ceil(float(total_entry) / 100)
                if total_page > 100:
                    total_page = 100
                print("total page")    
                print(total_page)    
                total_entry = res['paginationOutput']['totalEntries']
                if int(total_entry) < 1000:
                    productCountPerExtract = int(total_entry)
                else:
                    productCountPerExtract = 1000  
                print(total_entry)      
                
        except ConnectionError as e:
                print(e)
                print(e.response.dict())
                return Response({'status':'500','message':e.response.dict()})
        searchResult = []
        
        if 'searchResult' in res and 'item' in res['searchResult']:
                print("page number ")
                print(pageNumber)
                print("product count every page")
                print(len(res['searchResult']['item']))
                for row in res['searchResult']['item']:
                        print("page number ")
                        print(pageNumber)
                        print("product count every page")
                        print(len(res['searchResult']['item']))
                       
                        itemId = row['itemId']
                        productCount = productCount + 1
                        print("productcount")
                        print(productCount)
                        print("itemId")
                        print(itemId)
                        listingType = row['listingInfo']['listingType']
                        print("listingType")
                        print(listingType)
                        if(listingType == 'FixedPrice'):
                            searchResult.append(itemId)
                            result = Product.objects.filter(item_id=itemId).first()
                            if result is None:
                                    print("no in database")
                                    time.sleep(2)
                                    try:
                                        result = getProductDetail(itemId)
                                       
                                        time.sleep(1)
                                        # print("product information check result")
                                        # print(result)
                                        if result != False:
                                            listedCount = listedCount + 1
                                            print(listedCount)
                                            latest_listing_id = Log.objects.latest('id').id
                                           
                                            image_urls = json.dumps(result[5])
                                            specifics = json.dumps(result[6])
                                            print("latest",latest_listing_id)
                                            
                                            converted_title = result[0] + ' #AA' + str(listedCount)
                                            if len(converted_title) >= 79:
                                                converted_title = converted_title[:76] + '...'
                                            serializer = ProductSerializer(data={'listing_id':latest_listing_id,'item_id':itemId,'title':converted_title,'qty':result[1],'price':result[2],'category_id':result[3],'condition_id':result[4],'picture_urls':json.dumps(result[5]),'item_specifics':json.dumps(result[6]),'sku':result[7],'description':'a','account_token':'AAA','shipping_cost':result[9]})
                            
                                            if serializer.is_valid():
                                                serializer.save()
                                            else:
                                                print(serializer.errors)
                                                pass
                                          
                                        else:
                                            print(result)
                                              # current date and time
                                        t2 = datetime.now()

                                            # get difference
                                        # delta = t2 - t1
                                        #     # time difference in seconds
                                        # if (delta.total_seconds() > 7200):
                                        #     break 

                                        currentCallTime = datetime.now()
                                        different = currentCallTime - previousCallTime
                                        print("different total seconds1")
                                        print(different.total_seconds())
                                        if (different.total_seconds() > 10):
                                            print("timeout1")
                                            break       
                                        if(listedCount >= 1000):
                                            break
                                       
                                    except ConnectionError as e:
                                        print(e)
                                        print(e.response.dict())
                                        
                                        pass                                             
                              
                            else:
                                 pass

                        t2 = datetime.now()

                        # get difference
                        delta = t2 - t1
                                        
                        # time difference in seconds
                        # if (delta.total_seconds() > 7200):
                        #     break 

                        currentCallTime = datetime.now()
                        different = currentCallTime - previousCallTime   
                        print("different total seconds2")
                        print(different.total_seconds())
                        if (different.total_seconds() > 10):
                            print("timeout2")
                            break          

                currentCallTime = datetime.now()
                different = currentCallTime - previousCallTime   
                print("different total seconds")
                print(different.total_seconds())
                if (different.total_seconds() > 10):
                    print("timeout3")
                    break          
                
                
                
                if(pageNumber < total_page):
                     pageNumber = pageNumber + 1    
                else:
                     break
                
                if(listedCount >= 1000):
                     break                                                    
                
        else:
                print("no exist")  
                return Response({'status':'300','message':'item is not existed in store'}) 
   
   
   logs = Log.objects.all()
   serializer = LogSerializer(logs, many=True)
   print(serializer.data)
   
   extractResult = 'success'
   systemStatus = 'process'
   return Response({"status": "200", "result": serializer.data}, status=status.HTTP_200_OK) 


@api_view(['GET','POST'])
def getLog(request):
   logs = Log.objects.all()
   serializer = LogSerializer(logs, many=True)
   print(serializer.data)
   return Response({"status": "200", "result": serializer.data}, status=status.HTTP_200_OK) 


def getOAuthToken():

 
        # Replace these values with your own client ID and client secret
    client_id = "ronaldha-getItems-PRD-87284ce84-5ae3d9bf"
    client_secret = "PRD-7284ce84eebb-5140-4802-8969-1f50"

    # Generate the base64-encoded authorization string
    auth_string = f"{client_id}:{client_secret}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()

    # Set the API endpoint URL and headers
    token_url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Authorization": f"Basic {encoded_auth_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Set the API request data
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    # Make the API request and get the access token
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        print(f"Application auth token: {access_token}")
        return access_token
    else:
        print(f"Failed to get application auth token: {response.text}")
 
   

@api_view(['GET','POST'])
def getStatus(request):
     global extractResult
     global listedCount
     global data
     global productCountPerExtract
     global previousCallTime
     global currentCallTime
     global systemStatus
     if(extractResult == 'success'):
         logs = Log.objects.all()
         serializer = LogSerializer(logs, many=True)
         print(serializer.data)

         extractResult = 'no'
         return Response({"status": "success", "result": serializer.data}, status=status.HTTP_200_OK) 
     else:
         previousCallTime = datetime.now()
         return Response({'status':'no','extracted_count':listedCount,'total_count':productCountPerExtract})

@api_view(['GET','POST'])
def getDetail(request):
    input = request.data
    products = Product.objects.filter(listing_id=input['listing_id']).values('id','item_id','title','price','picture_urls','sku','shipping_cost','listed_item_id')
    data = list(products)
    return Response({"status": "200", "result": data}, status=status.HTTP_200_OK) 

      
@api_view(['GET','POST'])
def update(request):
    input = request.data
    product_id = input['product_id']
   
    product = Product.objects.get(id=product_id)
    serializer = ProductSerializer(product,input['data'],partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "200"}, status=status.HTTP_200_OK)   

@api_view(['GET','POST'])        
def listProduct(request):
    inputs = request.data

    logId = inputs['logId']
    businessPolicy = inputs['businessPolicy']
    templateDescription = inputs['description']
    profitRate = inputs['profitRate']
    checkboxList = inputs['checkboxList']
    bestofferList = inputs['checkboxbestoffer']
    accountToken = inputs['account']
    bestofferFlag = True
    
    global productList_cn
    productList_cn = 0

    products = Product.objects.filter(listing_id=logId)
    serializer = ProductSerializer(products, many=True)
    product_list = serializer.data

    try:
        for product in product_list:
            if (str(product['id']) in checkboxList):
                continue
            else:
                if(str(product['id']) in bestofferList):
                    bestofferFlag = True
                else:
                    bestofferFlag = False  
                if templateDescription == 'default':
                    descriptionFlag = False
                else:
                    descriptionFlag = False          
                addProduct(product['id'],product['title'],product['qty'],product['price'],profitRate, product['category_id'], product['condition_id'],json.loads(product['picture_urls']),json.loads(product['item_specifics']), product['sku'],businessPolicy,templateDescription,bestofferFlag,accountToken,descriptionFlag,product['description'])    
                productList_cn = productList_cn + 1
                obj = Product.objects.get(id=product['id'])
                obj.account_token = accountToken
                obj.save()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())
        return Response({'status':'500'})
    
    global listResult
    listResult = "success"
    global descriptionFlagResult
    descriptionFlagResult = descriptionFlag
    productList_cn = 0
    return Response({'status':'200','result':descriptionFlag})


@api_view(['GET','POST'])
def getListStatus(request):
     global listResult
     

     if(listResult == 'success'):
         logs = Log.objects.all()
         serializer = LogSerializer(logs, many=True)
         print(serializer.data)
         return Response({"status": "success", "result": serializer.data}, status=status.HTTP_200_OK) 
     else:
         return Response({'status':'no','list_cn':productList_cn})




@api_view(['GET','POST'])
def titleUpdate(request):
    inputs = request.data
    products = inputs['products']
    for key in products.keys():
 
        product = Product.objects.get(id=key)
        serializer = ProductSerializer(product,{"title":products[key]},partial=True)
      
        if serializer.is_valid():
            print('valid')
            serializer.save()
        else:
            pass    
    return Response({"status": "200"}, status=status.HTTP_200_OK)   



@api_view(['GET','POST'])    
def monitorInventory(request):
    products = Product.objects.values_list('item_id','account_token','listed_item_id')
    length = 0
    i = 0
    token = getOAuthToken()            
    item_ids = []
    for product in products:
        item_ids.append(product[0])
        if product[2] == None:
            pass
        i = i + 1
        if i >= 20:
            api_request = {
                            'IncludeSelector':'Details',
                            'ItemID':item_ids
                        }
            print(api_request)
            api = Shopping(domain='open.api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf", iaf_token=token,config_file=None)

            try:
                print(api_request)
                res= api.execute('GetMultipleItems', api_request)
                result = res.dict()
              
                for item in result['Item']:
                    qty = item['Quantity']
                    item_id = item['ItemID']
                    print(qty)
                    if qty == '0':
                        product_result = Product.objects.get(item_id=item_id)
                        if product_result.account_token != 'AAA':
                            try:
                                api = Trading(domain='api.ebay.com',appid="ronaldha-getItems-PRD-87284ce84-5ae3d9bf",certid="PRD-7284ce84eebb-5140-4802-8969-1f50",devid="da34ba40-4ce8-472d-a43a-ab641d551ef7",token=product_result.account_token,config_file=None,siteid=0)
                                listed_item_id = product_result.listed_item_id
                                end_item_request = {
                                    'ItemID': listed_item_id,
                                    'EndingReason':'NotAvailable'
                                }

                                response = api.execute('EndItem', end_item_request)
                                
                              
                            except ConnectionError as e:
                                print(e)
                                print(e.res.dict())
                                pass     
                    else:
                        print("hello")  
            except ConnectionError as e:
                print(e)
                print(e.res.dict())
                pass    

            i = 0    
            item_ids = []


        else:
            pass         
    return Response({"status": "200"}, status=status.HTTP_200_OK)     
            
        
@api_view(['GET','POST'])
def deleteLog(request):
    input = request.data
    log = get_object_or_404(Log, id=input['logId'])
    log.delete()
    return Response({"status": "200", "data": "log Deleted"})


      
@api_view(['GET','POST'])
def descriptionUpdate(request):
    input = request.data
    description_id = input['description_id']
   
    description = Description.objects.get(id=description_id)
    serializer = DescriptionSerializer(description,input['data'],partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"status": "200"}, status=status.HTTP_200_OK)   