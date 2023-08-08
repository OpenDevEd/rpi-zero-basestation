echo "Setting up pm2 processes"
echo "setting up pijuice_tools process"
cd pijuice_tools
pm2 start pm2_process.json
pm2 save
echo "setting up pijuice_tools process done"
echo "setting up sensorboard process"
cd ../sensorboard
pm2 start pm2_sensorboard_process.json
pm2 save
echo "setting up sensorboard process done"
echo "setting up sensorboard-pm process"
pm2 start pm2_sensorboard-pm_process.json
pm2 save
echo "setting up sensorboard-pm process done"
echo "setting up zigbee process"
cd ../zigbee
pm2 start pm2_zigbee_process.json
pm2 save
echo "setting up zigbee process done"
echo "setting up lora process"
cd ../Lora
pm2 start pm2_loralogger_process.json
pm2 save
echo "setting up lora process done"
echo "setting up core-temp process"
cd ../core-temp
pm2 start pm2_process.json
pm2 save
echo "setting up core-temp process done"
