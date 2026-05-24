#!/bin/bash
apt-get update -q
apt-get install -y python3 python3-pip
pip3 install pika
echo "Produtor pronto!"