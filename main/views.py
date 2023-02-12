from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
import shortuuid
import qrcode
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



# client = pymongo.MongoClient('mongodb+srv://username:password@HOSTNAME/DATABASE_NAME?authSource=admin&tls=true&tlsCAFile=<PATH_TO_CA_FILE>')
client = pymongo.MongoClient("mongodb://localhost:27017/")


dbname = client['scanData']
collection = dbname['users']

collection.create_index("phno", unique=True)


def home(request):
  if 'loginStatus' in request.COOKIES and 'phno' in request.COOKIES:
    currPhno=request.COOKIES['phno']
    print("yes inside the if")
    currData=collection.find_one({'phno':currPhno})
    # generateQrCode(currData.uuid)
    return render(request,'index.html',currData)
  print("outide")
  return render(request,'login.html')

def signup(request):
  print("currData")
  if request.method=='POST':
    print("currData")
    currPhno=request.POST.get('phno')
    currName=request.POST.get('name')
    currEmail=request.POST.get('email')
    currPW=request.POST.get('password')
    currCPW=request.POST.get('cPassword')
    print("currData")
    currUUID=shortuuid.uuid()
    print("currData")
    if currPW!=currCPW:
      print("currData2")
      return HttpResponse('password not matching')
    elif collection.find_one({'phno':currPhno}):
      print("currData2")
      return HttpResponse('number already in use')
    print("currData2")
    currData={
      'phno':currPhno,
      'name':currName,
      'email':currEmail,
      'password':currPW,
      'uuid':currUUID,
    }
    print(currData)
    collection.insert_one(currData)
    response=HttpResponseRedirect('/',currData)
    response.set_cookie('phno',currPhno)
    response.set_cookie('loginStatus',True)
    return response
    
  return render(request,'login.html')


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