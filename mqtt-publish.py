def mtStr(s):
  return bytes([len(s) >> 8, len(s) & 255]) + s.encode('utf-8')

def mtPacket(cmd, variable, payload):
  return bytes([cmd, len(variable) + len(payload)]) + variable + payload

def mtpConnect(name):
  return mtPacket(
           0b00010000,
           mtStr("MQTT") + # protocol name
           b'\x04' +       # protocol level
           b'\x00' +       # connect flag
           b'\xFF\xFF',    # keepalive
           mtStr(name)
  )

def mtpDisconnect():
  return bytes([0b11100000, 0b00000000])

def mtpPub(topic, data):
  return  mtPacket(0b00110001, mtStr(topic), data)

import socket
import binascii
import time

addr = socket.getaddrinfo("test.mosquitto.org", 1883)[0][4]
s = socket.socket()

print('Connecting...')
s.connect(addr)
s.send(mtpConnect("WiPy1"))
print(binascii.hexlify(s.recv(4096)))

print("Publishing...")

time.sleep(10)

s.send(mtpPub("wipytopic", b'wipy-data'))

time.sleep(10)

s.send(mtpPub("wipytopic", b'wipy-data-again'))
##print(binascii.hexlify(s.recv(4096)))

print('Disconnecting...')
s.send(mtpDisconnect())
s.close()
