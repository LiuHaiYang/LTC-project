import json
from flask import Flask,jsonify,request
from flask_restful import Resource
import pandas as pd
import numpy as np
from flask_restful import Api
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession,ApplicationRunner
from autobahn.wamp.exception import ApplicationError
from os import environ
app = Flask(__name__)
api = Api(app)

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        def onhello(msg):
            self.log.info("received: {msg}", msg=msg)
            data_json = json.loads(msg)
            time = data_json['time']
            RSSIpkt = data_json['RSSIpkt']
            seq = data_json['seq']
            time1 = []
            for i in time.split(" "):
                time1.append(i)
            time2 = time1[1]
            print(time2,-int(RSSIpkt),seq)

            real_data ={"time":time,"RSSIpkt":-int(RSSIpkt),"seq":seq}
            self.publish('LTC_real_data', real_data)
            self.log.info("published  {real_data}",
                          real_data=real_data)
        yield self.subscribe(onhello, 'LTC-server-test')
        
        
            
        

if __name__ == '__main__':
    runner = ApplicationRunner(
    environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://www.wugeek.cn:8090/ws"),  # "ws://www.wugeek.cn:8090/ws";String realm = "realm1";
    u"realm1",
    )
    runner.run(AppSession)