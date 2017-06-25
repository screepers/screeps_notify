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


### Screeps Settings

```yaml

# Screeps account info
screeps_username:
screeps_password:
screeps_ptr: false
```


### Define Services

Services are used by the system to send messages. Currently there are three
service types (HTTP, Slack, and SMS), each of which can be used multiple times
(for instance, you can define multiple slack hooks to send different types of
messages to different channels).

```yaml
services:

  sms:
    # Set driver to twilio
    type: sms

    # Your Account SID from www.twilio.com/console
    twilio_sid:

    # Your Auth Token from www.twilio.com/console
    twilio_token:

    # You SMS number from twilio. https://www.twilio.com/console/phone-numbers/dashboard
    sms_from: '+15555555555'

    # This should be the number you want to receive the texts.
    sms_to: '+15555555555'

  alliance:
    # Set driver to HTTP
    type: http

    # Specify a url
    url: https://example.execute-api.us-east-1.amazonaws.com/prod/service

    # Provide an API key for AWS Gateway (optional)
    api-key:

  logs:
    # Set driver to HTTP
    type: http

    # Specify a url
    url: https://example.execute-api.us-east-1.amazonaws.com/prod/service

    # Provide an API key for AWS Gateway (optional)
    api-key:

  slack:
    # Set driver to SLACK
    type: slack

    # Specify a url
    webhook_url:

    # Optionally set a channel. If not set the webhook default will be used.
    channel:

    # Optionally set a username.
    username:

    # Optionally specify an emoji as a user icon
    icon_emoji:
```


### Define Groups

Groups define which services get used when a notification is sent. At a minimum
a `default` group should be set.

Groups can either be an array of services or the string `all` (which will make
sure the group sends a message to all available services).

```yaml
groups:

  default:
    - sms
    - logs
    - slack

  economy:
    - sms
    - logs

  defense: all
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


### AWS Lambda

Even when run every second the load is more than low enough to qualify for the
free tier.

1. Clone the repository.
2. Copy settings file - `cp .screeps_settings.dist.yaml .settings.yaml`
3. Edit settings with the appropriate API keys.
4. Build the lambda package- `make lambda`
5. Upload zip to lambda using `notify.lambda_handler` as the handler


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

// Will send only to the economy group services, and only once every 100 ticks.
Notify('Rate Limited Group Message', 100, ['economy'])

// Will send immediately but only to the defense group services
Notify('Rate Limited Group Message', false, ['defense'])
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
