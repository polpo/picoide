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
├── cdrom/                      # CD-ROM images (ATAPI)
│   ├── game.iso
│   ├── album.cue
│   ├── album.bin
│   └── Big Game/               # Subdirectories supported
│       └── Disc 1.iso
│       └── Disc 2.iso
├── hdd/                        # Hard disk images (IDE)
│   ├── dos622.img
│   └── windows98.vhd
├── firmware/                   # Firmware update files
│   ├── picoide.uf2             # Main board firmware
│   └── picoide-frontpanel.bin  # Front panel firmware
└── picoide.ini                 # Configuration file
```

### Supported File Formats

The file type of an image also determines which kind of device PicoIDE emulates for it. See [Configuration File](#configuration-file) for more detail.

#### CD-ROM (ATAPI)

| Extension | Description |
|-----------|-------------|
| `.iso` | ISO 9660 disc image |
| `.cue` | CUE sheet with associated `.bin` file(s) |
| `.toast` | Disc image commonly used on vintage Macs |

!!! note "bin/cue Images"
    For bin/cue CD images, place the `.cue` file and all referenced `.bin` files in the same directory. PicoIDE supports audio tracks for CD music playback.

#### Hard Disk (IDE)

| Extension | Description |
|-----------|-------------|
| `.vhd` | [Virtual Hard Disk](https://en.wikipedia.org/wiki/VHD_%28file_format%29) (supports baked-in CHS geometry) |
| `.img` | Raw disk image |
| `.hda` | Raw disk image |
| `.hdf` | Raw disk image (Amiga, RDB format only) |
| `.raw` | Raw disk image |

!!! note "VHD Images"
    Only fixed VHD images are supported. Dynamic and differencing VHD images will not work.

    [86Box](https://86box.net/) is great for creating VHD images with arbitrary CHS geometry and setting them up ahead of time.

!!! note "HDF Images"
    Amiga "hardfile" HDF images are not supported - only raw images including the RDB are supported. Images created from actual Amiga disks or partitioned RDB images from Amiga emulators will work.

## Configuration File

The `picoide.ini` file controls which devices PicoIDE emulates and which images they load at startup. PicoIDE will automatically generate one at the root of the SD card the first time it loads an image. If you have the front panel installed, you can edit this file from the [web interface](web-interface.md#configuration-editor).

Each emulated device is described by its own section, `[device0]` and `[device1]`. Which of them are used depends on the M/S/CS jumper (see [Device Selection](getting-started.md#device-selection)):

| Jumper | Sections used |
|--------|---------------|
| **M**, **S**, or **CS** (single-device mode) | `[device0]` only, which configures the one emulated device determined by the jumper. `[device1]` is ignored |
| **none** (dual-device mode) | `[device0]` describes device 0 and `[device1]` describes device 1 |

### Example Configuration

A single device that boots from a hard disk image:

```ini
# PicoIDE Configuration File

[device0]
image = /hdd/windows98.img
```

PicoIDE determines the device type to emulate from the image's file extension, so in most cases the `image` line is all you need.

In dual-device mode, add a `[device1]` section for the second device:

```ini
[device0]
image = /hdd/windows98.img

