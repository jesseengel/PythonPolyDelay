### to_max to Launchpad ###
# LED addressing is like a matlab matrix inverted (column, row)[-1:7][0:8]
# Starting in the upperleft hand corner
# The grid is [0:7][0:7]

import OSC

class launchpad:
        def __init__(self, send_port, receive_port):
                self.client = OSC.OSCClient()
                self.msg = OSC.OSCMessage()
                self.send_port = send_port
                self.receive_port = receive_port
                
                self.color_dict = {'Red': [0,3], 'Green': [3,0], 'Yellow': [3,3], 'Clear': [0,0]}
                self.octave_dict = {-1: 'Red', 0:'Green', 1:'Yellow'}
                self.mode = 'polydelay'


        def sendOSC(self, port, address, data):
                self.msg.setAddress(address)
                self.msg.append(data)
                try:
                        self.client.sendto(self.msg, port, None)
                except OSC.OSCClientError:
                        print 'Packet didn\'t make it'
                self.msg.clearData()



        # def led_array(self, led_list):
        #         # led_list [[x,y,color], [x,y,color]]
        #         # Check if led_list is 2-dimensional
        #         if type(led_list[0]) is list:
        #                 for i in range(len(led_list)):
        #                         self.sendOSC(self.send_port, '/launchpad/wac.lp/0/1/led',
        #                                      led_list[i][0:2] + self.color_dict[led_list[i][2]])
        #         else:
        #                 self.sendOSC(self.send_port, '/launchpad/wac.lp/0/1/led',
        #                                      led_list[0:2] + self.color_dict[led_list[2]])
                                
                
        def led(self, x,y,color):
                self.sendOSC(self.send_port, '/launchpad/wac.lp/0/1/led', [x,y] + self.color_dict[color])

        def column(self, x, height, color):
                for iy in range(8):
                        # bottom to top
                        h = 8-iy
                        if h <= height:
                                self.led(x, iy, color)
                        else:
                                self.led(x, iy, 'Clear')

        def clear_column(self, x):
                # just clears
                self.column(x, 8, 'Clear')

        def clear_all(self):
                for ix in range(9):
                        for iy in range(8):
                                self.led(ix, iy, 'Clear')	

        def clear_page(self):
                for ix in range(8):
                        for iy in range(8):
                                self.led(ix, iy, 'Clear')


        # # Transport buttons
        # def tap_in(self, val):
        #         if val:
        #                 self.led(8,8-sidebar.tap_tempo,'Green')
        #         else:
        #                 self.led(8,8-sidebar.tap_tempo,'Clear')

        # def tap_out(self):
        #         self.sendOSC(self.send_port, '/launchpad', ['tap','bang'])


        # Pass launchpad a polydelay object to let it know you're refreshing a polydelay
        def refresh(self, polydelay):
                tmp = []

                if self.mode is 'polydelay':
                        for i in range(polydelay.voices):
                        # turn on the columns that are on	
                                if polydelay.input_volume[i] > 0.0:
                                        self.column(polydelay.time[i], polydelay.pitch[i],
                                                    self.octave_dict[polydelay.octave[i]])
                                        tmp.append(polydelay.time[i])
                        # turn off the columns that are off and not on in another delay line		
                                elif not any(polydelay.time[i]==itmp for itmp in tmp):
                                        self.clear_column(polydelay.time[i])
                        # clear the rest of them
                        for icolumn in range(8):
                                if not any(icolumn==itime for itime in polydelay.time):
                                        self.clear_column(icolumn)

                ###Octave Buttons####
                # self.led(8,8-sidebar.octave_up,'Yellow')
                # self.led(8,8-sidebar.octave_down,'Red')

                






        # class slider:
        #         """A class to control slider info/behavior
        #         Mostly for feedback and wet to begin"""
        #         def __init__(self, parameter_name, column_number, top, color):
        #                 self.column = column_number #base 0
        #                 self.height = 5 #base 1
        #                 self.top = top
        #                 self.parameter = parameter_name
        #                 self.color = color

        #         def refresh(self):
        #                 self.column(self.column, self.height, self.color)

        #         def set(self, y):
        #                 self.height = y
        #                 self.sendOSC('/max',  [self.parameter, (self.height-1) / 7.0 * self.top])
        #                 self.refresh()

        # class button:
        #         """A class to control button info/behavior
        #         Mostly for dry"""
        #         def __init__(self, parameter, behavior, x, y, color):
        #                 self.x = x 
        #                 self.y = y 
        #                 self.parameter = parameter
        #                 self.color = color
        #                 self.behavior = behavior #toggle or sustain
        #                 self.onoff = 1

        #         def refresh(self):
        #                 if self.onoff: 
        #                         launchpad.led(self.x, 8-self.y, self.color)
        #                 else:
        #                         launchpad.led(self.x, 8-self.y, 'Clear')

        #         def push(self, push):
        #                 if self.behavior is 'sustain':
        #                         self.onoff = push
        #                 elif self.behavior is 'toggle' and push:
        #                         self.onoff = (self.onoff + 1) % 2
        #                 self.sendOSC('/max/launchpad/', [self.parameter, self.onoff])
        #                 self.refresh()

        # #Column 8 (Sidebar) Functions
        # class sidebar:
        #         def __init__(self):
        #                 self.octave_up = 2
        #                 self.octave_down = 1
        #                 self.tap_tempo = 8
        #                 self.keyboard = 6
        #                 self.sliders = 7

                        
            ### Behavior Functions / From Launchpad ###



    # def press(polydelay, *A):
    #         # Python's varargs are implemented as tuples, not lists. (list(A))
    #         xtime, ypitch, push = list(A)
    #         #map 0:7 onto 8:1
    #         ypitch = 8-ypitch
    #         # print "x:", x, "y:", y, "push:", push

    #         if xtime < 8:

    #                 if polydelay.slider_menu:
    #                         if xtime == wet.column:
    #                                 wet.set(ypitch)
    #                         elif xtime == feedback.column:
    #                                 feedback.set(ypitch)
    #                         elif xtime == dry.x and ypitch == dry.y:
    #                                 dry.push(push)

    #                 elif polydelay.keyboard_menu:
    #                         print 'insert keyboard functions here'
    #                 else:

    #                         if push:
    #                                 foundit = 0

    #                                 for i, ionoff in enumerate(polydelay.onoffs): 

    #                                         #find active lines with same delay time and pitch and turn them off
    #                                         if ionoff and polydelay.times[i]==xtime:			

    #                                                 if polydelay.pitches[i]==ypitch and polydelay.octave_cue==0:
    #                                                         focus(i)
    #                                                         onoff(0)
    #                                                         to_max('onoff', polydelay.focus, 0)
    #                                                         polydelay.octaves[i]=0
    #                                                         to_max('octave', polydelay.focus, 0)
    #                                                         foundit = 1
    #                                                 #or just set the pitch
    #                                                 else:
    #                                                         focus(i)
    #                                                         pitch(ypitch)
    #                                                         to_max('pitch', polydelay.focus, ypitch)
    #                                                         if polydelay.octave_cue != 0:
    #                                                                 octave(polydelay.octave_cue)
    #                                                         foundit = 1


    #                                 #if none found, turn on a new line
    #                                 if not foundit:

    #                                         #if there's an open delay line, use it
    #                                         if polydelay.onoffs.count(0) > 0:	
    #                                                 focus(polydelay.onoffs.index(0))
    #                                                 onoff(1)
    #                                                 to_max('onoff', polydelay.focus, 1)
    #                                         #otherwise use the closest line
    #                                         else:
    #                                                 focus( min(range(len(polydelay.times)), key=lambda index: abs(polydelay.times[index]-xtime)) )

    #                                         #In both cases, set the time and pitch
    #                                         time(xtime)
    #                                         to_max('time', polydelay.focus, xtime)
    #                                         pitch(ypitch)
    #                                         to_max('pitch', polydelay.focus, ypitch)
    #                                         if polydelay.octave_cue != 0:
    #                                                 octave(polydelay.octave_cue)

    #                                 #always refresh the page after a push
    #                                 refresh_page()


    #             #Sidebar Functions 
    #             elif xtime == 8:

    #                     # For bringing octaves up	
    #                     if ypitch == sidebar.octave_up:
    #                             if push:
    #                                     polydelay.octave_cue = 1
    #                             else:
    #                                     polydelay.octave_cue = 0

    #                     #For bringing octaves down	
    #                     if ypitch == sidebar.octave_down:
    #                             if push:
    #                                     polydelay.octave_cue = -1
    #                             else:
    #                                     polydelay.octave_cue = 0

    #                     #For tap tempo	
    #                     if ypitch == sidebar.tap_tempo:
    #                             if push:
    #                                     tap_out()
    #                                     launchpad.led(8,8-sidebar.tap_tempo,'Green')
    #                             else:
    #                                     launchpad.led(8,8-sidebar.tap_tempo,'Clear')

    #                     #For Sliders
    #                     if ypitch == sidebar.sliders:
    #                             if push:
    #                                     polydelay.slider_menu = 1
    #                                     launchpad.clear_page()
    #                                     wet.refresh()
    #                                     feedback.refresh()
    #                                     dry.refresh()
    #                                     launchpad.led(8,8-sidebar.sliders,'Green')
    #                             else:
    #                                     polydelay.slider_menu = 0
    #                                     refresh_page()
    #                                     launchpad.led(8,8-sidebar.sliders,'Clear')

    #                     #For Keyboard
    #                     if ypitch == sidebar.keyboard:
    #                             if push:
    #                                     polydelay.keyboard_menu = 1
    #                                     launchpad.led(8,8-sidebar.keyboard,'Yellow')
    #                             else:
    #                                     polydelay.keyboard_menu = 0
    #                                     launchpad.led(8,8-sidebar.keyboard,'Clear')

                                                # ### Define my Objects ###
        # sidebar = sidebar()
        # wet = slider('wet', 0, 100, 'Yellow')
        # feedback = slider('feedback', 1, 100, 'Red')
        # dry = button('dry', 'toggle', 2, 1, 'Green')
