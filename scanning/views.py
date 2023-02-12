from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymongo
import shortuuid
import qrcode

import cv2
import numpy as np
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
  return render(request,'index2.html')

def scan(request):


  cap = cv2.VideoCapture(0)

  while True:
    global currUUID
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode the QR code
    data = decode(gray)
    if len(data)>0:
      print(data[0].data.decode("utf-8"))
      currUUID=data[0].data.decode("utf-8")
    if len(data)==1:
      break
    for qr_code in data:

        (x, y, w, h) = qr_code.rect
        print(x,y,w,h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, qr_code.data.decode("utf-8"), (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("QR Code Scanner", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

  cap.release()
  cv2.destroyAllWindows()

  currData=collection.find_one({'uuid':currUUID})
  if not currData:
    return HttpResponse('QR code not matching')
  
  return HttpResponseRedirect(request,'/',currData)

