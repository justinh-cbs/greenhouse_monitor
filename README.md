# greenhouse_monitor

A small project to monitor my portable greenhouse and hopefully stop me from killing all my plants... again...  

I'm running this on a RPi Zero 2, and the sensor is a cheap DHT11 that I had sitting around. For better resolution in temp and humidity I'd recommend the DHT22, but I'm just working with what I have.  

Install the Adafruit library for the sensor:  
`sudo pip3 install Adafruit_DHT`  

Give the setup script permission:  
`chmod +x setup.sh`  
`./setup.sh`  

This will:  
  
Install all required dependencies  
Make the scripts executable  
Set up systemd services to run the data logger and dashboard automatically  
Start both services  

To access the dashboard:  
Open a web browser and navigate to `http://<pi_ip_address>:8080`  

