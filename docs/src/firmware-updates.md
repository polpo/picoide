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
# Firmware Updates

PicoIDE consists of two microcontrollers, each with its own firmware that is loaded independently but works in concert with the other. Because of this, the firmware download bundle includes both files, so please update both!

## Overview

| Component | Processor | Firmware File |
|-----------|-----------|---------------|
| Main Board | RP2350 | `picoide.uf2` |
| Front Panel | ESP32-C3 | `picoide-frontpanel.bin` |

If a firmware update fails, the firmware will automatically be rolled back to the last known good version.

## Updating Firmware (via front panel)

### Via front panel

1. Download and extract the latest firmware bundle at the [releases page](https://github.com/polpo/picoide/releases).
1. Copy the `picoide.uf2` and `picoide-frontpanel.bin` files to the `/firmware` folder on your SD card
2. Insert the SD card into PicoIDE
3. Using the front panel, navigate to: **Settings > Firmware Update**
4. Select **Main Board** and confirm the update
5. Wait for the update to complete (progress shown on display)
6. PicoIDE automatically reboots into the new firmware
7. Select **Front Panel** and confirm the update
8. Wait for the update to complete
9. Front panel automatically reboots

### Via pidectl

Instructions to come before final release

## Checking Current Versions

### From System Info

Navigate to: **Main Menu > System Info**

This displays:

- Main board firmware version
- Front panel firmware version
- Connection status

### From Firmware Update Screen

Navigate to: **Settings > Firmware Update**

This shows:

- Current version for each component
- Available version (if update file present on SD card)

## Troubleshooting Updates

### Update Not Detected

- Verify the `picoide.uf2` and `picoide-frontpanel.bin` firmware files are in `/firmware/` directory
- Try removing and reinserting the SD card

### Update Fails

- Try re-downloading the firmware file as it may be corrupted
- Try a different, freshly formatted microSD card
