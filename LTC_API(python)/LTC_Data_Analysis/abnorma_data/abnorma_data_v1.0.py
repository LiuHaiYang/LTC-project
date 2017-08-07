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
#     "index":["RSSIpkt","time" ],
# }

'''
异常值的衡量标准
上边界 和 下边界
l= data2[index1].describe().astype(np.int64).T
Q1 = l[4]
Q3 = l[6]
IQR = Q1-Q3
up_border = Q3 + 1.5*IQR
below_border = Q1 - 1.5*IQR
'''
class TrackAPI(Resource): #获取数据库 
    def post(self):
        data = request.json
        start = data['start']
        end = data['end']
        index = data['index']
        index1 = data['index'][0]
        print(start,end,index,index1)

        client = pymongo.MongoClient('172.16.100.54',27017)
        ltc_data= client['ltc_collect']
        wamp_history = ltc_data['alarm_history_data']
        cursor = wamp_history.find()
        index_1 = ["base_topic" ,"dst" ,"src","seq" ,"SNR" , "RSSIpkt" ,"BW", "CR" ,"SF","sensor_id","version" ,"command_id", "data_length", "data" , "mote_lon" , "mote_lat", "time" , "distance2base"]
        result = pd.DataFrame(list(cursor),columns=index_1)
        data = result[result['time'] >= start]
        data1 = data[data['time'] <= end]
        data2= pd.DataFrame(data1,columns=[[index1,'abnorma']])
        # 异常值判断
        l= data2[index1].describe().astype(np.int64).T
        Q1 = l[4]
        Q3 = l[6]
        IQR = Q1-Q3
        up_border = Q3 + 1.5*IQR
        below_border = Q1 - 1.5*IQR
        lll = []
        for i in data2['abnorma']:
            lll.append(i)
        ll = []
        for i in data2['RSSIpkt']:
            ll.append(i)
        data_index = data2['RSSIpkt']
        for i in range(len(ll)):
            if ll[i] < below_border  and ll[i] > up_border:
                lll[i] ='F'
            else:
                lll[i] ='T'
        data_abnorma= pd.DataFrame(ll,columns=['abnorma'])
        data_RSSIpkt= pd.DataFrame(lll,columns=['RSSIpkt'])
        # data_all = pd.merge(data_abnorma,data_RSSIpkt,left_index=True,right_index=True,how='outer')
        data_all = pd.merge(result,data_abnorma,left_index=True,right_index=True,how='outer')

        data_j = data_all.to_json(orient="index")
        # data_json = json.dump(data_j)
        data_json = json.loads(data_j)
        return  data_json #jsonify(data1)

api.add_resource(TrackAPI,'/v1.0/abnorma_data')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002)