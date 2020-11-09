#!usr/bin/env python
# -*- coding: utf-8 -*- 

import paho.mqtt.client as mqtt
import sys

count = 0
# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続完了表示
  client.subscribe("gps/test")  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
    global count
    # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    if(count < 10):
        count += 1
        f = open('GPS_DATA.csv','a')
        f.write(str(msg.payload)+'\n')
        f.close()

# MQTTの接続設定
client = mqtt.Client()                 # インスタンスの作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック

client.connect("localhost", 1883, 60)  # 接続先

client.loop_forever()                  # 待ち続ける