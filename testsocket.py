import urllib
import urllib2
import string
import json
import websocket
import thread
import time


#// Grab hitbox ip and socket id //////////////////#

site = "http://api.hitbox.tv/chat/servers.json?redis=true"
lines = json.load(urllib2.urlopen(site))#.read()

for line in lines:
    ip = ".".join(line['server_ip'].split(".")[0].split("-")[1:])
    print "usable ip:", ip

site = "http://"+ip+"/socket.io/1/"
lines = urllib2.urlopen(site).read()

socketid = lines.split(":")[0]
print "socket id:", socketid

socketstring = "ws://"+ip+"/socket.io/1/websocket/"+socketid

#// Grab token ///////////////////////////////////#

bot = json.load(open("botvalues.json"))
print "Hitbox username:", bot['name']

values = {'login' : bot['name'],
          'pass' : bot['password'],
          'app' : 'desktop' }

url = 'http://api.hitbox.tv/auth/token'

try:
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = json.load(response)
    token = the_page["authToken"]
    print "authToken:", token
except Exception, e:
    print "Error: Are correct bot credentials in botvalues.json?"
    raise e

#// Hitbox Websocket Code ////////////////////////#

join_msg = ("5:::{\"name\":\"message\",\"args\":[{\"method\":\"joinChannel\",\"params\":{\"channel\":\""
    +bot['channel']+"\",\"name\":\""+bot['name']+"\",\"token\":\"" + token + "\",\"isAdmin\":false}}]}")

def hitbox_send_message(ws, message):
    ws.send("5:::{\"name\":\"message\",\"args\":[{\"method\":\"chatMsg\",\"params\":{\"channel\":\""
        +bot['channel']+"\",\"name\":\""+bot['name']+"\",\"nameColor\":\"FA5858\",\"text\":\""+message+"\"}}]}")

def on_message(ws, message):
    print "message:",message
    if message.startswith("5:::"):
        m = json.loads(message[4:])['args'][0]
        m2 = json.loads(m)
        inmessage = m2['params']['text']
        print inmessage
        if m2['params']['name'] != bot['name']:
            #PLACE BOT FUNCTIONALITY HERE
            hitbox_send_message(ws, "BOT - " + inmessage)
    if message == "2::":
        ws.send("2::")

def on_error(ws, error):
    raise error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "open"
    time.sleep(1)
    ws.send(join_msg)
    time.sleep(1)
    hitbox_send_message(ws, "BOT IS ONLINE")
    # # alternate script, demonstrating a multithreaded approach to ws events.
    # def run(*args):
    #     for i in range(30000):
    #         time.sleep(1)
    #         ws.send("Hello %d" % i)
    #     time.sleep(1)
    #     ws.close()
    #     print "thread terminating..."
    # thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True) #True prints out the handshake, any characters sent, and any errors in debug handling
    ws = websocket.WebSocketApp(socketstring,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()