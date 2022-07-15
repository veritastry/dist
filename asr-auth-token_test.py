import requests
import json
import random
import time
import logging

lnserver = 'http://120.201.104.114:8003'
zjserver = 'http://112.17.0.26:8003'
url = zjserver + "/asr-auth/token/apply"
client_id = 'com.cm.speech.asr'
xlexleclientid = 'ysxk.ovs.client.1628045025661'
sid = '0322fce0ffa96375682adffbf48407c8'


class TokenManager:
    def __init__(self, *args):
        self.url = args[0]
        self.client_id = args[1]
        self.secret = args[2]
        logging.debug("url:" + self.url + "\nclient_id:" + self.client_id + "\nsecret:" + self.secret)

    def fetch_token(self):
        duration = [0.1, 0.5, 0.7]
        times = 0
        while (times < 3):
            response = requests.get(self.url, {
                'client_id': self.client_id,
                'client_secret': self.secret
            })
            info = json.loads(response.text)
            logging.debug('response code:' + info['code'])
            if info['code'] == 'success':
                return info['token'], info['expire_duration']
            else:
                time.sleep(1)
                times += 1
        return 'not et error'
        print("fetch token failed for 3 times...")


def main():
    tm = TokenManager(url, xlexleclientid, sid)
    logging.debug('get tokenmanager')
    tkn, exp = tm.fetch_token()
    logging.debug('token:' + tkn + 'expire_duration:' + exp)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    main()
