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
        getScreepsConnection.sconn = screepsapi.API(
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


class App():

    def run(self):
        notifications = getNotifications()
        if not notifications or len(notifications) <= 0:
            print 'No notifications to send.'
            return
        limit = 0
        print 'Sending notifications.'
        for notification in notifications:
            if notification['tick'] > limit:
                limit = notification['tick']

            if 'groups' in notification:
                groups = notification['groups']
            else:
                groups = ['default']

            services = config.getServicesFromGroups(groups)
            for service in services:
                try:
                    driver = messenger.getMessengerDriver(service)
                    driver.sendMessage(notification['message'])
                except:
                    traceback.print_exc()

        clearNotifications(limit)

def lambda_handler(event,context):
    app = App()
    app.run()

if __name__ == '__main__':
    app = App()
    app.run()
