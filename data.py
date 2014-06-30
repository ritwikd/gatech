from pymongo import MongoClient

dataBase = MongoClient('localhost', 27017)
users = dataBase['data']['users'].find()
motion = dataBase['data']['motion']
for user in users:
	print user

def getUser(name):
    print name
