In our setup, we use a Designer Systems phat-gsm module.

It is important to adjust the baud rate, because the device works over I2C, and the device gets stuck when it received "too much" data from TLS connections. The device
could handle smaller ping requests without an adjustment of the baud rate.

In this folder, there are

1. A fragment of /boot/config.txt file. This is as recommended by the vendor.

2. A simplified version of a chat script: `/etc/chatscripts/gprs.mm`. This file has an ATZ command to reset the modem to the default state before a connection attempt. It is a widely recommended practice, but the modem vendor may view it differently.

3. A `/etc/ppp/peers/gsm.mm` with some changes compared to similar files we found online. We've used a baud rate of 57600 and different MTU / MRU values to optimize the performance. The modem itself works in the auto-baud mode by default (can be checked by AT+IPR? command, which should return zero). This means that we don't need to configure the modem itself (compared to what the vendor proposed), but we can only instruct pppd to use the reduced baud rate. There are also some useful pppd options for your consideration, along with comments.

You can try that everything works smoothly with the following commands:
```
pon gsm.mm
ping -I ppp0 -n google.com
curl -v -4 --interface ppp0 https://google.com
poff gsm.mm
```

It's helpful to explicitly use IPv4 for testing because IPv6 connections require more header data to be transferred.

As a side note, as we were trying to get the modem working, we tried this with kernel 5.4 (as opposed to the default kernel 6.x), but this had no impact on anything.

Note that for debugging, packaged like `socat`, `lsof`, `tcpdump`, and `telnet` are useful packages for debugging, but not needed for running the device.

To what extent are these instructions helpful to your use case?

1. Changing a mobile network provider may require a chat script update (dial-in number, username, password, APN). Ideally one would make it with a configuration template, which you can apply for any new device or provider you use. It can be done with Ansible or simple bash scripting.

2. Changing a modem to a different vendor may also require a chat script update (some extra AT commands in addition to ATZ, for example) and device path correction (instead of /dev/ttySC0). This is easy if you have documentation from the vendor. However the chat script proposed above (`gprs.mm`) is fail-safe and generic and should work in most of cases.

3. Using another Raspberry Board should work as well, but it should be checked against every specific model. For example, during our research we found that some RPi 3 boards may not work with I2C speed negotiation properly. (https://forums.raspberrypi.com//viewtopic.php?f=29&t=219675) or some older Raspbian kernels caused errors with I2C modems (which we tested and didn't confirm for our current device, a RPi Zero W).

4. Also the connection speed via PPP may be impacted by different factors, even if set properly. Here is a good article on the topic with some conclusions that you may consider in future: https://unix.stackexchange.com/questions/442668/how-do-i-make-ppp-reliable-over-lossy-radio-modems-using-pppd-and-tcp-kernel-set.

On a side note, we are building various fail safes into our setup, including a watchdog, RPi monitoring and some emergency recovery or reboot tooling.