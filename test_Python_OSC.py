def test():
    print 'woot'
    import OSC
    import time, threading

    receive_address = ( '127.0.0.1', 57120 )
    send_address = ( '127.0.0.1', 9600 )

    # Sending
    s = OSC.OSCClient()
    s.connect(send_address) # (host,port)

    msg = OSC.OSCMessage()
    msg.setAddress("/polydelay")

    def send(data):
        msg.append(data)
        s.send(msg)
        msg.clearData()
    
    data = ['pitch', 0, 1, 2, 3]
    send(data)

    data = ['octave', 0, 1, -1, 0]
    send(data)

    data = ['root_note', 5]
    send(data)

    data = ['note', 2]
    send(data)

    data = ['status']
    send(data)









if __name__ == "__main__":
    test()
