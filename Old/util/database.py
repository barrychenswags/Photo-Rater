from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient(
            'mongodb://<dbuser>:<dbpassword>@ds123698.mlab.com:23698/dbdatabase')
        self.db = self.client['photorate']


    

