#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from flask import Flask
import multiprocessing

class WXBotServer(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid('hi', msg['user']['id'])


'''
    def schedule(self):
        self.send_msg('tb', 'schedule')
        time.sleep(1)
'''

app = Flask(__name__)
bot = WXBotServer()
botProccess = None
appProcess = None

@app.route("/")
def hello():
    return "Hello, %s" % bot.get_user_id('广超')

def catchKeyboardInterrupt(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except KeyboardInterrupt:
            botProccess.terminate()
            print '\n[*] 强制退出程序'
    return wrapper

@catchKeyboardInterrupt
def main():
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    print '[INFO] bot run.'
    botProccess = multiprocessing.Process(target=bot.run)
    # bot.run()
    print '[INFO] app run.'
    # appProcess = multiprocessing.Process(target=app.run)
    botProccess.start()
    app.run()
    # appProcess.start()

if __name__ == '__main__':
    main()
