# Poly Variable list:
# ###--------------------###
# pitch: (1:8), not the pitch shift, the note relative to root=1
# octave: (-2:2)
# time: (0:8), simultaneous=0
# unit: (1n 2n 4n 8n 16n 32n)[t,d]
# input_volume: (0.0:1.0)
# output_volume: (0.0:1.0)
# feedback: (0.0:0.9) 1 would be forever
# pan: (0:0.5:1.0) left = 0.0, center = 0.5, right = 1.0
#
# Pattr Variable list:
# ###--------------------###
# global_feedback(0:1)
# 

import OSC, launchpad
import cPickle as pickle


class polydelay:
    """A class to take in played midi notes and calculate out
    transposition values for polydelay"""
    def __init__(self, send_port, receive_port):
        self.client = OSC.OSCClient()
        self.msg = OSC.OSCMessage()
        self.send_port = send_port
        self.receive_port = receive_port
        self.voices = 4
        
        self.input_volume = [1.0] * self.voices
        self.output_volume = [0.0] * self.voices
        self.pan = [0.5] * self.voices
        self.feedback = [0.0] * self.voices
        self.pitch = [1] * self.voices
        self.octave = [0] * self.voices
        self.time = [0] * self.voices
        self.unit = ['8n'] * self.voices
        self.note = 0
        self.transpose = [0] * self.voices
        self.root_note = 0
        self.root_key = 'C'
        self._attr_list = ['input_volume', 'output_volume', 'pan', 'feedback', 
                              'pitch', 'octave','time', 'unit']
        self._root_dict = {'C': 0, 'C#': 1, 'D': 2, 'D#':3, 
                          'E': 4, 'F': 5, 'F': 6, 'G': 7, 
                          'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        self.transpose_lookup=[] #Create transpose_lookup[note][pitch_list]
        self._transpose_lookup_init()
        

    def _transpose_lookup_init(self):
        base = [0,2,4,5,7,9,11,12]
        modes = {'ionian':[0,0,0,0,0,0,0,0],
                      'dorian':[0,0,-1,0,0,0,-1,0],
                      'phrygian':[0,-1,-1,0,0,-1,-1,0],
                      'lydian':[0,0,0,+1,0,0,0,0],
                      'mixolydian':[0,0,0,0,0,0,-1,0],
                      'aeolian':[0,0,-1,0,0,-1,-1,0],
                      'locrian':[0,-1,-1,0,-1,-1,-1,0]}
        mode_lookup = ['ionian','dorian','dorian','phrygian',
                'phrygian','lydian','mixolydian','mixolydian',
                'aeolian','aeolian','locrian','locrian']
        out_of_key = [0,1,0,1,0,0,1,0,1,0,1,0]
        for i in range(12):
            self.transpose_lookup.append(map(lambda x,y,z: x+y+z, 
                                        base, modes[mode_lookup[i]],
                                        (ones*out_of_key[i] for ones in [1]*8)))

    def sendOSC(self, port, address, data):
        self.msg.setAddress(address)
        self.msg.append(data)
        try:
            self.client.sendto(self.msg, port, None)
        except OSC.OSCClientError:
            print 'Packet didn\'t make it'
        self.msg.clearData()


    def polydelay_refresh(self):
        for attr in self._attr_list:
            for i in range(self.voices):
                self.sendOSC(self.send_port, '/polydelay/poly', ['target', i+1])
                self.sendOSC(self.send_port, '/polydelay/poly', [attr, getattr(self, attr)[i]] )
             

    def launchpad_refresh(self):
        self.sendOSC(self.receive_port, '/launchpad', ['refresh'])


    def calc_transpose(self):
         for i,ipitch in enumerate(self.pitch):
            self.transpose[i] = self.transpose_lookup[self.note][ipitch-1] \
                                + self.octave[i]*12
            self.sendOSC(self.send_port, '/polydelay/poly', ['target', i+1])
            self.sendOSC(self.send_port, '/polydelay/poly', ['transpose', self.transpose[i]])

        
                
    # Setters calculate transpose too
    # input message example "(\polydelay set time 1 0 3 4)"
    def set(self, data):
        attribute = data.pop(0)

        if attribute == ('input_volume' or 'output_volume' or 'pan' or 'feedback' \
           or 'time' or 'unit'):
            setattr(self, attribute, data)
            self.polydelay_refresh()
            self.launchpad_refresh()
        elif attribute == ('pitch' or 'octave'):
            setattr(self, attribute, data)
            self.polydelay_refresh()
            self.launchpad_refresh()
            self.calc_transpose()
        elif attribute == 'note':
             if type(data) is list:
                data = data[0]
             self.note = (data - self.root_note) % 12
             self.calc_transpose()
        elif attribute == 'root_key':
            if type(data) is list:
                data = data[0]
            self.root_key = data
            self.root_note = self._root_dict[data]
        elif attribute == 'root_note':
            if type(data) is list:
                data = data[0]
            self.root_note = data % 12

            


    def save_preset(self, preset_number):
        tmp = []
        
        for attr in self._attr_list:
            tmp.append( getattr(self, attr))
        print tmp
                  
        filename ='polydelay_preset%r.pkl' % preset_number
        output = open(filename, 'wb')
        pickle.dump(tmp, output)
        output.close()

        self.launchpad_refresh()
        self.polydelay_refresh()

    def load_preset(self, preset_number):
        tmp = []
                         
        try:
            filename ='polydelay_preset%r.pkl' % preset_number
            pkl_file = open(filename, 'rb')
            tmp = pickle.load(pkl_file)
            pkl_file.close()

            print tmp
            for iattr, attr in enumerate(self._attr_list):
                setattr(self, attr, tmp[iattr])

            self.launchpad_refresh()
            self.polydelay_refresh()

        except (IOError, IndexError):
            print 'Preset file %s does not exist' % filename
            pass


 

        
    def status(self, hack):
        print "---"
        print "input_volume: %s" % self.input_volume
        print "output_volume: %s" % self.output_volume
        print "pan: %s" % self.pan
        print "feedback: %s" % self.feedback
        print "time: %s" % self.time
        print "unit: %s" % self.unit
        print "pitch: %s" % self.pitch
        print "octave: %s" % self.octave
        print "note: %s" % self.note
        print "root_note: %s" % self.root_note
        print "transpose: %s" % self.transpose
        # print "transpose_lookup:"
        # print self.transpose_lookup
        print "---"
