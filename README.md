<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://github.com/BambamNZ/panda-status"><img width="500" height="500" alt="Panda_Aura_A1-6" src="https://github.com/user-attachments/assets/f5f1d966-ceb6-44a7-8495-edb5fceca019" />
</a>
  <br /><br /><strong>Panda Status</strong>
</h1>

_Control your BigTreeTech Panda Status via Home Assistant_

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ping-localhost/panda-status?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/BambamNZ/panda-status?style=for-the-badge)

---

## Overview

**Panda Status** custom Home Assistant integration for monitoring and controlling your BigTreeTech Panda Status device. Connection via WebSocket, parses messages, and exposes device data and controls to Home Assistant.

**Tested with**: V1.0.0 Panda Aura A1 / A1 Mini

---

## Project Status

<table>
  <tr>
    <td><a href="https://github.com/BambamNZ/panda-status/actions/workflows/lint.yml" alt="lint"><img src="https://github.com/BambamNZ/panda-status/actions/workflows/lint.yml/badge.svg" alt="lint build"/></a></td>
    <td><a href="https://github.com/BambamNZ/panda-status/actions/workflows/validate.yml" alt="MS Build"><img src="https://github.com/BambamNZ/panda-status/actions/workflows/validate.yml/badge.svg" alt="MS Build"/></a></td>
  </tr>
</table>

---

## Features

### Sensors

- **WiFi AP SSID**: Shows the SSID of the device's WiFi access point.
- **Device IP address**: Displays the IP address of the Panda Status device.
- **Device hostname**: Shows the hostname.
- **WiFi connection state**: Indicates connection status.
- **Printer name**: Displays the connected printer's name.
- **Printer IP address**: Shows the printer's IP.
- **Printer S/N**: Shows the printer's Serial Number.
- **Printer state**: Indicates printer status.
- **Firmware version**: Shows the firmware version.

### Switches

- **WiFi AP** - Allows you to enable/disable the AP.

### Light

- **RGB Idle Light** - Allows control the idle light
  - **Changes from original integration:**
  - Idle light as an entity in HA, with expected light controls

### Select Entities

- **Light effect mode**: Lets you swap from mode on the fly (Music/H2D style).

## Installation

**Recommended:** Install via [HACS](https://hacs.xyz/)

1. Go to HACS → Integrations.
2. [Add this repo to your HACS custom repositories](https://hacs.xyz/docs/faq/custom_repositories).
3. Search for `Panda Status` and install.
4. Restart Home Assistant.

## Configuration

After installation, add the integration via Home Assistant UI:

1. Go to **Settings → Devices & Services**.
2. Click **Add Integration** and search for `Panda Status`.
3. Follow the setup prompts.
4. The required URL has to be something like `ws://192.168.0.33/ws`.

## Support & Issues

For issues or feature requests, open an [issue on GitHub](https://github.com/BambamNZ/panda-status/issues).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
