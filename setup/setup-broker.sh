#!/bin/bash
apt-get update -q
apt-get install -y rabbitmq-server
systemctl enable rabbitmq-server
systemctl start rabbitmq-server

rabbitmqctl add_user meuapp senha123
rabbitmqctl set_user_tags meuapp administrator
rabbitmqctl set_permissions -p / meuapp ".*" ".*" ".*"

rabbitmq-plugins enable rabbitmq_management

echo "listeners.tcp.default = 0.0.0.0:5672" >> /etc/rabbitmq/rabbitmq.conf
echo "management.tcp.port = 15672"          >> /etc/rabbitmq/rabbitmq.conf

systemctl restart rabbitmq-server
echo "Broker RabbitMQ pronto!"