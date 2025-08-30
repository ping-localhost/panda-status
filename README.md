<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo" href="https://www.aregtech.com"><img align="center" src="https://i.imgur.com/bo7pxoH.png" alt="Panda Status style="width:100%;height:100%"/></a>
  <br /><br /><strong>Panda Status</strong>
</h1>

_Control your BigTreeTech Panda Status via Home Assistant_

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ping-localhost/panda-status?style=for-the-badge)
![GitHub Release Date](https://img.shields.io/github/release-date/ping-localhost/panda-status?style=for-the-badge)

---

<!-- markdownlint-disable -->
## Project Status[![](https://raw.githubusercontent.com/ping-localhost/panda-status/master/docs/img/pin.svg)](#project-status)

<table class="no-border">
  <tr>
    <td><a href="https://github.com/ping-localhost/panda-status/actions/workflows/lint.yml" alt="lint"><img src="https://github.com/ping-localhost/panda-status/actions/workflows/lint.yml/badge.svg" alt="lint build"/></a></td>
    <td><a href="https://github.com/ping-localhost/panda-status/actions/workflows/validate.yml" alt="MS Build"><img src="https://github.com/ping-localhost/panda-status/actions/workflows/validate.yml/badge.svg" alt="MS Build"/></a></td>
  </tr>
</table>

---

## Introduction

This is a very simple integration that connects to the Panda Status WebSocket, parses it messages and allows you to change certain settings (currently just the idle light on/off).

## Installation

Recommended to be installed via [HACS](https://github.com/hacs/integration)

1. Go to HACS -> Integrations
2. [Add this repo to your HACS custom repositories](https://hacs.xyz/docs/faq/custom_repositories)
3. Search for `Panda Status` and install.
4. Restart Home Assistant
5. Setup via the configuration flow (YAML is not supported)
