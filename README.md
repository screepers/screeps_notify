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

## To enable SMS Messages fill out the information below.

# Your Account SID from www.twilio.com/console
twilio_sid:

# Your Auth Token from www.twilio.com/console
twilio_token:

# You SMS number from twilio. https://www.twilio.com/console/phone-numbers/dashboard
sms_from: '+15555555555'

# This should be the number you want to receive the texts.
sms_to: '+15555555555'


## To enable HTTP Messages fill out the information below.

# URL to post to.
http:

# Username, if required.
http_user:

# Password, if required.
http_pass:

# AWS Lambda API Key.
api-key:
```





## Installation

### vagrant

This service can be enabled on a desktop machine using vagrant. First setup the
configuration file as per the instruction below, then provision the machine.

```
vagrant up
```

### docker

1. Clone the repository.
2. Copy settings file - `cp .screeps_settings.dist.yaml .settings.yaml`
3. Edit settings with the appropriate API keys.
4. Build your docker image- `docker build -t screepsnotify .`
5. Test to make sure it works- `docker run --rm screepsnotify`
6. Add a cronjob to call `docker run --rm screepsnotify` as often as you wish.


### Self Hosting

1. Download - `wget $(curl -L -s https://api.github.com/repos/screepers/screeps_notify/releases/latest | grep tarball_url | head -n 1 | cut -d '"' -f 4) -O screepsnotify.tgz`
2. Unpack - `mkdir screepsnotify; tar zxvf screepsnotify.tgz -C ./screepsnotify --strip 1`.
3. Move - `sudo mv screepsnotify /opt/screepsnotify`.
4. Change Directory - `cd /opt/screepsnotify`
5. OPTIONAL: Install Dependencies `sudo ./provisioning/provision.sh`.
6. Configure - `cp .screeps_settings.dist.yaml .screeps_settings.yaml` and then edit.
7. Build - `make`
8. Install - `sudo make install`


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
