from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
from mlx90614 import MLX90614
import paho.mqtt.client as mqtt
#import time
import hashlib
import hmac
import random
import json
#import numpy as np
#这个就是我们在阿里云注册产品和设备时的三元组啦
#把我们自己对应的三元组填进去即可
# options = {
#     'productKey':'gbto9CuyOjb',
#     'deviceName':'device1',
#     'deviceSecret':'4077ede63cdab9f447af1b940c1518ab',
#     'regionId':'cn-shanghai'
# }
# 
# HOST = options['productKey'] + '.iot-as-mqtt.'+options['regionId']+'.aliyuncs.com'
# PORT = 1883 
# PUB_TOPIC = "/sys/" + options['productKey'] + "/" + options['deviceName'] + "/thing/event/property/post";
# 
# 
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     # client.subscribe("the/topic")
# 
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))
# 
# def hmacsha1(key, msg):
#     return hmac.new(key.encode(), msg.encode(), hashlib.sha1).hexdigest()
# 
# def getAliyunIoTClient():
# 	timestamp = str(int(time.time()))
# 	CLIENT_ID = "paho.py|securemode=3,signmethod=hmacsha1,timestamp="+timestamp+"|"
# 	CONTENT_STR_FORMAT = "clientIdpaho.pydeviceName"+options['deviceName']+"productKey"+options['productKey']+"timestamp"+timestamp
# 	# set username/password.
# 	USER_NAME = options['deviceName']+"&"+options['productKey']
# 	PWD = hmacsha1(options['deviceSecret'],CONTENT_STR_FORMAT)
# 	client = mqtt.Client(client_id=CLIENT_ID, clean_session=False)
# 	client.username_pw_set(USER_NAME, PWD)
# 	return client

thermometer_address = 0x5a

thermometer = MLX90614(thermometer_address)
#百度人脸识别API账号信息
APP_ID = '24691172 '
API_KEY = 'yP16X8sngLX3dSiqTnYoZxgT'
SECRET_KEY ='jqUa2ZgjuzbGwOtm6OVxHIIM8TMWSoPB'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象
#用户组
GROUP = 'test'
 

#ranhou fanhui yige duixiang
# class mycanshu:
#     flag=0
#     name='xxx'
#     curren_time='0'
#     Temperature=0.0
#     
# canshu=mycanshu()
#total_flag=0
list2=["tom"]#全体学生name
list_yi=[]
list_wei=list2

#照相函数
def getimage():
    camera.resolution = (1024,768)#摄像界面为1024*768
    camera.start_preview()#开始摄像
    time.sleep(2)
   
    camera.capture('faceimage.jpg')#拍照并保存
    
    #time.sleep(2)
#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img

#上传到百度api进行人脸检测
#zhe ge di fang kan lai de ding yi yi ge can shu dui xiang
def go_api(image,canshu):
    Temperature=0.0
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    #print(result['error_msg'])
    if result['error_msg'] == 'SUCCESS':#如果成功了
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        #print(score)
        if score > 80:#如果相似度大于80
            if name == 'tom':
 
                print("欢迎%s !" % name)
                print("属实人员，请测温")
                Temperature=thermometer.get_obj_temp()
                print('people:')
                print(Temperature)
                time.sleep(3)
            if name == 'Jerry':
                print("欢迎%s !" % name)
                print("属实人员，请测温")
                Temperature=thermometer.get_obj_temp()
                print('people:')
                print(Temperature)
                time.sleep(3)
            if name == "xiaoyu":
                print("欢迎%s !" % name)
                print("属实人员，请测温")
                Temperature=thermometer.get_obj_temp()
                print('people:')
                print(Temperature)
        else:
            print("对不起，我不认识你！")
            name = 'Unknow'
            canshu.flag=0
            return canshu
        curren_time = time.asctime(time.localtime(time.time()))#获取当前时间
 
        #将人员出入的记录保存到Log.txt中
        f = open('Log.txt','a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time)+ "     " + "Temperature:" + str(Temperature)+'\n')
        canshu.name=name
        canshu.curren_time=curren_time
        canshu.Temperature=Temperature
        f.close()
        
        if name in list_wei:
            list_yi.append(name)
            list_wei.remove(name)
        
        canshu.flag=1
        return canshu
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        time.sleep(2)
        canshu.flag=0
        return canshu
    else:
        print(str(result['error_code'])+' '+ str(result['error_code']))
        #print('ying gai shi zhe ge cuo wu!')
        canshu.flag=0
        return canshu
#主函数if __name__ == '__main__' def woshimain
def woshimain():
#     Aliyunclient = getAliyunIoTClient()
#     Aliyunclient.on_connect = on_connect
#     Aliyunclient.on_message = on_message
# 
#     Aliyunclient.connect(HOST, 1883, 300)
    
    #ranhou fanhui yige duixiang
    class mycanshu:
        flag=0
        name='xxx'
        curren_time='0'
        Temperature=0.0
        
    canshu=mycanshu()
    #total=[]
    while True:
        print('准备')
        if True:
            getimage()#拍照
            img = transimage()#转换照片格式
            canshu = go_api(img,canshu)#将转换了格式的图片上传到百度云
            
            if(canshu.flag == 1):#是人脸库中的人
                #print('hahhahahhahahh')
                #total=[total,canshu2]
                #print(total)
#                 payload_json = {
#                     'id': int(time.time()),
#                     'params': {
#                         'name': canshu.name,#人名
#                         'Current_Time':canshu.curren_time,
#                         'AnimalTemperature':canshu.Temperature#体温
#                         #'total':total
#                     },
#                     'method': "thing.event.property.post"
#                 }
#                 print('send data to iot server: ' + str(payload_json))
# 
#                 Aliyunclient.publish(PUB_TOPIC,payload=str(payload_json),qos=1)
                return canshu
            else:
                print("非法人员，禁止进入！")
            #print('稍等三秒进入下一个')
            #Aliyunclient.loop_forever()
            #time.sleep(3)

