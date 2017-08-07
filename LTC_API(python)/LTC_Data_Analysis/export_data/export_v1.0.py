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
#     "exportpath":"D:\\pandas\\pandas_work\\ipython\\LTC_ipython\\bb.csv"
# }

class TrackAPI(Resource): #获取数据库 
    def post(self):
        data = request.json
        start = data['start']
        end = data['end']
        index = data['index']
        # exportpath = data['exportpath']+'.csv'
        print(start,end,index,exportpath)

        client = pymongo.MongoClient('172.16.100.54',27017)
        ltc_data= client['ltc_collect']
        wamp_history = ltc_data['alarm_history_data']
        cursor = wamp_history.find()
        # result = pd.DataFrame(list(cursor),columns=["collcetion_latest_id","base_topic" ,"dst" ,"src","seq" ,"SNR" , "RSSIpkt" ,"BW", "CR" ,"SF","sensor_id","version" ,"command_id", "data_length", "data" , "mote_lon" , "mote_lat", "time" , "distance2base"])
        result = pd.DataFrame(list(cursor),columns=index)
        data = result[result['time'] >= start]
        data1 = data[data['time'] <= end]
        data_sum = {"data_num":str(data1['seq'].count())}
        print(data_sum)
        data1.to_csv("%s - %s_ltc_data.csv"%(start,end),encoding='utf8')
        return  jsonify(data_sum)

api.add_resource(TrackAPI,'/v1.0/exportdata/csv')

class TrackAPI1(Resource): #获取数据库 
    def post(self):
        data = request.json
        start = data['start']
        end = data['end']
        index = data['index']
        # exportpath = data['exportpath']+".xlsx"
        print(start,end,index,exportpath)

        client = pymongo.MongoClient('172.16.100.54',27017)
        ltc_data= client['ltc_collect']
        wamp_history = ltc_data['alarm_history_data']
        cursor = wamp_history.find()
        # result = pd.DataFrame(list(cursor),columns=["collcetion_latest_id","base_topic" ,"dst" ,"src","seq" ,"SNR" , "RSSIpkt" ,"BW", "CR" ,"SF","sensor_id","version" ,"command_id", "data_length", "data" , "mote_lon" , "mote_lat", "time" , "distance2base"])
        result = pd.DataFrame(list(cursor),columns=index)
        data = result[result['time'] >= start]
        data1 = data[data['time'] <= end]
        data_sum = {"data_num":str(data1['seq'].count())}
        # data1.to_excel(exportpath,sheet_name='Sheet1')
        data1.to_excel("%s - %s_ltc_data.xlsx"%(start,end),sheet_name='Sheet1')
        return  jsonify(data_sum)

api.add_resource(TrackAPI1,'/v1.0/exportdata/xlsx')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
