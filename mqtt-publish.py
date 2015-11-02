def mtStr(s):
  return bytes([len(s) >> 8, len(s) & 255]) + s.encode('utf-8')

def mtPacket(cmd, variable, payload):
  return bytes([cmd, len(variable) + len(payload)]) + variable + payload

def mtpConnect(name):
  return mtPacket(
           0b00010000,
           mtStr("MQTT")  /*protocol name*/+
           b'\x04'        /*protocol level*/+
           b'\x00'        /*connect flag*/+
           b'\xFF\xFF'    /*Keepalive*/
           , mtStr(name)
  )

def mtpPub(topic, data):
  return  mtPacket(0b00110001, mtStr(topic), data)

# For CC3000 WiFi
var wlan = require("CC3000").connect()
wlan.connect( "BTHub4-5ZN2", "2f3b5659ad")
if s=="dhcp":
  print("My IP is "+wlan.getIP().ip)

var client
print('creating client')
client = require("net").connect({host : "192.168.1.50", port: 1883})

print('client connecting')
client.write(mtpConnect("Espruino"))

print("Publishing")
client.write(mtpPub(b'topic/subtopic', b'my-data'))

#client.on('data',
#  print("[MQTT]"+ubinascii.hexlify(data))
#)
#
#client.on('end', 
#  print('client disconnected')
#  clearInterval(intr)
#)
