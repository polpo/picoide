# Troubleshooting

Common issues and solutions for PicoIDE.

## Device Not Detected by BIOS

### Symptoms
- Computer doesn't see PicoIDE during POST
- BIOS shows no IDE device on the channel

### Solutions

1. **Check IDE cable orientation**
   - Pin 1 (red stripe) should align on both ends

2. **Verify jumper settings**
   - Ensure M/S/CS jumper matches your configuration
   - Try M if PicoIDE is the only device on the channel
   - If the jumper is removed, PicoIDE is in [dual-device mode](getting-started.md#dual-device-mode) and must be the only drive on the channel

3. **Check power connection**
   - Berg connector should be fully seated

4. **Try a different IDE channel**
   - Test on primary vs secondary IDE
   - Test with and without other devices on the same channel

5. **Verify SD card is inserted and working**
   - PicoIDE won't function without a valid SD card
   - Try a different SD card or reformat (see section below)

## SD Card Not Recognized

### Symptoms
- Front panel shows "No SD Card"
- Images don't appear in file browser

### Solutions

1. **Check card format**
   - Must be FAT32 (exFAT coming soon)
   - Reformat using the [SD Association card formatter](https://www.sdcard.org/downloads/formatter/) for best results

2. **Try a different card**
   - Some cards have compatibility issues
   - Class 10 or UHS-I cards recommended

3. **Check card seating and clean contacts**
   - Remove and reinsert the card
   - Ensure it clicks into place
   - Check SD card contacts and clean with isopropyl alcohol if needed

## Front Panel Not Responding

### Symptoms
- Display stays blank
- Buttons have no effect
- Display shows garbled content

### Solutions

1. **Check cable connection**
   - Ensure ribbon cable is fully seated at both ends
   - Try reseating the cable (pull on the cable retention clip, reseat, and push the cable retention clip back in)

2. **Power cycle**
   - Disconnect power completely
   - Wait 10 seconds, reconnect

## Image Won't Load

### Symptoms
- Selecting an image does nothing
- "Error loading image" message

### Solutions

1. **Verify file format**
   - Hard disk: `.img`, `.vhd`, `.hda`, `.hdf`
   - CD-ROM: `.iso`, `.cue`, `.toast`
   - The file type also selects which device PicoIDE emulates, so an unrecognized one won't be browsable or auto-mounted

2. **Check file integrity**
   - Re-download or re-copy the image
   - Verify file isn't truncated (check size)

3. **For CUE/BIN files**
   - Ensure all `.bin` files referenced in `.cue` are present
   - Files must be in the same directory as the `.cue`

4. **Check the `image` path in picoide.ini**
   - Verify the file exists at the specified location
   - Check it's under the right device's section (`[device0]` or `[device1]`)

## WiFi Connection Issues

### Symptoms
- Can't connect to PicoIDE access point
- Can't connect PicoIDE to your network
- Web interface unreachable

### Solutions

1. **Reset WiFi to AP mode**
   - Front panel: Settings > WiFi > Reset WiFi
   - Reconnect using the device-specific default credentials

2. **Check network compatibility**
   - Must be 2.4 GHz (5 GHz not supported)
   - WPA/WPA2 security required

3. **Find your device's credentials**
   - Power on your PicoIDE and watch the splash screen for a few seconds
   - It displays your unique SSID (e.g., `PicoIDE-FrontPanel-XX`) and 8-letter password
   - Or check the startup logs if you built from source
   - Re-enter your network password carefully

4. **Check IP address**
   - View WiFi Status on front panel for current IP
   - Try accessing by IP instead of `picoide.local`

## CD Audio Not Playing

### Symptoms
- Music CD shows tracks but no sound
- Games with CD audio have no music

### Solutions

1. **Check audio connection**
   - Analog audio output must be connected to sound card
   - Verify cable is properly seated

2. **Verify image format**
   - Use CUE/BIN format for audio tracks
   - ISO format doesn't support audio tracks

3. **Check CUE file**
   - Ensure audio tracks are properly defined
   - Track types should be AUDIO, not MODE1/2352

---

## Frequently Asked Questions

### General

**What computers work with PicoIDE?**

Any computer with a standard 40-pin IDE interface. This includes most PCs from the 1990s through mid-2000s, as well as some other systems with IDE ports.

**Can I emulate two devices at the same time?**

Yes, using [dual-device mode](getting-started.md#dual-device-mode): remove the M/S/CS jumper and PicoIDE emulates both devices on the channel, configured by the `[device0]` and `[device1]` sections of `picoide.ini`. Each can be a hard disk or a CD-ROM drive, in any combination. No other drive can share the IDE channel in this mode.

With the jumper installed, PicoIDE emulates one device at a time, whose type follows the image configured in `[device0]`. To switch it, edit the configuration file and reboot.

**What's the maximum supported disk size?**

The IDE protocol supports up to 128 GB using LBA28 addressing. Actual limits depend on your BIOS and operating system.

### SD Cards

**What size SD card should I use?**

Any size works, but 8GB or larger is recommended to hold multiple disk images. The card must be formatted as FAT32 (up to 32GB) or exFAT (larger cards).

**Can I hot-swap the SD card?**

No. Always power off before removing or inserting the SD card to avoid corruption.

### Compatibility

**Does PicoIDE work with UDMA?**

No. PicoIDE supports PIO and MWDMA transfer modes. UDMA requires hardware changes that aren't currently implemented.

**My computer has issues with MWDMA **

Some systems or IDE controllers have buggy DMA implementations or trigger bugs in PicoIDE's DMA implementation. You can force PIO-only mode by adding this to `picoide.ini`:

```ini
[overrides]
max_mwdma_mode = -1
```

**I'm getting data corruption or read errors**

Some systems have trouble with the fastest transfer modes. Try lowering the maximum PIO mode in picoide.ini:

```ini
[overrides]
max_pio_mode = 3
```

If issues persist, try progressively lower values (2, 1, 0).

See the [Configuration Reference](sd-card.md#overrides-section) for all transfer mode options.

### Networking

**What's the default WiFi password?**

Each device has a unique 8-letter password (lowercase only), generated once on first boot. The password and SSID (e.g., `PicoIDE-FrontPanel-XX`) are displayed on the splash screen when powered on. See [Initial WiFi Setup](web-interface.md#initial-wifi-setup) for details.

**Can I use 5 GHz WiFi?**

No. The ESP32-C3 only supports 2.4 GHz WiFi.
