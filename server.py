#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from flask import Flask
import threading

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
botThread = None

@app.route("/")
def hello():
    print bot.contact_list
    return "Hello, %s" % bot.get_user_id(u'广超')

def catchKeyboardInterrupt(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except KeyboardInterrupt:
            # botThread.
            print '\n[*] 强制退出程序'
    return wrapper

@catchKeyboardInterrupt
def main():
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    print '[INFO] bot run.'
    botThread = threading.Thread(target=bot.run)
    botThread.start()
    print '[INFO] app run.'
    app.run()

if __name__ == '__main__':
    main()
