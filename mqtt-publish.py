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


var client
def onConnected():
  print('creating client')
  client = require("net").connect({host : "192.168.1.50", port: 1883}, def() { //'connect' listener
    print('client connected')
    client.write(mtpConnect("Espruino"))

    var intr = setInterval(def():
      print("Publishing")
      client.write(mtpPub("a/b", E.getTemperature().toFixed(4)))
    , 2000)

    client.on('data', def(data):
      print("[MQTT]"+data.split("").map(def(c) { return c.charCodeAt(0); }))
    })
    client.on('end', def():
      print('client disconnected')
      clearInterval(intr)
    )
  )
}

# For CC3000 WiFi
var wlan = require("CC3000").connect()
wlan.connect( "BTHub4-5ZN2", "2f3b5659ad", def (s) {
  if s=="dhcp":
    print("My IP is "+wlan.getIP().ip)
    onConnected()

})
