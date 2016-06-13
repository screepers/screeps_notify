#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )"
cd $DIR
pwd

apt_quiet_install () {
   echo "** Install package $1 **"
   DEBIAN_FRONTEND=noninteractive apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" -y -f -q install $1
}


# Install Development Tools
echo "** Install Development Tools **"
apt_quiet_install git
apt_quiet_install python-dev
apt_quiet_install python-pip


echo "** Install virtualenv **"
pip install virtualenv


echo "** make screeps-stats project **"
cd $DIR/../
make

echo "** install screeps-stats project **"
make install


if [ -f "$DIR/../.screeps_settings.yaml" ]; then
  echo "** Settings Found: Launching Stats Daemon **"
  systemctl start screepsstats.service
fi

