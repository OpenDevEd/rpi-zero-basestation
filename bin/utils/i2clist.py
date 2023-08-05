
#!/usr/bin/env python
# # https://forums.raspberrypi.com/viewtopic.php?t=79860
# import pigpio

# pigpio.exceptions = False # handle errors

# pi = pigpio.pi()

# for bus in range(2):
#    for x in range(0x08, 0x79):
#       h = pi.i2c_open(bus, x)
#       if h >= 0:
#          s = pi.i2c_read_byte(h)
#          if s >= 0:
#             print("device {} found on bus {}".format(x, bus))
#          pi.i2c_close(h)

# pi.stop()

# https://stackoverflow.com/questions/48797011/how-to-extract-i2c-address-from-i2cdetect-console-output
import json
import os
import re
import subprocess

def get_addresses(i2cdetect_output):
    ''' Takes output from i2cdetect and extracts the addresses
        for the entries.
    '''

    # import json file
    with open(os.path.dirname(__file__)+'/i2clist.json', 'r') as f:
        devices = json.load(f)

    # Get the rows, minus the first one
    i2cdetect_rows = i2cdetect_output.split('\\n')[1:]
    #print(len(i2cdetect_rows))
    i2cdetect_matrix = []

    # Add the rows to the matrix without the numbers and colon at the beginning
    for row in i2cdetect_rows:
        i2cdetect_matrix.append(re.split(' +', row)[1:])

    # Add spaces to the first and last rows to make regularly shaped matrix
    i2cdetect_matrix[0] = ['  ', '  ', '  ','  ', '  ', '  ', '  ', '  '] + i2cdetect_matrix[0]
    i2cdetect_matrix[7] = i2cdetect_matrix[7][:-1] + ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']

    # Make a list of the addresses present
    address_list = {}
    for i in range(len(i2cdetect_matrix)):
        #print(i2cdetect_matrix[i])
        for j in range(len(i2cdetect_matrix[i])-1):
            addr = ''.join('{:02X}'.format(i*16+j) )
            if i2cdetect_matrix[i][j] not in ('  ', '--'):
                address_list[addr] = { "detected": True }
                if devices.get(addr):
                   address_list[addr]["device"] = devices[addr]
            if i2cdetect_matrix[i][j] == 'UU':
                address_list[addr]["UU"] = True

    return address_list

# Get output from i2cdetect
# get output from system command

result = subprocess.run(['i2cdetect', '-y', '1'], stdout=subprocess.PIPE)
#print(str(result.stdout))
list = get_addresses(str(result.stdout))
print( json.dumps(list, indent=2) )
