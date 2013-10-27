import cPickle 
import polydelay

poly = polydelay.polydelay('send','receive')

poly.time = [0,1,2,3]

def save_preset(preset_number, file_prefix, save_object):
    filename = file_prefix + '%r.cpickle' % preset_number
    f = open(filename, 'wb')
    cPickle.dump(save_object, f, protocol=2)
    f.close()

def load_preset(preset_number, file_prefix):
    filename = file_prefix + '%r.cpickle' % preset_number
    f = open(filename, 'rb')
    p = cPickle.load(f)
    f.close()
    return(p)

# save_preset(1)
# poly_copy = load_preset(1)






import pickle

data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

output = open('data.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(data1, output)

# Pickle the list using the highest protocol available.
pickle.dump(selfref_list, output, -1)

output.close()


####

import pprint, pickle

pkl_file = open('data.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()
