#!/usr/bin/env python2
# coding=utf-8
'''
author : hyq 
for websocket interface     

'''
import json
import os
import time
import sys
import codecs
import websocket
from websocket import ABNF
import requests
import random
import uuid
import threading
from threading import Lock


# reload(sys)
# sys.setdefaultencoding('utf-8')
#passport 接口
# https://passport.ainirobot.com:8888/account/bind
# 填入语音识别url地址
#ASR_URL = 'http://asr.easestar.cn/v2/asr'
# 填入需要识别语音文件路径
#AUDIO_PATH = 'test.wav'
# 按照语音格式来填写，wav为pcm，（更多信息请参见开发文档https://speech.yitutech.com/devdoc/shortaudio 第2部分音频要求）
AUDIO_AUE = 'pcm'

 

MAX_RETRY = 10


class TokenRefresh:

    def __init__(self, url, id, secret):
        self.url = url
        self.id = id
        self.secret = secret
        self.token = ''
        self.lock = Lock()
        self.event = threading.Event()
        self.stop_flag = False

    def refresh_proc(self):
        print('#refresh proc start#')
        while (self.stop_flag != True):
            token, expire_duation = self.fetch_token()
            self.lock.acquire()
            self.token = token
            self.lock.release()
            # 休眠（7200 - 300）秒
            self.event.wait(int(expire_duation) - 300)
            print('#refresh#')
        print('#refresh proc end#')

    def fetch_token(self):
        duration = [0.1, 0.5, 0.7]
        times = 0
        while (times < 3):
            response = requests.get(self.url, {
                'client_id': self.id,
                'client_secret': self.secret
            })
            info = json.loads(response.text)
            if info['code'] == 'success':
                return info['token'], info['expire_duration']
            else:
                time.sleep(random.sample(duration))
                times += 1
        print("fetch token failed for 3 times...")

    def get_token(self):
        self.lock.acquire()
        token = self.token
        self.lock.release()
        return token

    def start(self):
        refresh_thread = threading.Thread(target=self.refresh_proc)
        refresh_thread.start()
        # sleep for child thread
        time.sleep(1)

    def stop(self):
        self.stop_flag = True
        self.event.set()
        print('#token refresh stop#')



class ASR(object):

    def __init__(self, url, token,  wavfile):
        self.url = url
        self.token = token
        self.counter = 0
        self.wavfile = wavfile
        self.interval = 500
        self.sample_rate = 16
        #print("token:", token)

    def on_message(self, ws, message):
        #print("message:", message)
        asr_result = json.loads(message)
        print('recvd: ',message)
        if asr_result["asr_param"]["err_no"] != 0:
            print("\nsid: %s, error: %s" %(self.sid, asr_result["asr_param"]["error"]))
        elif asr_result["asr_param"]["end_flag"] == 1:
            nbest = asr_result["asr_content"]["nbest"][0]
            print("\nsid: %s, result: %s" %(self.sid, nbest))

    def on_error(self, ws, error):
        print("error:", error)
        self.ws.close()

    def on_open(self, ws):
        #print("on_open")
        self.send_first()
        with open(self.wavfile, "rb") as audio_file:
            _ = audio_file.read(44)
            while True:
                data = audio_file.read(int (2 * self.interval * self.sample_rate))
                if not data:
                    print("send out, no data left")
                    break
                time.sleep(0.01)
                self.send_data(data)
        self.send_final()

    def on_close(self, ws, a1, a2):
        #print("### closed ###")
        self.ws.close()

    def running(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header={"Authorization": "Bearer " + self.token})
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def send_first(self):
        self.sid = str(uuid.uuid1())
        message = json.dumps({
            'sid': self.sid,
            'pid': 7017,
            'devid': 'asr-client',
            'protocol': '0',
            'audio_type': 0,
            'lang': 1
        })
        #print('first:', message)
        self.ws.send(message)
        self.counter += 1

    def send_data(self, message):
        self.counter += 1
        #print("counter:", str(self.counter))
        self.ws.send(message, ABNF.OPCODE_BINARY)

    def send_final(self):
        message = json.dumps({'total': str(self.counter)})
        #print('final:', message)
        self.ws.send(message)

  


# def test():
def start():
    audio_file = sys.argv[1]
    #wsurl = "ws://asrfjzp.easestar.cn:8003/ws/streaming-asr"
    wsurl = "ws://36.155.71.60:8003/ws/streaming-asr"
    #wsurl = "ws://120.201.104.114:8003/ws/streaming-asr"
        # 动态刷新token
    tf = TokenRefresh('http://36.155.71.60:8003/asr-auth/token/apply',
    #tf = TokenRefresh('http://asrfjzp.easestar.cn:8003/asr-auth/token/apply',
    #tf = TokenRefresh('http://112.50.246.202:8003/asr-auth/token/apply',
                 "com.cm.speech.asr", "0322fce0ffa96375682adffbf48407c8")
    tf.start()
    number = 0
    try:
        #asr = ASR(wsurl, "0322fce0ffa96375682adffbf48407c8", key, audio, trans_file)
        #asr = ASR(wsurl, "0322fce0ffa96375682adffbf48407c8", audio_file)
        asr = ASR(wsurl, tf.get_token(), audio_file)
        asr.running()
    except Exception as e:
        sys.stderr.write( str(e) + " exception, retrying.\n")
        sys.stderr.flush()
        time.sleep(0.1)
    tf.stop()        


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("asr_api_test.py  <./七点叫我起床.pcm>\n")
        exit(-1)
    start()
