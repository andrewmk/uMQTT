function mtStr(s) {
  return String.fromCharCode(s.length>>8,s.length&255)+s;
}

function mtPacket(cmd, variable, payload) {
  return String.fromCharCode(cmd, variable.length+payload.length)+variable+payload;
}

function mtpConnect(name) {
  return mtPacket(0b00010000, 
           mtStr("MQTT")/*protocol name*/+
           "\x04"/*protocol level*/+
           "\x00"/*connect flag*/+
           "\xFF\xFF"/*Keepalive*/, mtStr(name));
}

function mtpPub(topic, data) {
  return  mtPacket(0b00110001, mtStr(topic), data);
}

var client;
function onConnected() {
  console.log('creating client');
  client = require("net").connect({host : "192.168.1.50", port: 1883}, function() { //'connect' listener
    console.log('client connected');
    client.write(mtpConnect("Espruino"));
    
    var intr = setInterval(function() {
      console.log("Publishing");
      client.write(mtpPub("a/b", E.getTemperature().toFixed(4)));
    }, 2000);
    
    client.on('data', function(data) {
      console.log("[MQTT]"+data.split("").map(function(c) { return c.charCodeAt(0); }));
    });
    client.on('end', function() {
      console.log('client disconnected');
      clearInterval(intr);
    });
  });
}

// For CC3000 WiFi
var wlan = require("CC3000").connect();
wlan.connect( "BTHub4-5ZN2", "2f3b5659ad", function (s) { 
  if (s=="dhcp") {
    console.log("My IP is "+wlan.getIP().ip);
    onConnected();
  }
});
