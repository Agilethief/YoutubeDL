# Tips and running notes

## Service

service name: ytdl
sudo nano /etc/systemd/system/ytdl.service

sudo systemctl daemon-reload
sudo systemctl restart ytdl.service
sudo systemctl status ytdl.service
sudo systemctl start ytdl.service
sudo systemctl stop ytdl.service
sudo systemctl enable ytdl.service

firewall
sudo ufw allow 5001
