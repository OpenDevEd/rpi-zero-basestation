# https://www.zigbee2mqtt.io/guide/installation/01_linux.html#determine-location-of-the-adapter-and-checking-user-permissions
# Verify that the correct nodejs and npm (automatically installed with nodejs)
# version has been installed
node --version  # Should output v14.X, V16.x, V17.x or V18.X
npm --version  # Should output 6.X, 7.X or 8.X

# Create a directory for zigbee2mqtt and set your user as owner of it
sudo mkdir /opt/zigbee2mqtt
sudo chown -R ${USER}: /opt/zigbee2mqtt

# Clone Zigbee2MQTT repository
git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt

# Install dependencies (as user "pi")
cd /opt/zigbee2mqtt
npm ci
