# import json
# def test():
#     msg= { "baseTopic": "LTC-base1", "src": "2", "dst": "_1", "seq": "9", "SNR": "-9", "RSSIpkt": "-54", "BW": "125", "CR": "4/5", "SF": "12", "sensor_id": "1", "version": "1", "command_id": "1", "data_length": "4", "data": "Ping", "mote_lon": "114.513122", "mote_lat": "36.577103", "time": "2017-06-24 09:38:19"}
#     data_json = msg
#     time = data_json['time']
#     RSSIpkt = data_json['RSSIpkt']
#     seq = data_json['seq']
#     time1 = []
#     for i in time.split(" "):
#         time1.append(i)
#     time2 = time1[1]
#     print(time2,-int(RSSIpkt),seq)
# test()

# b = "SB"
# bb ="Hello"
# print("%s say:%s"%(b,bb))
# print("say: %s"%(bb))


start="2017-07-25 07:43:25"
end="2017-07-26 07:43:25"
print("%s - %s_ltc_data.csv"%(start,end))
