import OSC, polydelay
import cPickle as pickle

receive_port = ( '127.0.0.1', 9600 )
send_port = ( '127.0.0.1', 57120 )


p = polydelay.polydelay(send_port, receive_port)

p.input_volume = [1.0, 1.0, 1.0, 1.0] 
p.output_volume = [1.0, 0.0, 0.0, 0.0] 
p.pan = [0.5, 0.5, 0.5, 0.5] 
p.feedback = [0.99, 0.99, 0.99, 0.99] 
p.pitch = [1, 1, 1, 1] 
p.octave = [0, 0, 0, 0] 
p.time = [2, 2, 2, 2] 
p.unit = ['16n', '16n', '16n', '16n']

p.save_preset([1])


p.input_volume = [1.0, 1.0, 1.0, 1.0] 
p.output_volume = [1.0, 1.0, 1.0, 1.0] 
p.pan = [0.5, 0.5, 0.5, 0.5] 
p.feedback = [0.99, 0.99, 0.99, 0.99] 
p.pitch = [1, 1, 1, 1] 
p.octave = [1, -1, 1, -1] 
p.time = [2, 4, 6, 7] 
p.unit = ['16n', '16n', '16n', '16n']

p.save_preset([2])


p.input_volume = [1.0, 1.0, 1.0, 1.0] 
p.output_volume = [1.0, 1.0, 0.0, 0.0] 
p.pan = [0.5, 0.5, 0.5, 0.5] 
p.feedback = [0.99, 0.99, 0.99, 0.99] 
p.pitch = [3, 5, 1, 1] 
p.octave = [0, -1, 0, 0] 
p.time = [2, 5, 0, 0] 
p.unit = ['16n', '16n', '16n', '16n']

p.save_preset([3])


p.input_volume = [1.0, 1.0, 1.0, 1.0] 
p.output_volume = [1.0, 1.0, 1.0, 1.0] 
p.pan = [0.0, 0.3, 0.6, 1.0] 
p.feedback = [0.99, 0.99, 0.99, 0.99] 
p.pitch = [3, 2, 5, 4] 
p.octave = [0, 0, 0, 0] 
p.time = [5, 12, 16, 7] 
p.unit = ['16n', '16n', '16n', '16n']

p.save_preset([4])
