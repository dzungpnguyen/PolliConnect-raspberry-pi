# Setting up headless Raspberry Pi as a Wifi Access Point (via SSH)

This document is inspired by [a tutorial for non-headless Pi](https://learn.sparkfun.com/tutorials/setting-up-a-raspberry-pi-3-as-an-access-point).

Before starting, make sure your Pi and your computer are connected to the same network.

## SSH to Pi

In a terminal, establish a SSH connection to Pi using the command: `ssh <user-name>@<ip-pi>`

`ssh polliconnect@192.168.1.203`

Then enter the user password.

## Install packages

`sudo apt-get -y install hostapd dnsmasq`

## Set static IP address

1. Ignore the wireless interface `wlan0`

Edit the `hdcpcd.conf` file:

`sudo nano /etc/dhcpcd.conf`

Add at the bottom of the file:

`denyinterfaces wlan0`

Save changes and exit.

2. Set a static IP address for the Wifi interface

Open de `interfaces` file:

`sudo nano /etc/network/interfaces`

Add at the bottom of the file:

```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.5.1
    netmask 255.255.255.0
    network 192.168.5.0
```

Save changes and exit.

## Configure hostapd

Edit the `hostapd.conf` file:

`sudo nano /etc/hostapd/hoastapd.conf`

Add the following to that file. You can freely change the `ssid` (Wifi network name) and the `wpa_passphrase` (network password).

```
interface=wlan0
driver=nl80211
ssid=MySSID
hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=1
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=MyPassphrase
rsn_pairwise=CCMP
```

Save changes and exit.

Tell `hostapd` where to file this configuration file by open the `hostapd` startup script:

`sudo nano /etc/default/hostapd`

Uncomment the line `#DAEMON_CONF=""` and replace it with:

`DAEMON_CONF="/etc/hostapd/hostapd.conf"`

Save changes and exit.

## Configure dnsmasq

Back up the `dnsmasq.conf` file and open a new one for editing:

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.backup
sudo nano /etc/dnsmasq.conf
```

Add the following to the blank file:

```
interface=wlan0 
listen-address=192.168.5.1
bind-interfaces 
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.5.100,192.168.5.200,24h
```

## Verify AP configuration before rebooting (MUST DO if you have a headless Pi)

Make sure all AP services are enabled:

```
sudo systemctl status hostapd
sudo systemctl status dnsmasq
```

You should see for each service, the line `Loaded: ..., enabled; ...`. If not, unmask the service (if it shows `Loaded: masked...`) and enable it:

```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl unmask dnsmasq
sudo systemctl enable dnsmasq
```

This enables both services at boot. To verify:

```
systemctl is-enabled hostapd
systemctl is-enabled dnsmasq
```

Test the AP config without rebooting:

`sudo hostapd -dd /etc/hostapd/hostapd.conf`

Look for the line `wlan0: AP-ENABLED` and any fatal errors. If no error, you can safely reboot Pi:

`sudo reboot`

This will close the SSH session since Pi and your computer are no longer under the same network. Wait for 30s-1m, you should see PolliEdgeAP appears as a wireless network from your computer.

Connect to the network using the predefined password and SSH to `192.168.5.1`.