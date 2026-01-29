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

`pidectl` is an MS-DOS utility that allows control of PicoIDE directly from the computer you have your PicoIDE in. Browse directories, mount images, and manage the device without needing the front panel.

## Download

Pre-built `pidectl.exe` is bundled with compatible firmware, downloadable from the [releases page](https://github.com/polpo/picoide/releases).

## Usage

```
pidectl [options] <command> [args...]
```

### Options

| Option | Description |
|--------|-------------|
| `/p<port>` | IDE port (no space after `/p`): `p`=primary, `s`=secondary, `t`=tertiary, `q`=quaternary, or hex address |
| `/d<drive>` | Drive number (no space after `/d`): `0` or `m`=device 0 (default), `1` or `s`=device 1 |

### Commands

| Command | Description |
|---------|-------------|
| `list` | List images in current directory |
| `cd <index>` | Change to directory at index (0 for parent) |
| `load <index>` | Mount image at index |
| `load <name>` | Mount named image (use `""` to surround file names with spaces) |
| `eject` | Eject current image |
| `status` | Show current image status |
| `path` | Show current directory path |
| `prev` | Load previous image |
| `next` | Load next image |

## Examples

### Basic Usage

```
C:\> pidectl list
Index  Type  Name
-----  ----  ----
    1  DIR   games
    2  FILE  freedos.iso
    3  FILE  win95.iso

C:\> pidectl load 2
Loaded: freedos.iso

C:\> pidectl status
Image loaded: freedos.iso
```

### Browsing Directories

```
C:\> pidectl cd 1
Changed directory

C:\> pidectl path
/cdrom/games

C:\> pidectl list
Index  Type  Name
-----  ----  ----
    1  FILE  myst.iso
    2  FILE  quake.cue

C:\> pidectl load 1
Loaded: myst.iso

C:\> pidectl cd 0
Changed directory
```

Use `cd 0` to go to the parent directory.

### Switching Images

```
C:\> pidectl next
Loaded: quake.cue

C:\> pidectl prev
Loaded: myst.iso
```

### Using Different Ports

```
C:\> pidectl /ps list           # Secondary IDE (0x170)
C:\> pidectl /pt /d1 status     # Tertiary IDE, drive 1
C:\> pidectl /p170 list         # Explicit hex address
```

## Loading Images

The `load`, `eject`, `prev`, and `next` commands wait for the operation to complete before returning:

```
C:\> pidectl load 5
Loading...
Loaded: game.iso

C:\> pidectl status
Image loaded: game.iso
```

## Troubleshooting

### "Error: Device not ready"

- Check IDE cable connection
- Verify PicoIDE is powered on
- Verify PicoIDE has microSD card inserted
- Try different port or drive with `/p` or `/d` options (e.g., `/ps`, `/d1`)

### "Error: Invalid index"

Run `list` to see valid indices. Indices start at 1 and change after `cd` commands. Use index 0 to go to the parent directory.
