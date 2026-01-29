<!---
SPDX-License-Identifier: GPL-2.0-only

Copyright (C) 2026  Ian Scott

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License (as published by the
Free Software Foundation) version 2, dated June 1991.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, see <https://www.gnu.org/licenses/>.
-->
# Web Interface

The front panel module includes WiFi capability for remote management through a web browser.

## Initial WiFi Setup

On first boot (or after a WiFi reset), the front panel creates its own WiFi access point:

| Setting | Value |
|---------|-------|
| **SSID** | `PicoIDE-FrontPanel` |
| **Password** | `frontpanel123` |
| **IP Address** | `192.168.4.1` |
| **Hostname (Zeroconf/mDNS)** | `picoide.local` |

### Connecting to the Access Point

1. On your computer or phone, connect to the `PicoIDE-FrontPanel` WiFi network
2. Enter password: `frontpanel123`
3. Open a web browser and navigate to [`http://picoide.local`](http://picoide.local) or [`http://192.168.4.1`](http://192.168.4.1)

## Connecting to Your Network

To connect PicoIDE to your existing WiFi network:

1. Access the web interface via the access point (see above)
2. Click **Scan Networks**
3. Select your network from the list
4. Enter your network password
5. Click **Connect**

Once connected, PicoIDE will:

- Be accessible at `http://picoide.local` under the new IP (if your network supports mDNS)
- Remember the WiFi config for future boots. This is stored on the front panel so it will persist even if you change the microSD card.
- Display its new IP address on the front panel under Settings > WiFi > WiFi Status

!!! tip "Finding the IP Address"
    If mDNS doesn't work on your network, check the WiFi Status screen on the front panel to see the assigned IP address.

## Web Interface Features

### SD Card Browser

- View currently loaded image
- Navigate directory structure
- Select images to load
- Previous/Next image navigation
- Eject current image (ATAPI mode)
- Upload new images

#### File Upload

Upload new images directly to your SD card:

1. Navigate to the destination directory in the card browser
2. Select a file from your computer
3. Click **Upload**
4. Monitor upload progress (speed and ETA displayed)
5. File integrity is automatically verified after upload

Files are uploaded to the currently browsed directory. With good WiFi reception, uploads run at approximately 6-10 Mbps.

### WiFi Settings

- View current connection status
- Scan for available networks
- Connect to a different network
- Reset WiFi to access point mode

### Configuration Editor

Edit your `picoide.ini` configuration file directly from the web interface. Make your changes in the text editor, click save config, and reboot the computer for the changes to take effect.

This is useful for adjusting settings like device type (IDE or ATAPI), browse directories, or transfer mode overrides without removing the SD card. See [SD Card Setup](sd-card.md#configuration-file) for the full configuration reference.

### Firmware Updates

Update both the main board and front panel firmware from the web interface:

1. Place firmware files in the `/firmware/` folder on your SD card, either directly or uploading via the SD card browser
3. Refer to the **Firmware Update** section of the web interface to see current and available versions on the SD card
4. Click **Update** for the component you want to update
5. Wait for the update to complete

The web interface shows update progress and automatically detects when the device has rebooted with the new firmware. Note that updating the front panel from the web interface may be a bit buggy, so updating from the front panel controls is recommended. Don't worry, if the update fails, it will automatically roll back to the last known good firmware version.

## Resetting WiFi

If you need to reset WiFi so it can be reconfigured:

### From Front Panel

1. Navigate to Settings > WiFi > Reset WiFi
2. Confirm the reset
3. PicoIDE restarts in access point mode

### From Web Interface

1. Find WiFi Settings
2. Click **Reset to AP Mode**
3. Reconnect using the default credentials

## WiFi/Network Specs

- 2.4 GHz WiFi only (5 GHz not supported)
- WPA/WPA2/WPA3 security supported
- DHCP for automatic IP assignment required
