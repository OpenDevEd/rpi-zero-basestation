# File /etc/ppp/peers/gsm.mm

# Your modem's device path
/dev/ttySC0

# Rate 115200 turned out to be too high
57600

# We don't need -T option here
connect 'chat -v -f /etc/chatscripts/gprs.mm'

# You should remove this option in your production setup if a modem is the only (or primary) interface
nodefaultroute

# Authentication settings
noauth
user "gg"   # Replace with your username, if required
password "p" # Replace with your password, if required

# DNS configuration (to receive DNS server from the provider)
usepeerdns

# OR use pre-defined DNS servers
#ms-dns 8.8.8.8
#ms-dns 8.8.4.4

# Continiously try to restart the connection if it fails (or set a number or retries in 'maxfail' parameter) 
#persist
#maxfail 0

# Important to have a smaller MTU and MRU than 1500 for better connectivity. 
# Depending on your network, 1460 or 1492 can be a good choice.
mtu 1460
mru 1460