[device1]
image = /cdrom/game.iso
```

This config has both a hard disk and a CD-ROM drive, but each device can independently be either type depending on what's in the .ini file.

### Configuration Reference

#### `[device0]` and `[device1]` Sections

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `image` | path | (empty) | Image to load at startup, and what the device type is inferred from. Empty = load the first image found alphabetically in `browse_dir` |
| `type` | `cdrom`, `hdd` | `cdrom` | Which device to emulate. Usually unnecessary, as it's inferred from `image`, but if `image` is empty this will be used |
| `browse_dir` | path | `/cdrom` or `/hdd`, depending on device type | Directory to browse for images, and to auto-load the first image from when `image` is empty |
| `auto_load` | `true`, `false` | `true` | Load an image at startup. Set to `false` to start with an empty CD-ROM drive |

Device type is inferred from the file type of `image`:

| Image file type | Device emulated |
|-----------------|-----------------|
| `.iso`, `.cue`, `.toast` | CD-ROM (ATAPI) |
| `.img`, `.vhd`, `.hda`, `.hdf`, `.raw` | Hard disk (IDE) |

Set `type` explicitly when there's no image to infer from, for example if you want an empty CD-ROM drive that you'll load a disc into later from the front panel:

```ini
[device0]
type = cdrom
auto_load = false
```

!!! info "Automatic `image` Updating"
    When you select a different image using the front panel, web interface, or host control, that device's `image` setting is automatically updated to remember your selection.

##### Hard Disk Geometry

By default, a hard disk's geometry (cylinders, heads and sectors per track) is derived from the image itself, using the following methods in order:

1. If the image is a fixed VHD, the image's own built-in geometry
2. If the image has an MBR partition table, the geometry it was written with
3. Otherwise, the geometry is calculated from the image size.

Geometries larger than the ATA limit of 16383 cylinders, 16 heads and 63 sectors per track are reported as 16383/16/63.

To override this, the following options can be added to the image's `[device0]` or `[device1]` section:

| Setting | Values | Description |
|---------|--------|-------------|
| `heads` | `1`-`16` | Number of heads |
| `sectors` | `1`-`255` | Sectors per track |
| `cylinders` | `1`-`65535` | Number of cylinders. Optional: if omitted, it's calculated from the image size |

`heads` and `sectors` must both be set, or the geometry override is ignored. For example, NEC PC-9821 machines expect IDE hard disks up to about 4.5 GB to use 8 heads and 17 sectors per track, rather than the common 16 heads and 63 sectors:

```ini
[device0]
image = /hdd/pc98.img
heads = 8
sectors = 17
```

With `cylinders` left out, it's calculated from the image size.

!!! warning "Geometry larger than the image"
    If you set `cylinders` explicitly, PicoIDE uses it even if cylinders * heads * sectors is larger than the image. The host will see errors when it tries to access the sectors past the end of the image.

##### Drive Identity

Each device reports a model name, firmware revision and serial number to the host. CD-ROM drives also report a vendor, product and revision. Some software and drivers check these, so you can override them per device:

| Setting | Max length | Default | Description |
|---------|------------|---------|-------------|
| `model` | 40 | `PicoIDE Hard Disk` or `PicoIDE Totally Legit CD-ROM drive` | Model name |
| `revision` | 8 | `v1.0.0` (hard disk) or `v420.69` (CD-ROM) | Firmware revision |
| `serial` | 20 | The PicoIDE board's unique ID | Serial number |
| `vendor` | 8 | `PicoIDE` | CD-ROM only: vendor name |
| `product` | 16 | `Virtual CD-ROM` | CD-ROM only: product name |
| `product_revision` | 4 | `1234` | CD-ROM only: product revision |

Longer values are cut off at the maximum length. For example, the Konami System 573 arcade platform shipped with a Matsushita CR-58x CD-ROM drive. To make PicoIDE identify as that drive:

```ini
[device0]
image = /cdrom/ddr.cue
model = MATSHITA CR-589
revision = 1.0
vendor = MATSHITA
product = CD-ROM CR-589
product_revision = GS0N
```

!!! note "Serial numbers in dual-device mode"
    Unless `serial` is set, both devices report the same serial number, the board's unique ID.

#### `[overrides]` Section

Advanced settings to override the maximum transfer mode, bus timing, logging, etc. to fix compatibility issues with certain vintage computers. They apply to the IDE bus as a whole, so in dual-device mode both devices share them. To change what a drive identifies itself as, see [Drive Identity](#drive-identity).

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `max_pio_mode` | `0`-`4` | `4` | Maximum PIO transfer mode |
| `max_mwdma_mode` | `0`-`2` or `-1` | `2` | Maximum Multi-word DMA mode (`-1` disables DMA) |
| `disable_iordy` | `true`, `false` | `false` | Disable IORDY flow control |
| `sector_delay_us` | `0`-`1000` | `0` | Delay in microseconds between sectors during multi-sector PIO reads |
| `mwdma_cycle_time` | `120`-`1200` or `0` | `0` | Multi-word DMA cycle time in ns (`0` = standard minimum for the advertised mode) |
| `atapi_complete_delay_us` | `0`-`10000` | `1000` | Delay in microseconds before a CD-ROM finishes a short command while DMA is enabled. Gives slow host drivers time to get ready for the interrupt (for example the VIA VT6421 Windows 9x driver) |
| `bus_delay` | `1`-`6` | `1` | Bus timing delay factor for slow or noisy IDE buses. Values above `2` also limit PIO to mode 2 |
| `log` | `true`, `false` | `true` | Write a log to `log.txt` on the SD card. The previous boot's log is kept as `lastlog.txt` |
| `debug` | `true`, `false` | `false` | Add detailed debug messages to the log |

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

Example for the beige Power Macintosh G3, which needs slightly slower Multi-word DMA burst timing than the 120ns default:
```ini
[overrides]
mwdma_cycle_time = 180
```

Example for slowing bus timing on very old systems (e.g., IBM 5170):
```ini
[overrides]
bus_delay = 6
```

## Auto-Mount Behavior

Each device mounts an image at startup independently, following its own section:

- **With `image` set**: Loads that image. If it can't be loaded, falls back to the first image found in the browse directory
- **With `image` empty**: Loads the first image found alphabetically in the browse directory
- **With `auto_load = false`**: Loads nothing, leaving an empty CD-ROM drive

This allows for completely headless operation - just power on and the configured image is ready.

!!! note "Auto-mount for hard disks"
    If a hard disk device can't load an image, the host will see errors, as PicoIDE currently only supports emulating a fixed (non-removable) disk. `auto_load = false` is only useful for CD-ROM devices.

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
