from flask import Flask,jsonify,request
from flask_restful import Resource
import pandas as pd
from flask_script import Manager
from flask_restful import Api
from flask_mongoengine import MongoEngine
from model import *

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    "host": '172.16.100.54',
    "port": 27017,
    "db": 'ltc_collect'
}

db = MongoEngine(app)
manager = Manager(app)
api = Api(app)


class TrackAPI1(Resource): #获取数据库
    def get(self,):
        l=[]
        data = alarm_history_data.objects.order_by("-_id").limit(100)
        for i in data:
            l.append(i)
        return jsonify(l)

api.add_resource(TrackAPI1,'/v1.0/LTC_data/head/100')
class TrackAPI2(Resource): #获取数据库
    def post(self):
        data = request.json
        print(data)
        show_num = data['show_num']
        # show_num = request.form['show_num']
        l=[]
        data = alarm_history_data.objects.order_by("-_id").limit(int(show_num))
        for i in data:
            l.append(i)
        return jsonify(l)

api.add_resource(TrackAPI2,'/v1.0/LTC_data/head')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
