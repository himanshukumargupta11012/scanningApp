import pymongo
import csv

client = pymongo.MongoClient("mongodb+srv://administrator:Himanshu%40iith@scanningapp.d4ayche.mongodb.net/?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb://localhost:27017/")


dbname = client['scanData']
collection = dbname['users']


# inside=list(collection.find({'status':True}))

# lis=[]
# for i in range(len(inside)):
#     lis.append([inside[i]['phno'],inside[i]['email'],inside[i]['name']])
    
    
# print(len(list(inside)))


# with open('data.csv', 'w') as f:
      
#     csv_writer = csv.writer(f)
#     csv_writer.writerows(lis)



today=list(collection.find())
todayList=[]
for i in today:
    if 'lastEntryTime' in i:
      if i['lastEntryTime'].day==17:
          todayList.append([i['phno'],i['email'],i['name'],i['times']])
print(len(todayList))


with open('17_feb.csv', 'w') as f:
      
    csv_writer = csv.writer(f)
    csv_writer.writerows(todayList)