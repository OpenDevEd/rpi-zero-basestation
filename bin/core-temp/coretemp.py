import json
import os
import re
import subprocess

entry = {}

gputemp = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
print(gputemp.stdout)
# get digits from gputemp
digits = re.findall(r'[\d\.]+', gputemp.stdout.decode('utf-8'))
print(digits[0])
entry["gpu"] = float(digits[0])

cputemp = subprocess.run(['cat', '/sys/class/thermal/thermal_zone0/temp'], stdout=subprocess.PIPE)
print(cputemp.stdout)
digits = re.findall(r'[\d\.]+', cputemp.stdout.decode('utf-8'))
print(int(digits[0])/1000)
entry["cpu"] = int(digits[0])/1000


# convert entry to json
with open('entry.json', 'w') as outfile:
    json.dump(entry, outfile)
