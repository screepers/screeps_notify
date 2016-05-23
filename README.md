# screeps_notify

This project allows players to send text message alerts from inside their
Screeps scripts.


## Requirements

This project depends on [Twilio](https://www.twilio.com) for sending SMS. You
will need an account, which will end up costing $1 a month plus an additional
$0.0075 per text message.


## Settings

The settings file is a yaml file. Begin by copying the settings.dist file to
.settings.yaml in the directory you will be calling `notify.py` from.

```
cp .settings.dist.yaml .settings.yaml
```

The settings file is in yaml and takes various authentication tokens.

```yaml
# Copy this to .settings.yaml and fill it out.

# Screeps account info
screeps_username:
screeps_password:
screeps_ptr: false

# Your Account SID from www.twilio.com/console
twilio_sid:

# Your Auth Token from www.twilio.com/console
twilio_token:

# You SMS number from twilio. https://www.twilio.com/console/phone-numbers/dashboard
sms_from: '+15555555555'

# This should be the number you want to receive the texts.
sms_to: '+15555555555'
```


## Running

To run the program simply call notify.py from the directory your local settings
are in. You may simply wish to add this to a cronjob.

```bash
$ ./screeps_notify/notify.py
```

## Sending Notifications from Screeps

This project includes a javascript module named 'Notify' that is used to queue
messages to be sent.

```js
Notify = require('notify.js')

// Will send immediately
Notify('Test Message')

// Will send immediately, but only once every 100 ticks.
Notify('Rate Limited Message', 100)
```


## Cleanup

In order to make the rate limiting work copies of rate limited messages are kept
in memory. The `Notify` module has a function to clean this up.

```js
Notify = require('notify.js')
Notify.clean()
```

## Thanks!

Special thanks to dhzu for putting together the python code to access the
Screeps API .
