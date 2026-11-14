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
# pidectl - Host Control Utility

`pidectl` is an MS-DOS and Win32 console utility that allows control of PicoIDE directly from the computer you have your PicoIDE in. Browse directories, mount images, and manage the device without needing the front panel. There are two versions: `pidectl.exe` for DOS, and `pidectl32.exe` for Windows (compatibility notes below).

Both versions take the same commands and pick a device the same way: by scanning for PicoIDEs and numbering which ones it finds. The `/d<index>` option picks which one, with the first found device being the default.

Pre-built `pidectl.exe` and `pidectl32.exe` are bundled with each firmware release, downloadable from the [releases page](../releases.md).

## Usage

```
pidectl [options] <command> [args...]
pidectl32 [options] <command> [args...]
```

Run with no command to see the built-in help. When the output is an interactive console, the help pauses at each full page.

### Options

Options go before the command. There is no space between an option letter and its value.

| Option | Description |
|--------|-------------|
| `/d<index>` | PicoIDE device to control, numbered as `devices` lists them (default: `0`, the first found) |
| `/p<port>` | DOS only: look on one IDE port instead of all four: `p`=primary (0x1F0), `s`=secondary (0x170), `t`=tertiary (0x1E8), `q`=quaternary (0x168), or a hex address such as `/p1F0` |
| `/v` | Show each port and drive (DOS) or driver interface (Windows) tried while finding the device |

### Commands

| Command | Description |
|---------|-------------|
| `devices` | List all detected PicoIDE devices |
| `list` | List images/directories in the current directory |
| `cd <index>` | Change to the directory at that index (`0` for the parent) |
| `cd <name>` | Change to the named subdirectory (case-insensitive; `..` for the parent) |
| `load <index>` | Mount the image at that index |
| `load <name>` | Mount the named image (put `""` around file names with spaces) |
| `eject` | Eject the current image (removable devices only) |
| `status` | Show firmware version, device type and loaded image |
| `path` | Show the full path of the current directory |
| `prev` | Load the previous image in the directory |
| `next` | Load the next image in the directory |

## Examples

### Basic Usage

```
C:\>pidectl list
Device 0: Pri port, drive 0
Current path: /cdrom

Index  Type  Name
-----  ----  ----
    1  DIR   games
    2  FILE  freedos.iso
    3  FILE  win95.iso

Total: 3 entries
Use 'pidectl cd 0' to go to parent directory

C:\>pidectl load 2
Device 0: Pri port, drive 0
Loading...
Loaded: freedos.iso

C:\>pidectl status
Device 0: Pri port, drive 0
PicoIDE running firmware: v0.8.0
Device: Pri port, drive 0
Device Type: CD-ROM (ATAPI)
Image Loaded: Yes
Image Name: freedos.iso
Directory: /cdrom
Image Index: 1 of 2
```

The `Device` line names the PicoIDE the command went to. On DOS it shows the IDE port and drive. On Windows it shows the drive letter or physical device, and the driver used to reach it (for example `E: via SPTI (ATAPI PACKET)`).

In HDD mode, `status` also shows the image's geometry (cylinders, heads and sectors).

### Browsing Directories

Change directory by index, or by name:

```
C:\>pidectl cd games
Device 0: Pri port, drive 0
Current path: /cdrom/games

C:\>pidectl list
Device 0: Pri port, drive 0
Current path: /cdrom/games

Index  Type  Name
-----  ----  ----
    1  FILE  myst.iso
    2  FILE  quake.cue

Total: 2 entries
Use 'pidectl cd 0' to go to parent directory

C:\>pidectl cd ..
Device 0: Pri port, drive 0
Current path: /cdrom
```

`cd 0` and `cd ..` both go to the parent directory. Directory names are matched case-insensitively, and names containing spaces must be quoted (e.g. `pidectl cd "The 7th Guest"`).

### Switching Images

This is useful for quickly switching between multiple images in a folder, such as for multi-CD games.

```
C:\>pidectl next
Device 0: Pri port, drive 0
Loaded: The 7th Guest Disc 2.iso

C:\>pidectl prev
Device 0: Pri port, drive 0
Loaded: The 7th Guest Disc 1.iso
```

### Choosing a Device

In dual mode, PicoIDE presents a separate device as each drive on the IDE channel, and each device has its own loaded image and its own current directory. The two virtual devices on one PicoIDE will appear as two devices in `pidectl devices`. The pidectl `/d` option selects which device a command controls, so `pidectl /d1 load 3` loads an image on the second PicoIDE device found. If you have mulitple PicoIDE units installed, they will all be found.

`devices` lists all of them and shows where each one is:

```
C:\>pidectl devices
Index  Port   Drive  Type             Image
-----  -----  -----  ---------------  -----
    0  Pri        0  Hard Disk (IDE)  win95.img
    1  Pri        1  CD-ROM (ATAPI)   (none)

Use /d<index> to control a device, e.g. 'pidectl /d1 list'
```

