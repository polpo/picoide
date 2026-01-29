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
# SD Card Setup

PicoIDE uses a microSD card to store disk and CD-ROM images along with configuration settings.

## Requirements

- microSD card (newer cards are recommended)
- FAT32 or exFAT formatted with MBR partitioning. Formatting with the [SD Association's SD Card Formatter](https://www.sdcard.org/downloads/formatter/) is _strongly_ recommended!

!!! tip "Card Selection"
    While most microSD cards work fine, higher-speed cards (Class 10 or UHS-I) provide better performance.

## Directory Layout

The following is an example directory structure on the SD card. `cdrom/` and `hdd/` are default locations for those types of images but they can be put elsewhere on the card.

```
/
├── cdrom/                      # CD-ROM images (ATAPI mode)
│   ├── game.iso
│   ├── album.cue
│   ├── album.bin
│   └── Big Game/               # Subdirectories supported
│       └── Disc 1.iso
│       └── Disc 2.iso
├── hdd/                        # Hard disk images (IDE mode)
│   ├── dos622.img
│   └── windows98.vhd
├── firmware/                   # Firmware update files
│   ├── picoide.uf2             # Main board firmware
│   └── picoide-frontpanel.bin  # Front panel firmware
└── picoide.ini                 # Configuration file
```

### Supported File Formats

#### ATAPI Mode (CD-ROM)

| Extension | Description |
|-----------|-------------|
| `.iso` | ISO 9660 disc image |
| `.cue` | CUE sheet with associated `.bin` file(s) |
| `.toast` | Disc image commonly used on vintage Macs |

!!! note "bin/cue Images"
    For bin/cue CD images, place the `.cue` file and all referenced `.bin` files in the same directory. PicoIDE supports audio tracks for CD music playback.

#### IDE Mode (Hard Disk)

| Extension | Description |
|-----------|-------------|
| `.vhd` | [Virtual Hard Disk](https://en.wikipedia.org/wiki/VHD_%28file_format%29) (supports baked-in CHS geometry) |
| `.img` | Raw disk image |
| `.hda` | Raw disk image |
| `.hdf` | Raw disk image (Amiga, RDB format only) |

!!! note "VHD Images"
    Only fixed VHD images are supported. Dynamic and differencing VHD images will not work.

    [86Box](https://86box.net/) is great for creating VHD images with arbitrary CHS geometry and setting them up ahead of time.

!!! note "HDF Images"
    Amiga "hardfile" HDF images are not supported - only raw images including the RDB are supported. Images created from actual Amiga disks or partitioned RDB images from Amiga emulators will work.

## Configuration File

The `picoide.ini` file controls device behavior and auto-loading. Place it in the root of your SD card. If you have the front panel installed, you can also edit this file from the [web interface](web-interface.md#configuration-editor).

### Example Configuration

```ini
# PicoIDE Configuration File

[device]
# Device type: IDE (hard disk) or ATAPI (CD-ROM)
type = ATAPI

[ide]
# Full path to hard disk image (leave empty for first found)
image_path = /hdd/windows98.img

# Directory to browse for hard disk images
browse_dir = /hdd

[atapi]
# Full path to CD-ROM image (leave empty for first found)
image_path = /cdrom/game.iso

# Directory to browse for CD-ROM images
browse_dir = /cdrom

# Auto-load image at boot time
auto_load = true
```

### Configuration Reference

#### `[device]` Section

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `type` | `IDE`, `ATAPI` | `ATAPI` | Device emulation mode |

#### `[ide]` Section

| Setting | Description |
|---------|-------------|
| `image_path` | Full path to auto-load (empty = first alphabetically in browse_dir) |
| `browse_dir` | Directory for image browsing (default: `/hdd`) |

#### `[atapi]` Section

| Setting | Description |
|---------|-------------|
| `image_path` | Full path to auto-load (empty = first alphabetically in browse_dir) |
| `browse_dir` | Directory for image browsing (default: `/cdrom`) |
| `auto_load` | `true`, `false` | `true` | Load image automatically at boot |

!!! info "Auto `image_path` Updating"
    When you select a different image using the front panel or host control, the configuration file is automatically updated to remember your selection.

#### `[overrides]` Section

Advanced settings to override the maximum transfer mode, IDENTIFY responses, etc. These are primarily useful for troubleshooting compatibility issues with certain vintage computers.

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `max_pio_mode` | `0`-`4` | `4` | Maximum PIO transfer mode |
| `max_mwdma_mode` | `0`-`2` or `-1` | `2` | Maximum Multi-word DMA mode (`-1` disables DMA) |
| `disable_iordy` | `true`, `false` | `false` | Disable IORDY flow control |
| `sector_delay_us` | `0`-`1000` | `0` | Delay in microseconds between sectors during multi-sector PIO reads |
| `bus_delay` | `1.0`-`6.0` | `1.0` | Bus timing delay factor for slow or noisy IDE buses |

Example for forcing PIO-only operation:
```ini
[overrides]
max_mwdma_mode = -1
```

Example for disabling IORDY flow control (for older systems with IORDY issues, or for a small speed boost on tolerant systems):
```ini
[overrides]
disable_iordy = true
```

Example for fixing hangs during boot on systems with BIOSes that expect to see BSY between sectors:
```ini
[overrides]
sector_delay_us = 100
```

Example for slowing bus timing on very old systems (e.g., IBM 5170):
```ini
[overrides]
bus_delay = 6.0
```

## Auto-Mount Behavior

When `auto_load` is enabled in ATAPI mode:

- **With `image_path` set**: Loads the specified image
- **With `image_path` empty**: Loads the first image found alphabetically in the browse directory

This allows for completely headless operation - just power on and the configured image is ready.

!!! note "Auto-mount in IDE mode"
    If the device is in IDE mode and an image cannot be loaded, it will result in an error as PicoIDE only supports emulating a fixed (non-removable) disk.

## Tips

### Organizing Images

Use subdirectories to organize your collection:

```
/cdrom/
├── games/
│   ├── doom.iso
│   ├── quake.iso
│   └── big game/
│       ├── disc 1.iso
│       └── disc 2.iso
├── os install/
│   └── win98cd.iso
└── music/
    └── album.cue
```

### Case Insensitivity

Paths and file names specified in `picoide.ini` are case-insensitive due to the FAT file system on the SD card.
