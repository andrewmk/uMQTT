def mtStr(s):
  return bytes([len(s) >> 8, len(s) & 255]) + s.encode('utf-8')

def mtPacket(cmd, variable, payload):
  return bytes([cmd, len(variable) + len(payload)]) + variable + payload

def mtpConnect(name):
  return mtPacket(
           0b00010000,
           mtStr("MQTT")  /*protocol name*/ +
           b'\x04'        /*protocol level*/ +
           b'\x00'        /*connect flag*/ +
           b'\xFF\xFF',   /*Keepalive*/
           mtStr(name)
  )

def mtpDisconnect():
  return bytes([0b11100000, 0b00000000])

def mtpPub(topic, data):
  return  mtPacket(0b00110001, mtStr(topic), data)

import socket
addr = socket.getaddrinfo("mqttbroker.com", 1883)[0][4]
s = socket.socket()

print('Connecting...')
s.connect(addr)
s.send(mtpConnect("WiPy1"))

print("Publishing...")
s.send(mtpPub("topic/subtopic", b'my-data'))

print('Disconnecting...')
s.send(mtpDisconnect())
s.close()

#client.on('data',
#  print("[MQTT]"+ubinascii.hexlify(data))
#)
#
#client.on('end', 
#  print('client disconnected')
#  clearInterval(intr)
#)
