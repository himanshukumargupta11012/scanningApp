# scanningApp

first create a virtual environment for python  
follow this link- https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-20-04-quickstart  

Then clone the repository and go inside that and run- (pip install -r requirements.txt) \
This will install all packages needed for this app\
Now run (python manage.py runserver) and it's done

you can see your website at localhost:8000

for outsiders website is at localhost:8000

but who will scan the QRs, they have to got to localhost:8000/scan (Don't worry anyone can't go to this link and scan the qr. We will only allow some IPs for this purpose)