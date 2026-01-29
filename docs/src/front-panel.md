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
# Front Panel

The optional front panel module provides a physical interface for controlling PicoIDE and seeing its status. It also includes a WiFi interface - see [Web Interface](web-interface.md) for details.

## Button Layout

| Button | Position | Functions |
|--------|----------|-----------|
| **Up** | Top | Navigate up, previous image |
| **Down** | Bottom | Navigate down, next image |
| **Select** (✓ symbol) | Right | Confirm selection, enter menu |
| **Cancel** ( ×symbol) | Left | Cancel, exit menu, eject |

## Screens

### Splash Screen

Displayed briefly at power-on, showing:

- PicoIDE logo
- Front panel firmware version
- Initialization progress

### Status Screen

The main display when PicoIDE is running:

- **Top bar**: Current directory path and image position (e.g., "3/12")
- **Center**: Current image name (scrolls horizontally if too long)
- **Bottom**: [Playback status](#cd-rom-playback-display) (mixed-mode discs in CD-ROM mode only)

#### Navigation from Status Screen

| Button | Action |
|--------|--------|
| Up | Load previous image in directory |
| Down | Load next image in directory |
| Select | Open main menu |
| Cancel | Eject current image (ATAPI mode only) |

!!! note "IDE Mode Limitations"
    In IDE (hard disk) mode, ejecting is not available because fixed hard disks don't support hot-swapping. Selecting a new image will only take effect when the system resets.

### Main Menu

Press **Select** from the status screen to access the main menu:

| Option | Description |
|--------|-------------|
| **Select Image** | Browse and select a new image |
| **Eject Image** | Eject current image (ATAPI only) |
| **Settings** | Access device settings |
| **System Info** | View firmware versions and status |

### Select Image Menu

Navigate your SD card to select images:

- Directories shown in `[brackets]`
- Files shown by name
- `..` entry to go up one level (or press Cancel button)
- Scrollbar appears when list exceeds screen
- Long file names will scroll to show the full file name

| Button | Action |
|--------|--------|
| Up/Down | Navigate list |
| Select | Open directory or load image |
| Cancel | Return to parent directory |

### Settings Menu

| Option | Description |
|--------|-------------|
| **Firmware Update** | Check for and install firmware updates |
| **WiFi** | Configure WiFi settings |

#### WiFi Submenu

| Option | Description |
|--------|-------------|
| **WiFi Status** | View current connection info (SSID, IP address) |
| **Reset WiFi** | Clear saved credentials, restart in AP mode with default password |

## Display Behavior

### Screen Saving

The display automatically dims and turns off to save the life of the OLED:

| State | Timeout | Brightness |
|-------|---------|------------|
| Active | - | full |
| Dimmed | 30 seconds idle | half |
| Off | 2 minutes idle | zero |

Any button press wakes the display:

- From **dimmed**: Button action is performed
- From **off**: Display wakes, no action performed

## CD-ROM Playback Display

In ATAPI mode, the status screen shows audio playback information:

- Play/Pause/Stop status
- Current track number
- Track position (MM:SS format)

Data-only tracks display "Data track" instead of timing information.
