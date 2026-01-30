# Setting up Raspberry Pi Zero 2 W as a LTE hotspot in headless mode (Edge)

## Hardware
- A Raspberry Pi Zero 2 W
- A Clipper LTE Mini HAT from Pimoroni

## Set up Clipper Mini HAT
Follow this tutorial : https://learn.pimoroni.com/article/getting-started-with-clipper-hat#troubleshooting

You should have an interface named **ppp0** with internet access, which represents the Clipper.

## Turn Pi into a LTE hotspot with NetworkManager
### 1. Install packages

`sudo apt install iptables`

### 2. Create the Wifi hotspot (put Pi in AP mode)

`sudo nmcli device wifi hotspot ifname wlan0 ssid {your_ssid} password {your_password}`

*Attention, this will disconnect you from Pi if you were SSH-ing into Pi via Wifi. To continue working after Hotspot starts, you can SSH over USB or reconnect to the new hotspot you just created.*

This creates:
- Wi‑Fi AP on wlan0
- DHCP server handled automatically by NetworkManager
- Default IP range = 10.42.0.0/24

You can check it by looking for a connection named **Hotspot**

### 3. Enable IP forwarding

Run :
```
echo "net.ipv4.ip_forward=1" | sudo tee /etc/sysctl.d/99-ipforward.conf
sudo sysctl -p /etc/sysctl.d/99-ipforward.conf
```

Check :

`sysctl net.ipv4.ip_forward` # should return 1

### 4. Set up NAT/Masquerading from wlan0 to ppp0

Run:
```
sudo iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o ppp0 -j ACCEPT
sudo iptables -A FORWARD -i ppp0 -o wlan0 -j ACCEPT
```

Make this persistent :

`sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"`

Load on boot by editing :

`sudo nano /etc/rc.local`

Add this before **exit 0** :

`iptables-restore < /etc/iptables.ipv4.nat`

### 5. Reboot

`sudo reboot`

This restarts everything and applies the new set up. This should disconnect you from Pi since SSH via Wifi breaks.

### 6. Test the LTE hotspot

Wait for 1 minute so Pi reboots properly, then SSH into it via the default network (for example, a home Wifi).

Start the LTE hotspot :
```
sudo nmcli device wifi hotspot ifname wlan0 ssid {your_ssid} password {your_password}
sudo pon clipper
```

Test the internet connection in a Pi terminal :

`ping -I ppp0 -c 3 8.8.8.8`

If **ping** responds, you are good to go.

Now you should see the Pi's hotspot in your phone/laptop. Connect to it and test the connection. On your phone, browse a website. On your laptop, run :

`ping -c 3 8.8.8.8`

## Auto start the hotspot on boot
### 1. Create a systemd service

Run :

`sudo nano /etc/systemd/system/start-hotspot.service`

Add this :
```
[Unit]
Description=Start Wi‑Fi Hotspot then LTE (ppp0) at boot
After=network-online.target NetworkManager.service
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/nmcli device wifi hotspot ifname wlan0 ssid {your_ssid} password {your_password}
ExecStart=/bin/sleep 10
ExecStart=/usr/bin/pon clipper
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

### 2. Enable the service
```
sudo systemctl daemon-reload
sudo systemctl enable start-hotspot.service
systemctl status start-hotspot.service
```

### 3. Reboot

`sudo reboot`

Now you can reconnect to Pi via the LTE hotspot.