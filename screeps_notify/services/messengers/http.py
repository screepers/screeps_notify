
import services.config as config
import requests


class http:

    def __init__(self, settings):
        self.settings = settings

    def sendMessage(self, notification):
        print('sending message from http')

        data = {
            'user': config.settings['screeps_username'],
            'message': notification
        }

        headers = {'user-agent': 'screeps_notify'}
        if 'api-key' in self.settings:
            headers['x-api-key'] = self.settings['api-key']

        if 'http_user' in self.settings:
            r = requests.post(self.settings['url'],
                              json=data,
                              headers=headers,
                              auth=(self.settings['http_user'],
                                    self.settings['http_password']))
        else:
            r = requests.post(self.settings['url'],
                              json=data,
                              headers=headers)

        if r.status_code != requests.codes.ok:
            raise ValueError(
                'http request returned an error %s, the response is:\n%s'
                % (r.status_code, r.text))
        return r.status_code == requests.codes.ok
