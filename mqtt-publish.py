def mtStr(s):
  return str.fromCharCode(s.length>>8,s.length&255)+s

def mtPacket(cmd, variable, payload):
  return str.fromCharCode(cmd, variable.length+payload.length)+variable+payload

def mtpConnect(name):
  return mtPacket(0b00010000,
           mtStr("MQTT")/*protocol name*/+
           "\x04"/*protocol level*/+
           "\x00"/*connect flag*/+
           "\xFF\xFF"/*Keepalive*/, mtStr(name))

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

print('client connected')
client.write(mtpConnect("Espruino"))

intr = setInterval(
  print("Publishing")
  client.write(mtpPub("a/b", E.getTemperature().toFixed(4)))
, 2000)

client.on('data',
  print("[MQTT]"+ubinascii.hexlify(data))
)

client.on('end', 
  print('client disconnected')
  clearInterval(intr)
)
