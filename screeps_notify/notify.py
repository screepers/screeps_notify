#!/usr/bin/env python

import requests
from screeps import ScreepsConnection
import sys
import time
from twilio.rest import TwilioRestClient
import logging
import os
import yaml

base_directory = os.path.expanduser('~')
if not os.path.exists(base_directory):
    os.makedirs(base_directory)


def getSettings():
    if not getSettings.settings:
        cwd = os.getcwd()
        path = cwd + '/.settings.yaml'
        if not os.path.isfile(path):
            print 'no settings file found'
            sys.exit(-1)
            return False
        with open(path, 'r') as f:
            getSettings.settings = yaml.load(f)
    return getSettings.settings
getSettings.settings = False


def getScreepsConnection():
    if not getScreepsConnection.sconn:
        settings = getSettings()
        getScreepsConnection.sconn = ScreepsConnection(
            u=settings['screeps_username'],
            p=settings['screeps_password'],
            ptr=settings['screeps_ptr'])
    return getScreepsConnection.sconn
getScreepsConnection.sconn = False


def getNotifications():
    sconn = getScreepsConnection()
    notifications = sconn.memory(path='__notify')
    if 'data' not in notifications:
        return False
    return notifications['data']


def clearNotifications(tick=0):
    print 'clearing sent messages'
    sconn = getScreepsConnection()
    javascript_clear = 'var limit=' + str(tick) + ';'
    javascript_clear += "if(typeof limit == 'undefined') var limit = 0; Memory.__notify = _.filter(Memory.__notify, function(notification){ return notification.tick > this.limit }.bind({'limit':limit}))"
    sconn.console(javascript_clear)


def sendSMS(notification):
    message = 'Screeps: ' + notification['message']
    settings = getSettings()

    if 'twilio_sid' not in settings:
        print('skipping sms due to lack of settings.')
        return

    smsclient = TwilioRestClient(settings['twilio_sid'],
                                 settings['twilio_token'])
    message = smsclient.messages.create(
        body=message,
        to=settings['sms_to'],    # Replace with your phone number
        from_=settings['sms_from'])  # Replace with your Twilio number
    print(message.sid)


def sendHTTP(notification):
    settings = getSettings()

    if 'http' not in settings:
        print('skipping http due to lack of settings.')
        return

    notification['user'] = settings['screeps_username']
    headers = {
        'user-agent': 'screeps_notify',
    }

    if 'api-key' in settings:
        headers['x-api-key'] = settings['api-key']

    print headers
    if 'http_user' in settings:
        r = requests.post(settings['http'],
                          json=notification,
                          headers=headers,
                          auth=(settings['http_user'],
                                settings['http_password']))
    else:
        r = requests.post(settings['http'],
                          json=notification,
                          headers=headers)

        print r.text
        print r.status_code
        return r.status_code == requests.codes.ok


class App():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        # self.stdout_path = base_directory + '/screepsnotify.out'
        self.stderr_path = base_directory + '/screepsnotify.err'
        self.pidfile_path = base_directory + '/screepsnotify.pid'
        self.pidfile_timeout = 5

    def run(self):
        logging.basicConfig(level=logging.WARN)
        logger = logging.getLogger("ScreepsNotify")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(base_directory + "/screepsnotify.log")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        while True:
            notifications = getNotifications()
            if not notifications or len(notifications) <= 0:
                print 'No notifications to send.'
                sys.exit(0)
            limit = 0
            print 'Sending notifications.'
            for notification in notifications:
                if notification['tick'] > limit:
                    limit = notification['tick']
                sendSMS(notification)
                sendHTTP(notification)
            clearNotifications(limit)
            time.sleep(5)


if __name__ == '__main__':
    app = App()
    app.run()
