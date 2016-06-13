
SHELL:=/bin/bash
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: all fresh dependencies install fulluninstall uninstall removedeps


all: dependencies

fresh: fulluninstall dependencies

fulluninstall: uninstall cleancode

install:
	# Create link in /usr/local/bin to screeps notification program.
	ln -s -f $(ROOT_DIR)/bin/screepsnotify.sh /usr/local/bin/screepsnotify

	# Create link in /usr/local/bin to standalone service controller.
	ln -s -f $(ROOT_DIR)/bin/screepsnotifyctl.sh /usr/local/bin/screepsnotifyctl

	# Create screepsstats user- including home directory- for daemon
	id -u screepsnotify &>/dev/null || useradd screepsnotify --create-home --shell /bin/false -U

	# Move service file into place- note that symlinks will not work (bug 955379)
	if [ -d /etc/systemd/system ]; then \
		cp $(ROOT_DIR)/provisioning/etc/systemd/system/screepsnotify.service /etc/systemd/system/screepsnotify.service; \
		systemctl enable screepsnotify.service; \
		systemctl start screepsnotify.service; \
	fi;

dependencies:
	if [ ! -d $(ROOT_DIR)/env ]; then virtualenv $(ROOT_DIR)/env; fi
	source $(ROOT_DIR)/env/bin/activate; pip install -r $(ROOT_DIR)/requirements.txt

uninstall:
	# Remove user and home.
	if getent passwd screepsnotify > /dev/null 2>&1; then \
		pkill -9 -u `id -u screepsnotify`; \
		deluser --remove-home screepsnotify; \
	fi
	# Remove screepsstats link in /user/local/bin
	if [ -L /usr/local/bin/screepsnotify.sh ]; then \
		rm /usr/local/bin/screepsnotify; \
	fi;
	# Remove screepsstatsctl in /user/local/bin
	if [ -L /usr/local/bin/screepsnotifyctl.sh ]; then \
		rm /usr/local/bin/screepsnotifyctl; \
	fi;
	# Shut down, disbale, and remove all services.
	if [ -L /etc/systemd/system/screepsnotify.service ]; then \
		systemctl disable screepsnotify.service; \
		systemctl stop screepsnotify.service; \
		rm /etc/systemd/system/screepsnotify.service; \
	fi;

cleancode:
	# Remove existing environment
	if [ -d $(ROOT_DIR)/env ]; then \
		rm -rf $(ROOT_DIR)/env; \
	fi;
	# Remove compiled python files
	if [ -d $(ROOT_DIR)/screep_notify ]; then \
		rm -f $(ROOT_DIR)/screep_notify/*.pyc; \
	fi;
