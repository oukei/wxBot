#!/usr/bin/env python
# coding: utf-8

from wxbot import *
from flask import Flask
import threading
import pickle
import os

class WXBotServer(WXBot):
    def on_monitor(self):
        print 'dump bot to file'
        with open(path, 'wb') as f:
            pickle.dump(bot, f)

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
path = 'wxbox.dat'

@app.route("/")
def hello():
    # print bot.contact_list
    return "Hello, World"

def catchKeyboardInterrupt(fn):
    def wrapper(*args):
        try:
            return fn(*args)
        except KeyboardInterrupt:
            print '\n[*] 强制退出程序'
    return wrapper

@catchKeyboardInterrupt
def main():
    global bot
    global app
    if os.path.isfile(path):
        print 'read bot from file'
        with open(path, 'rb') as f:
            bot = pickle.load(f)
        botThread = threading.Thread(target=bot.proc_msg)
        botThread.setDaemon(True)
        botThread.start()
    else:
        bot.DEBUG = True
        bot.conf['qr'] = 'png'
        print '[INFO] bot run.'
        botThread = threading.Thread(target=bot.run)
        botThread.setDaemon(True)
        botThread.start()

    print '[INFO] app run.'
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()
