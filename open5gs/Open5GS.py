import pymongo

class Open5GS:
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.myclient = pymongo.MongoClient("mongodb://" + str(self.server) + ":" + str(self.port) + "/")

    def _GetSubscribers(self):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]
        subs_list = []
        for x in mycol.find():
            subs_list.append(x)
            pass

        return subs_list

    def _GetSubscriber(self, imsi):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]
        myquery = { "imsi": str(imsi)}
        mydoc = mycol.find(myquery)
        for x in mydoc:
            return x

    def _AddSubscriber(self, sub_data):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]

        x = mycol.insert_one(sub_data)
        return x.inserted_id

    def _UpdateSubscriber(self, imsi, sub_data):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]
        print("Attempting to update IMSI " + str(imsi))
        newvalues = { "$set": sub_data }
        myquery = { "imsi": str(imsi)}
        x = mycol.update_one(myquery, newvalues)
        print(x)
        return True

    def _DeleteSubscriber(self, imsi):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]
        myquery = { "imsi": str(imsi)}
        x = mycol.delete_many(myquery)
        # print(x.deleted_count, " subscribers deleted.")
        return x.deleted_count



    #####################################################
    def getSubscribersImsiList(self):
        subs = self._GetSubscribers()
        s_list=[]
        for s in subs:
            s_list.append(s["imsi"])
        return s_list


    def addSubscriber( self , profile:dict ):
        if "imsi" in profile.keys():
            imsi_list = self.getSubscribersImsiList()
            if profile["imsi"] in imsi_list:
                print( "A subscriber with this IMSI is already there." )
            else:
                x = self._AddSubscriber(profile.copy())
        else:
            print( "IMSI is required." )


    def removeAllSubscribers(self):
        subs = self._GetSubscribers()
        for s in subs:
            self._DeleteSubscriber(s["imsi"])


    def removeAllSubscribers_ByObjID(self):
        mydb = self.myclient["open5gs"]
        mycol = mydb["subscribers"]
        for c in mycol.find():
            aa = c["_id"]
            myquery = { "_id": aa }
            mycol.delete_many(myquery)

