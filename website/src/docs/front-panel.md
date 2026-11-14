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
| **Up** | Top | Navigate up, previous image on status screen) |
| **Down** | Bottom | Navigate down, next image on status screen) |
| **Select** (✓ symbol) | Right | Confirm selection, enter menu |
| **Cancel** (× symbol) | Left | Cancel, exit menu, eject on status screen |

## Screens

### Splash Screen

Displayed briefly at power-on, showing:

- PicoIDE firmware version
- Initialization progress

### Status Screen

The main display when PicoIDE is running:

- **Top bar**: Current directory path and image position (e.g., "3/12")
- **Center**: Current image name (scrolls horizontally if too long)
- **Bottom**: [Playback status](#cd-rom-playback-display) (audio or mixed-mode discs in CD-ROM mode only)

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
| **Select Device** | If in dual mode, select either device 0 or 1 |
| **Select Image** | Browse and select a new image |
| **Eject Image** | Eject current image (ATAPI only) |
| **Settings** | Access device settings |
| **System Info** | View firmware versions and status |

### Select Image Menu

Navigate your SD card to select images:

- Directories shown in `[brackets]`
- Files shown by name
- `..` entry to go up one level
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
| **Display Settings** | Settings for screen saver and display dimming |

#### Display Submenu

When no buttons have been pressed for a while, the display first goes into an idle mode (dimmed or a screen saver), then can later blank completely to protect the OLED screen. The menu shows the current value of each setting, for example "Idle Mode: Dim".

| Option | Choices | Default | Description |
|--------|---------|---------|-------------|
| **Idle Mode** | Dim, Flying Toasters, DVD Logo | Dim | What the display does after idle time: dim the screen or show a screen saver |
| **Idle Time** | 30 sec, 1 min, 2 min, 5 min, Never | 2 min | How long without a button press before the idle mode starts |
| **Blank Time** | 10 min, 20 min, 30 min, 1 hour, Never | 10 min | How long without a button press before the display turns off completely |

!!! tip "Waking the display"
    When the display is dimmed, showing a screen saver, or blanked, the first button press only wakes it, not performing its normal action so you don't accidentally load or eject an image while waking the screen. While the display is blanked, the activity LED slowly pulses so you can tell PicoIDE is still powered.

#### WiFi Submenu

| Option | Description |
|--------|-------------|
| **WiFi Status** | View current connection info (SSID, IP address) |
| **Reset WiFi** | Clear saved credentials and restart in AP mode with default password |

## CD-ROM Playback Display

In CD-ROM mode, the status screen shows playback info if an audio track is playing:

- Play/Pause/Stop status
- Current track number
- Track position (MM:SS format)
