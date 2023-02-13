from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
import shortuuid
import qrcode
from datetime import datetime, timedelta


import cv2
from pyzbar.pyzbar import decode
# from pylibdmtx.pylibdmtx import decode




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
    print("hii1")
    return render(request,'adminPassword.html')
    
  elif request.method=='POST':
    print("hii2")
    cap = cv2.VideoCapture(0)

    while True:
      global currUUID
      ret, frame = cap.read()

      # # Convert the frame to grayscale
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      data = decode(frame)

      if len(data)==1:
        currUUID=data[0].data.decode("utf-8")
        break

      cv2.imshow("QR Code Scanner", frame)

      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        return HttpResponseRedirect('/scan')

    cap.release()
    cv2.destroyAllWindows()

    currData=collection.find_one({'uuid':currUUID})
    print(currData)
    if not currData:
      return HttpResponse('QR code not matching')
    if not currData['status']:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": True, 'lastEntryTime':datetime.utcnow() + timedelta(hours=5, minutes=30)},"$inc":{"times":1}  })

    else:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": False, 'lastExitTime':datetime.utcnow() + timedelta(hours=5, minutes=30)} })
    print(currData)
    return render(request,'index2.html',currData)
  print("hii3")
  return render(request,'index2.html')
  


# logout function
def logout(request):
  response=HttpResponseRedirect('/scan')
  response.delete_cookie('loginStatusAdmin')
  return response