
import json
import services.config as config
import requests


class slack:

    def __init__(self, settings):
        self.settings = settings

    def sendMessage(self, notification):
        print('sending message from slack')

        url = self.settings['webhook_url']
        user = config.settings['screeps_username']
        message = '%s: %s' % (user, notification)
        slack_data = {'text': message}

        r = requests.post(self.settings['webhook_url']
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
