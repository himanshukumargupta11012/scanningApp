from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
from datetime import datetime, timedelta
import json




client = pymongo.MongoClient("mongodb+srv://administrator:Himanshu%40iith@scanningapp.d4ayche.mongodb.net/?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb://localhost:27017/")


dbname = client['scanData']
collection = dbname['users']

collection.create_index("phno", unique=True)


def verifyPassword(request):
  if request.method=='POST':
    password=request.POST.get('password')
    adminPassword=collection.find_one({'role':'admin'})['password']
    if password!=adminPassword:
      return HttpResponse('Incorrect password')
    response=HttpResponseRedirect('/scan')
    response.set_cookie('loginStatusAdmin',True)
    return response
  return HttpResponse('You can\'t access this page')

def home(request):

  if 'loginStatusAdmin' not in request.COOKIES:
    return render(request,'adminPassword.html')
    
  elif request.method=='POST':


    # data = json.loads(request.body)
    currUUID = request.POST.get('gotUUID')
    currData=collection.find_one({'uuid':currUUID})
    if not currData:
      return HttpResponse('QR code not matching')
    if not currData['status']:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": True, 'lastEntryTime':datetime.utcnow() + timedelta(hours=5, minutes=30)},"$inc":{"times":1}  })

    else:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": False, 'lastExitTime':datetime.utcnow() + timedelta(hours=5, minutes=30)} })
    return render(request,'index2.html',currData)
  return render(request,'index2.html')
  


# logout function
def logout(request):
  response=HttpResponseRedirect('/scan')
  response.delete_cookie('loginStatusAdmin')
  return response