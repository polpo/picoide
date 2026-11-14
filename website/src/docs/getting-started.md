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
# Getting Started

This guide covers the initial hardware setup for PicoIDE.

## What You'll Need

- PicoIDE unit
- SD card, FAT32 or exFAT formatted with MBR partitioning, best formatted with the [SD Association's SD Card Formatter](https://www.sdcard.org/downloads/formatter/)
- IDE ribbon cable
- 4-pin floppy/berg power connector

## Jumper Configuration

### Device Selection

The M/S/CS jumper block determines PicoIDE's device selection on the IDE bus:

| Jumper Position | Mode | Description |
|-----------------|------|-------------|
| **M** | Device 0 | Traditionally named "master" |
| **S** | Device 1 | Traditionally named "slave" |
| **CS** (cable select) | Auto | Position determined by cable |
| **none** | Dual-device | Emulate both devices on the channel simultaneously |

!!! tip "Choosing a Position"
    - Use **M** if PicoIDE is the only device on the IDE channel
    - Use **CS** only if your IDE cable supports cable select (80-pin cables with blue/gray IDE connectors support cable select)
    - Remove the jumper entirely for dual-device mode, described below

### Dual-Device Mode

With the jumper removed, PicoIDE emulates *both* devices on the IDE channel at once, from a single PicoIDE. Each can independently be a hard disk or a CD-ROM drive, so you can have two hard disks, two CD-ROM drives, or one of each.

Each device is configured by its own section in `picoide.ini`: `[device0]` and `[device1]`. See [Configuration File](sd-card.md#configuration-file) for the details.

!!! warning "In dual mode, PicoIDE must be the only device on the cable"
    In dual-device mode PicoIDE occupies both device positions, so no other drive can share the IDE cable with it.

!!! danger "Don't park the jumper shunt on the jumper block in dual mode"
    Be careful as two of the pins on the jumper block are +5V and ground. If you park the jumper shunt across them it will cause a short, so in dual mode it's best to leave the jumper off completely.

## Connections

### IDE Cable

Connect the IDE ribbon cable between PicoIDE and your computer's motherboard or IDE controller card. The connector is keyed, but some cables are not, so make sure pin 1 is aligned correctly: match the stripe on the cable edge that indicates pin 1 with the pin 1 marking on both the PicoIDE (a triangle and a number `1`, which are the side of the connector closest to the power connector) and your computer's IDE connector.

### Power

Connect a standard 4-pin floppy/Berg power connector from your computer's power supply. PicoIDE only uses the +5V rail on this connector. If your power supply doesn't have a floppy power connector, use an adapter.

!!! danger "Make sure the connector is oriented correctly"
    Some floppy power cables don't have the best keying, so please ensure it's oriented correctly to avoid damage to the PicoIDE!

### Audio connectors

PicoIDE has two connectors for CD-ROM audio out: an MPC-2 compatible connector for internal connection to a sound card ([cables are still available!](https://www.amazon.com/Kentek-Universal-Computer-Internal-DVD-ROM/dp/B07KVG1ZCQ)), and a 3.5mm line out jack.

### Other connectors

There are two more connections on the PicoIDE on a standard 2.54mm header: "ext. LED" and "ext. btn". You can connect an external drive activity LED to the ext. LED connector, taking care the polarity is correct. An external action button can be connected to the ext. btn connector to switch images, etc. (support to come)

### Front Panel (Optional)

If you got a "Deluxe" PicoIDE with front panel, it should already be connected, but if you're upgrading your base PicoIDE with a front panel module, connect it using the flat flex cable to the header marked "front panel SPI" on the main board.

## Mounting Options

### External-facing Installation (Deluxe version with Front Panel)

When using the front panel, mount PicoIDE so the front panel is accessible from outside your computer case, using the rearward set of mounting holes on the sides of the PicoIDE, or the holes on the bottom.

!!! note "WiFi Reception"
    Even if you don't use the front panel controls, this is the recommended position for WiFi reception as the WiFi antenna is located at the center front of the PicoIDE.

### Internal Installation (base version without Front Panel)

To mount fully internally, use the more forward set of mounting holes on the sides of the PicoIDE.

This configuration is ideal if you don't have the optional front panel or if you prefer to manage images via the web interface over WiFi.

!!! note "Headless Operation"
    Without a front panel, PicoIDE automatically loads the first image found in the directory corresponding to the device mode (`/cdrom` for CD-ROM, `/hdd` for hard disk) unless a specific image is configured in [`picoide.ini`](sd-card.md#configuration-file).

    Disc images can be swapped via control apps like [pidectl](pidectl.md).

## First Boot

1. Insert the prepared microSD card (see [SD Card Setup](sd-card.md))
2. Power on the computer
4. The BIOS should detect PicoIDE as an IDE hard disk or ATAPI CD-ROM depending on your configuration

If the device isn't detected, check that the IDE cable is connected correctly and that the jumper is set appropriately, and that the microSD card is inserted.
