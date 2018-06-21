#!/usr/bin/python3

# Zur Überprüfung, welche Daten der Arduino Code an Python schickt.

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.123', 123)) ## IP Adresse: 192.168.43.123 Name: Xperia X_e8b2


data = s.recv(24) # erhalte Daten
print(data.decode()) # printe diese erhaltenen Daten kodiert (ohne b'')
data = s.recv(24)
print(data.decode())
data = s.recv(24)
print(data.decode())
data = s.recv(24)
print(data.decode())
data = s.recv(24)
print(data.decode()) 
data = s.recv(24)
print(data.decode())
data = s.recv(24)
print(data.decode())
