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
# PicoIDE

<figure markdown="span" style="float: right; margin-left: 1em; max-width: 200px;">
![The PicoIDE mascot, a woodpacker](https://picoide.com/picoides.png){ width=200 }
    <figcaption>the PicoIDE mascot is a member of the __[Picoides](https://en.wikipedia.org/wiki/Picoides)__ genus</figcaption>
</figure>

[PicoIDE](https://picoide.com) is a device that emulates IDE/ATAPI devices developed by Ian Scott, creator of [PicoGUS](https://picog.us). 

## Features

- **ATAPI CD-ROM Emulation** - Mount `.iso` and `.cue/.bin` CD images with audio track support using built-in DAC
- **IDE Hard Disk Emulation** - Mount `.vhd`, `.img`, and other raw disk images with LBA or arbitrary CHS
- **Front Panel** - (optional) OLED display with 4-button navigation and WiFi radio
- **Web Interface** - (optional) Swap and upload images over WiFi
- **Host control** - Control PicoIDE with apps on your host system (DOS only for now)

## Quick Start

1. [Set up the hardware](getting-started.md) - Connect PicoIDE to your vintage computer
2. [Prepare your SD card](sd-card.md) - Create the directory structure and add your disk images
3. [Configure the device](sd-card.md#configuration-file) - Edit `picoide.ini` for auto-loading (optional)
4. Enjoy!

## Documentation Sections

- **[Getting Started](getting-started.md)** - Hardware setup, jumper configuration, and mounting options
- **[SD Card Setup](sd-card.md)** - Directory layout and configuration file reference
- **[Front Panel](front-panel.md)** - Using the optional OLED display and buttons
- **[Web Interface](web-interface.md)** - WiFi setup and remote management
- **[Host Control (pidectl)](pidectl.md)** - Control PicoIDE from DOS
- **[Firmware Updates](firmware-updates.md)** - Updating the main board and front panel firmware
