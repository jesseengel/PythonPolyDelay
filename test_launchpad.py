import OSC
import time, random
import launchpad, polydelay

receive_port = ( '127.0.0.1', 57120 )
send_port = ( '127.0.0.1', 9600 )
errors = 0
count = 0
speed = .1 #seconds

# Sending
client = OSC.OSCClient()
client.connect(send_port) # (host,port)
msg = OSC.OSCMessage()

def sendOSC(port, address, data):
        msg.setAddress(address)
        msg.append(data)
        try:
            client.sendto(msg, port, None)
        except OSCClientError:
            print 'Packet didn\'t make it'
            errors += 1
        msg.clearData()


sendOSC(send_port, "/launchpad", ['clear_all'])

        
color_list = ['Red','Green','Yellow', 'Clear']
    
try:
    while True: 
        data = ['led', random.randint(0,7), random.randint(0,7),
                color_list[random.randint(0,len(color_list)-1)] ]
        sendOSC(send_port, "/launchpad", data)
        time.sleep(speed)
        count += 1

except KeyboardInterrupt:
    print "\nDone!"
    print "Errors:", errors
    print "Count:", count



# Messing around
# sendOSC(send_port, "/launchpad", ['refresh'])
# sendOSC(send_port, "/polydelay", ['status'])
