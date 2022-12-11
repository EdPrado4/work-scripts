#! /usr/bin/env bash

# Script to configure simple rules on Iptables

# Check if script is run as root

if [ "$(id -u)" -ne  0 ] ;then
  echo "please run me as root"
  exit 1
fi

# Setting policies as ACCEPT by default

iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# Defining Host IP
HOST_IP="192.168.56.1" 

# Deleting current rules and Policies
echo "Deleting previous configurations ..."
iptables -F && iptables -X
echo "Done!"

iptables -nL

echo -e "\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n"


# Setting all policies as DROP by default

echo "Setting Policies as DROP ..."

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP

echo "Done!"
iptables -nL

echo -e "\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n"

# Communicate with host and allow all over localhost

echo "Setting rules to allow traffic from external host and localhost ..."

iptables -A INPUT -s "$HOST_IP" -j ACCEPT 
iptables -A OUTPUT -d "$HOST_IP" -j ACCEPT 
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o la -j ACCEPT

echo "Done!"
iptables -nL

# Allowing DNS traffic for tcp/udp protocols

echo -e "\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n"


echo "Allowing TCP/UDP traffic over DNS ..."

iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --sport 53 -j ACCEPT
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p udp --sport 53 -j ACCEPT

echo "Done!"
iptables -nL

echo -e "\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n"

echo "Allowing traffic over ports 80 (http) and 443(https):"

# Allow traffic over port 80 (HTTP)

iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --sport 80 -j ACCEPT

# Allow traffic over port 443 (HTTPS)

iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --sport 443 -j ACCEPT

echo "Done!"

iptables -nL

echo -e "\n-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n"


