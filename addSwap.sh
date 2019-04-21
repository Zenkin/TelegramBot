#!/bin/bash

sudo fallocate -l $1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo echo "/swapfile swap swap defaults 0 0" >> /etc/fstab
sudo echo "vm.swappiness=10" >> /etc/sysctl.conf
sudo sysctl -p
sudo swapon --show
sudo free -h