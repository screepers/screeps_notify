#!/usr/bin/env python

import screepsapi
import sys
import time

import logging
import os
import traceback
import yaml

import services.config as config
import services.messenger as messenger


def getScreepsConnection():
    if not getScreepsConnection.sconn:
        settings = config.getSettings()
        if 'screeps_token' in settings:
            getScreepsConnection.sconn = screepsapi.API(
                token=settings['screeps_token'],
                ptr=settings['screeps_ptr'])
        else:
            getScreepsConnection.sconn = screepsapi.API(
                u=settings['screeps_username'],
                p=settings['screeps_password'],
                ptr=settings['screeps_ptr'])
    return getScreepsConnection.sconn
getScreepsConnection.sconn = False


def getNotifications(shard):
    sconn = getScreepsConnection()
    notifications = sconn.memory(path='__notify_v2', shard=shard)
    if 'data' not in notifications:
        return False
    notificationMap = notifications['data']
    messages = []
    for messageId, message in notificationMap.items():
        if isinstance(message, dict):
            message['messageId'] = messageId
            message['shard'] = shard
            messages.append(message)
    return messages


def clearNotification(messageId, shard='shard0'):
    print 'clearing sent messages'
    sconn = getScreepsConnection()
    sconn.set_memory('__notify_v2.%s' % messageId, None, shard)
    settings = config.getSettings()
    if 'screeps_ivm' in settings and settings['screeps_ivm']:
        message = "delete Memory.__notify_v2['%s']; 'ScreepsNotify: Clearing message %s'"
        sconn.console(message % (messageId, messageId), shard=shard)


class App():

    def run(self):
        try:
            api = getScreepsConnection()
            shard_data = api.shard_info()['shards']
            shards = [x['name'] for x in shard_data]
            if len(shards) < 1:
                shards = ['shard0']
        except:
            shards = ['shard0']

        for shard in shards:
            print('Checking for notifications on %s' % (shard,))
            notifications = getNotifications(shard)
            if not notifications or len(notifications) <= 0:
                print 'No notifications to send.'
                continue

            print 'Sending notifications.'
            for notification in notifications:
                msgid = notification['messageId']
                if 'groups' in notification:
                    groups = notification['groups']
                else:
                    groups = ['default']
                services = config.getServicesFromGroups(groups)
                for service in services:
                    try:
                        driver = messenger.getMessengerDriver(service)
                        driver.sendMessage(notification['message'], shard)
                    except:
                        traceback.print_exc()
                clearNotification(msgid, shard)


def lambda_handler(event,context):
    app = App()
    app.run()

if __name__ == '__main__':
    app = App()
    app.run()
