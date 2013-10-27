import OSC
import time, random
import launchpad, polydelay

receive_port = ( '127.0.0.1', 57120 )
send_port = ( '127.0.0.1', 9600 )


# Sending
client = OSC.OSCClient()
client.connect(send_port) # (host,port)
msg = OSC.OSCMessage()

poly = polydelay.polydelay(send_port, receive_port)
launch = launchpad.launchpad(send_port, receive_port)


def sendOSC(port, address, data):
        msg.setAddress(address)
        msg.append(data)
        try:
            client.sendto(msg, port, None)
        except OSCClientError:
            print 'Packet didn\'t make it'
            errors += 1
        msg.clearData()


# poly.pitch = [0, 1, 2, 3]
launch.refresh(poly)
