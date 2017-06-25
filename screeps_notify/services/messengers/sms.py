
from twilio.rest import TwilioRestClient


class sms:

    def __init__(self, settings):
        self.settings = settings
        self.smsclient = False

    def getClient(self):
        if self.smsclient:
            return self.smsclient
        assert 'twilio_sid' in self.settings
        self.smsclient = TwilioRestClient(self.settings['twilio_sid'],
                                          self.settings['twilio_token'])
        return self.smsclient

    def sendMessage(self, notification):
        print('sending message from sms')
        message_text = 'Screeps: ' + notification
        message = self.getClient().messages.create(
            body=message_text,
            to=self.settings['sms_to'],    # Replace with your phone number
            from_=self.settings['sms_from'])  # Replace with your Twilio number
        print(message.sid)

