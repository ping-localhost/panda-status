<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://github.com/ping-localhost/panda-status"><img align="center" src="https://i.imgur.com/bo7pxoH.png" alt="Panda Status" style="width:100%;height:100%"/></a>
  <br /><br /><strong>Panda Status</strong>
</h1>

_Control your BigTreeTech Panda Status via Home Assistant_

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ping-localhost/panda-status?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/ping-localhost/panda-status?style=for-the-badge)

---

## Overview

**Panda Status** is a Home Assistant custom integration for monitoring and controlling your BigTreeTech Panda Status device. It connects via WebSocket, parses messages, and exposes device data and controls to Home Assistant.

**Tested with**: V1.0.1

---

## Project Status

<table>
  <tr>
    <td><a href="https://github.com/ping-localhost/panda-status/actions/workflows/lint.yml" alt="lint"><img src="https://github.com/ping-localhost/panda-status/actions/workflows/lint.yml/badge.svg" alt="lint build"/></a></td>
    <td><a href="https://github.com/ping-localhost/panda-status/actions/workflows/validate.yml" alt="MS Build"><img src="https://github.com/ping-localhost/panda-status/actions/workflows/validate.yml/badge.svg" alt="MS Build"/></a></td>
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
- **RGB Idle Light** - Allows you enable/disable the idle light
  - It just sets the brightness to 0% or 100%.

### Select Entities

- **Light effect mode**: Lets you swap from mode on the fly (Music/H2D style).

## Installation

**Recommended:** Install via [HACS](https://hacs.xyz/)

1. Go to HACS → Integrations.
2. [Add this repo to your HACS custom repositories](https://hacs.xyz/docs/faq/custom_repositories).
3. Search for `Panda Status` and install.
4. Restart Home Assistant.
5. Set up via the configuration flow (YAML is not supported).

## Configuration

After installation, add the integration via Home Assistant UI:

1. Go to **Settings → Devices & Services**.
2. Click **Add Integration** and search for `Panda Status`.
3. Follow the setup prompts.
4. The required URL has to be something like `ws://192.168.0.33/ws`.

## Support & Issues

For issues or feature requests, open an [issue on GitHub](https://github.com/ping-localhost/panda-status/issues).

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
