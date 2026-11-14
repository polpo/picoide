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

PicoIDE when used with the front panel consists of two microcontrollers, each with its own firmware that work in concert with the other. The PicoIDE firmware bundles firmwares for both in a single `picoide.uf2` file and the update process updates both automatically.

If a firmware update fails, the firmware will automatically be rolled back to the last known good version.

## Updating Firmware (via front panel)

### Via front panel

1. Download and extract the latest firmware bundle at the [releases page](../releases.md).
1. Copy `picoide.uf2` to the `/firmware` folder on your SD card
2. Insert the SD card into PicoIDE
3. Using the front panel, navigate to: **Settings > Firmware Update**
4. The panel shows the currently running version and the version on the SD card.
5. Press the right button to continue.
6. Wait for the update to complete (progress shown on display).
7. PicoIDE automatically reboots into the new firmware

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

- Verify the `picoide.uf2` firmware file is in the `/firmware/` directory on the SD card
- Ensure the name is named exactly `picoide.uf2` (future firmware versions may make this more lenient)

### Update Fails

- Try re-downloading the firmware file as it may be corrupted
- Try a different microSD card, freshly formatted with the [SD Association Formatater](https://www.sdcard.org/downloads/formatter/)
