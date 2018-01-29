
import json
import services.config as config
import requests
import re


def addLinks(matchobj, shard):
    roomname = matchobj.group(1).upper()
    return "<https://screeps.com/a/#!/room/%s/%s|%s>" % (shard, roomname, roomname)


class slack:

    def __init__(self, settings):
        self.settings = settings

    def sendMessage(self, notification, shard):
        print('sending message from slack')

        user = config.settings['screeps_username']
        message = re.sub(r'([E|W][\d]+[N|S][\d]+)',
                              addLinks,
                              notification,
                              flags=re.IGNORECASE)
        slack_data = {'text': message}

        if 'channel' in self.settings:
            slack_data['channel'] = self.settings['channel']

        if 'username' in self.settings:
            slack_data['username'] = self.settings['username']

        if 'icon_emoji' in self.settings:
            slack_data['icon_emoji'] = self.settings['icon_emoji']

        r = requests.post(self.settings['webhook_url'],
                          data=json.dumps(slack_data),
                          headers={
                            'Content-Type': 'application/json',
                            'user-agent': 'screeps_notify'
                          })

        if r.status_code != requests.codes.ok:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (r.status_code, r.text))

        return r.status_code == requests.codes.ok
