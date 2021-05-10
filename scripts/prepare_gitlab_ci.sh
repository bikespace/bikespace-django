#!/bin/bash

echo "deb http://toolbelt.heroku.com/ubuntu ./" > /etc/apt/sources.list.d/heroku.list
wget -O- https://toolbelt.heroku.com/apt/release.key | apt-key add -
apt-get update --quiet --yes
apt-get install --yes gnupg2 libssl-dev build-essential wget ruby-dev heroku-toolbelt
wget --quiet --output-document - https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
source /root/.bashrc
nvm install --lts 
nvm use node
ruby -v
node -v
npm -v
gem install dpl
