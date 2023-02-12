from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
import shortuuid
import qrcode

import cv2
from pyzbar.pyzbar import decode
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
  if request.method=='POST':

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
          break

    cap.release()
    cv2.destroyAllWindows()

    currData=collection.find_one({'uuid':currUUID})

    if not currData:
      return HttpResponse('QR code not matching')
    if currData['status']==0:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": True,},"$inc":{"times":1}  })
    else:
      collection.update_one({'uuid':currUUID},{ "$set": { "status": False,  } })
    return render(request,'index2.html',currData)
  return render(request,'index2.html')