If there is only one PicoIDE in the machine and it's not in dual mode, it is always device 0 wherever it is plugged in, so you don't need `/d` to reach it.

### Limiting the Scan to One Port (DOS only)

This is usually not necessary but some other drives may not appreciate being scanned.

```
C:\>pidectl /ps list           # Secondary IDE (0x170) only
C:\>pidectl /pt /d1 status     # Second PicoIDE on the tertiary port
C:\>pidectl /p170 list         # Explicit hex address
```

A controller at a non-standard address can be reached by giving its port address with `/p<hex>`.

## Loading Images

The `load`, `eject`, `prev`, and `next` commands will wait up to about 10 seconds for the operation to complete. If it takes longer than that you will get a timeout message. If that happens, that usually means there is an issue with the SD card or there are other devices in the system conflicting with the PicoIDE.

```
C:\>pidectl load 5
Device 0: Pri port, drive 0
Loading...
Loaded: game.iso

C:\>pidectl eject
Device 0: Pri port, drive 0
Ejecting...
Image ejected successfully
```

## Windows

On Windows, `pidectl32` has to use different methods in the Windows storage drivers to access the PicoIDE, depending on the Windows version and if the PicoIDE device is in CD-ROM or HDD mode:

| PicoIDE mode | Windows 95 / 98 / ME | Windows NT 4.0 / 2000 / XP before SP2 | Windows XP SP2 and later |
|--------------|----------------------|----------------------------------------|--------------------------|
| CD-ROM (ATAPI) | ASPI (`WNASPI32.DLL`) | SPTI | SPTI |
| Hard disk (IDE) | `SMARTVSD.VXD` | not reachable | ATA pass-through (needs Administrator) |

`pidectl32` checks every device those drivers expose for the PicoIDE signature and numbers the PicoIDEs it finds in scan order. With no `/d` option, `pidectl32` controls the first PicoIDE found, just like in DOS. `devices` lists them all:

```
C:\>pidectl32 devices
Index  Device            Type             Image
-----  ----------------  ---------------  -----
    0  E:                CD-ROM (ATAPI)   quake.cue
    1  PhysicalDrive1    Hard Disk (IDE)  win95.img

Use /d<index> to control a device, e.g. 'pidectl32 /d1 list'
```

Devices are named by drive letter (`E:`) or `PhysicalDriveN` on the NT family. On Windows 9x they are named by IDE position (`Primary drive 1`) or ASPI adapter and target (`ASPI 0:1`).

Notes:

- The DOS `pidectl.exe` refuses to run on Windows.
- On Windows 9x, a CD-ROM mode PicoIDE needs `WNASPI32.DLL` installed. It ships with many CD burning programs and with Adaptec's ASPI package. `SMARTVSD.VXD` is part of Windows 95 OSR2 and later, but may need copying from `\WINDOWS\SYSTEM` to `\WINDOWS\SYSTEM\IOSUBSYS`.
- On Windows XP SP2 and later, run from an Administrator account to control a hard disk mode PicoIDE.
- Windows NT 4.0, 2000, and XP before SP2 have no driver interface that can send the hard disk control command, PicoIDE is only reachable in CD-ROM mode.
- If `devices` finds nothing, start by running it with `/v` (`pidectl32 /v devices`), which prints each driver interface as it is tried.

## Exit Codes

For use in batch files:

| Code | Meaning |
|------|---------|
| `0` | The command succeeded |
| `1` | The command failed: no PicoIDE found, the requested `/d` device is not present, or the device reported an error, such as if a `load`, `cd` or `eject` failed |
| `3` | Usage error: unknown option or command, missing argument, or invalid `/d` or `/p` value |

## Troubleshooting

### "No PicoIDE device found"

- Check the IDE cable connection
- Check that the PicoIDE is powered on
- Check that the PicoIDE has a microSD card inserted
- Check that the PicoIDE firmware is not too old or new for the version of `pidectl`. Use the version that comes with the firmware.
- Run with `/v` to see every port and drive (DOS) or driver interface (Windows) that was tried
- On DOS, a controller at a non-standard address can be named with `/p<hex>`
- On Windows, a hard disk mode PicoIDE needs XP SP2 or later with an Administrator account, or Windows 9x with `SMARTVSD.VXD`

### "PicoIDE device N not found"

The `/d` index is higher than the number of PicoIDEs found. Run `devices` to see the valid indices, which start at 0.

### "No directory named '...' here"

`cd <name>` only looks in the current directory and does not currently work with absolute paths. Run `list` to see the directories there, or use `cd` with an index.

### "Select entry failed"

The index given to `load` or `cd` does not exist in the current directory. Run `list` to see valid indices. Indices start at 1 and change after `cd` commands. Use index 0 to go to the parent directory.
