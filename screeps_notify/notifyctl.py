#!/usr/bin/env python

from daemon import runner
import notify

if __name__ == "__main__":
    app = notify.App()
    daemon_runner = runner.DaemonRunner(app)
    daemon_runner.do_action()
