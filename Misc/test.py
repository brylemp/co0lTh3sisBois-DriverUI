import os,re

ipadd = os.popen('Netsh WLAN show interfaces').read()
x = ipadd.find('Profile                : ') + 25

watt = ipadd[x:].split(' ')[0]
