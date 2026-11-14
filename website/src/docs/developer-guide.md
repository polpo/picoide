# Developer Guide

This guide covers building PicoIDE firmware from source and contributing to the project.

## Repository Structure

```
picoide/
├── sw/                     # Main board firmware (RP2350)
├── sw-frontpanel/          # Front panel firmware (ESP32-C3)
├── hw/                     # Main board hardware design files
├── hw-frontpanel-3.5/      # Front panel hardware design files
└── docs/                   # Documentation (this site)
```

## Building Main Board Firmware

The main board runs on an RP2350 (Pimoroni PGA2350 variant) and uses the Pico SDK.

### Prerequisites

=== "Linux (Debian/Ubuntu)"

    ```bash
    sudo apt update
    sudo apt install git cmake gcc-arm-none-eabi build-essential
    ```

=== "macOS (Homebrew)"

    ```bash
    brew install cmake
    brew install --cask gcc-arm-embedded
    ```

=== "Windows"

    Use the [Pico Setup for Windows](https://github.com/raspberrypi/pico-setup-for-windows) installer, or use WSL with Linux instructions.

### SDK Setup

Clone the Pico SDK and set the environment variable:

```bash
git clone https://github.com/raspberrypi/pico-sdk.git ~/pico-sdk
export PICO_SDK_PATH="$HOME/pico-sdk"
```

Add the export to your `.bashrc` or `.zshrc` for persistence.

### Building

```bash
# Clone the repository with submodules
git clone --recurse-submodules https://github.com/polpo/picoide.git
cd picoide/sw

# Create build directory and build
mkdir build && cd build
cmake ..
make -j$(nproc)
```

Output: `picoide.uf2` in the build directory.

### Build Configuration

Key settings in `CMakeLists.txt`:

- **Board**: Pimoroni PGA2350
- **Clock**: 366 MHz (overclocked)
- **Language**: C++23
- **Panel Communication**: SPI (default) or I2C

## Building Front Panel Firmware

The front panel uses an ESP32-C3 and the ESP-IDF framework.

### Prerequisites

Install ESP-IDF v5.5 or later:

- [Linux/macOS Setup Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/linux-macos-setup.html)
- [Windows Setup Guide](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/get-started/windows-setup.html)

### Building

```bash
cd picoide/sw-frontpanel

# Source ESP-IDF environment (path may vary)
source ~/esp/esp-idf/export.sh

# Build
idf.py build
```

Output: `sw-frontpanel.bin` in the build directory.

### Flash and Monitor

```bash
idf.py flash monitor
```

### Using VS Code

Install the [ESP-IDF VS Code Extension](https://github.com/espressif/vscode-esp-idf-extension) for integrated development.

## Architecture Overview

### Main Board (RP2350)

The main board firmware is designed around the RP2350's unique capabilities:

**Multi-core Design**

- Core 0: Main protocol logic and command handling
- Core 1: IDE task processing (`ide_task.cpp`)

**PIO State Machines**

Hardware-accelerated IDE bus operations using PIO:

- IOW_PIO_SM (0) - Write operations
- IOWDMA_PIO_SM (1) - DMA write operations
- IOR_PIO_SM (2) - Read operations
- IORDMA_PIO_SM (3) - DMA read operations
- IOCS16_PIO_SM - 16-bit I/O chip select

**Key Components**

| File | Purpose |
|------|---------|
| `picoide.cpp` | Entry point, PIO initialization |
| `ide_task.cpp` | IDE command processing |
| `ide.h` | IDE register definitions |
| `harddisk/HardDiskDevice.cpp` | ATA hard disk emulation |
| `cdrom/CDRomDevice.cpp` | ATAPI CD-ROM emulation |
| `panel_protocol.cpp` | Front panel communication |
| `image_utils.cpp` | Disk image management |

### Front Panel (ESP32-C3)

**Key Components**

| File | Purpose |
|------|---------|
| `main.c` | Entry point, event loop |
| `ui_screens.c` | Display screens and menus |
| `button_handler.c` | Button input with debouncing |
| `wifi_manager.c` | WiFi AP and client modes |
| `web_server.cpp` | HTTP API and interface |
| `ota_manager.c` | Firmware update handling |

**Communication**

The front panel communicates with the main board via SPI:

- 4 MHz clock speed
- Command/response protocol
- Status updates, image selection, firmware transfer

## Contributing

### Code Style

- Follow existing patterns in the codebase
- No comments explaining removed code - just remove it cleanly
- Clean up unused includes and variables

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Test on hardware if possible
5. Submit PR with description of changes

### Testing

- Main firmware: Build and test on PGA2350 board
- Front panel: Build with ESP-IDF, test on ESP32-C3

### Documentation

When adding features, update relevant documentation in `docs/src/`.

## Resources

- [Pico SDK Documentation](https://www.raspberrypi.com/documentation/pico-sdk/)
- [ESP-IDF Documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/)
- [ATAPI Standard (SFF-8020i)](https://picog.us/docs/ide/SFF8020i.pdf) - CD-ROM command reference
