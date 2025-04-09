#!/bin/bash

echo "Setting up Greenhouse Monitoring System Services..."

VENV_PYTHON=$(which python)
echo "Using Python from: $VENV_PYTHON"
SCRIPT_DIR=$(pwd)

echo "Creating systemd service for data logger..."
cat > greenhouse-logger.service << EOF
[Unit]
Description=Greenhouse Sensor Data Logger
After=network.target

[Service]
ExecStart=$VENV_PYTHON $SCRIPT_DIR/data_logger.py
WorkingDirectory=$SCRIPT_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo mv greenhouse-logger.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-logger.service
sudo systemctl start greenhouse-logger.service

echo "Creating systemd service for dashboard..."
cat > greenhouse-dashboard.service << EOF
[Unit]
Description=Greenhouse Monitoring Dashboard
After=network.target

[Service]
ExecStart=$VENV_PYTHON $SCRIPT_DIR/web_dashboard.py
WorkingDirectory=$SCRIPT_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo mv greenhouse-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable greenhouse-dashboard.service
sudo systemctl start greenhouse-dashboard.service

IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "Setup complete!"
echo "Data logger and dashboard services have been installed and started."
echo "You can view your dashboard at http://$IP_ADDRESS:8080"
echo "To check service status, you can use:"
echo "  sudo systemctl status greenhouse-logger.service"
echo "  sudo systemctl status greenhouse-dashboard.service"
