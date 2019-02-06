from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient("mongodb://sheldon:test@ds123698.mlab.com:23698/dbdatabase")
           # 'mongodb://jaleel:test@ds263707.mlab.com:63707/help_plz')


        self.db = self.client['dbdatabase']


    

