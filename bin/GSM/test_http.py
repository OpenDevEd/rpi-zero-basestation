import serial
import time

ser = serial.Serial("/dev/ttySC0", 115200, timeout=1)
ser.flush()


def check_gprs_enabled():
    response = send_at_command("AT+CGATT?")
    if "+CGATT: 1" in response:
        print("GPRS is enabled")
    elif "+CGATT: 0" in response:
        print("GPRS is disabled")
    else:
        print("Failed to check GPRS status")


def connect_to_apn_2(apn_name):
    # Set the APN
    send_at_command('AT+CGDCONT=1,"IP","{}"'.format(apn_name))

    # Attach to the GPRS network
    send_at_command("AT+CGATT=1")

    # Start the wireless connection
    send_at_command('AT+CSTT="{}"'.format(apn_name))
    send_at_command("AT+CIICR")

    # Check if the connection was successful
    response = send_at_command("AT+CIFSR")
    if "ERROR" in response:
        print("Failed to connect to APN")
    else:
        print("Connected to APN with IP address:", response.strip())


def connect_to_apn(apn_name, apn_username, apn_password):
    # Set the APN
    send_at_command('AT+CGDCONT=1,"IP","{}"'.format(apn_name))

    # Attach to the GPRS network
    send_at_command("AT+CGATT=1")

    # Start the wireless connection
    send_at_command(
        'AT+CSTT="{}","{}","{}"'.format(apn_name, apn_username, apn_password)
    )
    send_at_command("AT+CIICR")

    # Check if the connection was successful
    response = send_at_command("AT+CIFSR")
    if "ERROR" in response:
        print("Failed to connect to APN")
    else:
        print("Connected to APN with IP address:", response.strip())


def send_at_command(command, delay=1):
    ser.write((command + "\r\n").encode("utf-8"))
    time.sleep(delay)
    response = ""
    while ser.in_waiting > 0:
        line = ser.readline().decode("utf-8").strip()
        print(line)
        response += line + "\n"
    return response


# Set APN and connect to the internet
# send_at_command('AT+CGDCONT=1,"IP","giffgaff.com"')
# send_at_command('AT+CSTT="giffgaff.com","gg","p"')
# send_at_command('AT+CGAUTH=1,1,"gg","p"')
# send_at_command("AT+CGACT=1,1")
ip_address = send_at_command("AT+CIFSR")
print("Assigned IP:", ip_address)


def check_signal_strength():
    response = send_at_command("AT+CSQ")
    signal_strength = response.split(": ")[1].split(",")[0]
    return int(signal_strength)


def check_network_registration():
    response = send_at_command("AT+CREG?")
    registration_status = response.split(",")[1]
    return registration_status == "1"


def send_https_get_request(url):
    # Initialize HTTP service
    send_at_command("AT+HTTPTERM")
    send_at_command("AT+HTTPINIT")

    # Set HTTP parameters
    send_at_command('AT+HTTPPARA="CID",1')
    send_at_command('AT+HTTPPARA="URL","{}"'.format(url))

    # Set HTTPS parameters
    send_at_command("AT+HTTPSSL=1")

    # Send HTTP GET request
    send_at_command("AT+HTTPACTION=0")

    # Read HTTP response
    response = send_at_command("AT+HTTPREAD")
    print("HTTP Response:")
    print(response)

    # Terminate HTTP service
    send_at_command("AT+HTTPTERM")


def send_http_get_request(url):
    # Initialize HTTP service
    send_at_command("AT+HTTPTERM")
    send_at_command("AT+HTTPINIT")

    # Set HTTP parameters
    send_at_command('AT+HTTPPARA="CID",1')
    send_at_command('AT+HTTPPARA="URL","{}"'.format(url))

    # Send HTTP GET request
    send_at_command("AT+HTTPACTION=0")

    # Read HTTP response
    response = send_at_command("AT+HTTPREAD")
    print("HTTP Response:")
    print(response)

    # Terminate HTTP service
    send_at_command("AT+HTTPTERM")


def connect_to_apn_using_sapbr(apn_name):
    # Set the APN for bearer profile 1
    send_at_command('AT+SAPBR=3,1,"APN","{}"'.format(apn_name))

    # Open the GPRS context for bearer profile 1
    send_at_command("AT+SAPBR=1,1")

    # Check if the connection was successful
    response = send_at_command("AT+SAPBR=2,1")
    if "+SAPBR: 1,1," in response:
        print("Connected to APN using SAPBR")
    else:
        print("Failed to connect to APN using SAPBR")


connect_to_apn_using_sapbr("giffgaff.com")
print("Signal strength:", check_signal_strength())
print("Network registered:", check_network_registration())

send_http_get_request("www.google.com")

ser.close()
