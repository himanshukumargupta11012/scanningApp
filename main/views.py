from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
import shortuuid
import qrcode
import random
import string
# from sms import send_sms

# Create your views here.



def generateQrCode(uuid):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(str(uuid))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # img.save("qr_code.png")



client = pymongo.MongoClient("mongodb+srv://administrator:Himanshu%40iith@scanningapp.d4ayche.mongodb.net/?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb://localhost:27017/")

dbname = client['scanData']
collection = dbname['users']

collection.create_index("phno", unique=True)


def home(request):
  if 'loginStatus' in request.COOKIES and 'phno' in request.COOKIES:
    currPhno=request.COOKIES['phno']
    currData=collection.find_one({'phno':currPhno})
    # generateQrCode(currData.uuid)
    print(currData)
    return render(request,'index.html',currData)
  return render(request,'login.html')


def otpGeneration():
  length=6
  return ''.join(random.choice(string.digits) for _ in range(length))


def signup(request):
  if request.method=='POST':
    currPhno=request.POST.get('phno')
    currName=request.POST.get('name')
    currEmail=request.POST.get('email')
    currPW=request.POST.get('password')
    currCPW=request.POST.get('cPassword')
    currUUID=shortuuid.uuid()
    currOTP=otpGeneration()
    

    if currPW!=currCPW:
      return HttpResponse('password not matching')
    elif collection.find_one({'phno':currPhno}):
      return HttpResponse('number already in use')
    currData={
      'phno':currPhno,
      'name':currName,
      'email':currEmail,
      'password':currPW,
      'uuid':currUUID,
      'otp':currOTP,
      'status':False,
      'times':0
    }
    collection.insert_one(currData)

    # send_sms(currPhno, 'Your OTP is: {}'.format(currOTP))
    # return render(request,'otp.html',currData)
    
    response=HttpResponseRedirect('/',currData)
    response.set_cookie('phno',currPhno)
    response.set_cookie('loginStatus',True)
    return response
    
  return render(request,'login.html')


# def verifyOtp(request):
#   if request.method=='POST':
#     gotPhno=request.POST.get('phno')
#     gotOtp=request.POST.get('phno')

#     currData=collection.find_one({'phno':gotPhno})

#     if currData['otp']!=gotOtp:
#       return HttpResponse('otp verification failed')
    
#     response=HttpResponseRedirect('/',currData)
#     response.set_cookie('phno',gotPhno)
#     response.set_cookie('loginStatus',True)
#     return response


def signin(request):
  if request.method=='POST':
    currPhno=request.POST.get('phno')
    currPW=request.POST.get('password')
    currData=collection.find_one({'phno':currPhno})
    print(currData)
    if not currData:
      return HttpResponse('number not exist')

    elif currPW!=currData['password']:
      return HttpResponse('password not matching')

    print(currData)
    response=HttpResponseRedirect('/',currData)
    response.set_cookie('phno',currPhno)
    response.set_cookie('loginStatus',True)
    return response
    
  return render(request,'login.html')

# logout function
def logout(request):
  response=HttpResponseRedirect('/')
  response.delete_cookie('phno')
  response.delete_cookie('loginStatus')
  return response