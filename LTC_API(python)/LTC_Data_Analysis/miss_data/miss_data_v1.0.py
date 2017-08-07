import json
from flask import Flask,jsonify,request
from flask_restful import Resource
import pandas as pd
import numpy as np
from flask_restful import Api
import pymongo
app = Flask(__name__)
api = Api(app)
# {
#     "start":"2017-07-25 07:43:25",
#     "end":"2017-07-26 07:43:25",
#     "index":["base_topic" , "dst" , "src" , "seq" , "SNR" , "RSSIpkt" , "BW" , "CR" , "SF" , "sensor_id" , "version", "command_id", "data_length" , "data" , "mote_lon" , "mote_lat" , "time" ],
# }

class TrackAPI(Resource): #获取数据库 
    def post(self):
        data = request.json
        start = data['start']
        end = data['end']
        index = data['index']
        print(start,end,index)

        client = pymongo.MongoClient('172.16.100.54',27017)
        ltc_data= client['ltc_collect']
        wamp_history = ltc_data['alarm_history_data']
        cursor = wamp_history.find()
        # result = pd.DataFrame(list(cursor),columns=["collcetion_latest_id","base_topic" ,"dst" ,"src","seq" ,"SNR" , "RSSIpkt" ,"BW", "CR" ,"SF","sensor_id","version" ,"command_id", "data_length", "data" , "mote_lon" , "mote_lat", "time" , "distance2base"])
        result = pd.DataFrame(list(cursor),columns=index)
        data = result[result['time'] >= start]
        data1 = data[data['time'] <= end]
        # print(data1.dtypes)
        data2 =  data1[data1['data'] == "," ]           
        data_j = data2.to_json(orient="index")
        # data_json = json.dump(data_j)
        data_json = json.loads(data_j)
        return  data_json #jsonify(data1)

api.add_resource(TrackAPI,'/v1.0/miss_data')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002)
