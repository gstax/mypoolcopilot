# MyPoolCopilot

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/v/release/gstax/mypoolcopilot)](https://github.com/gstax/mypoolcopilot/releases)

MyPoolCopilot is a custom integration for Home Assistant that allows you to monitor your PoolCopilot system.

---

## Installation

1. Add this repository as a custom repository in HACS (type: Integration).
2. Install the **MyPoolCopilot** integration from HACS.
3. Restart Home Assistant.
4. Configure the integration by providing your PoolCopilot API Key.

⚠️ **Important**: The PoolCopilot API token expires after about 50 minutes.
You must set up an automation in Home Assistant to refresh the API token regularly and update it dynamically.

---

## Features

- Displays pool water temperature, air temperature, pressure, pH, ORP, ioniser status, and system voltage.
- Shows pump status, pump speed, valve position, and PoolCop operational status.
- Full support for English and French translations.

---

## Notes

- Only one instance of the integration is allowed.
- Automatic token refresh is not implemented yet inside the integration.

---

## Future improvements

- Native support for automatic token refresh.
- More device classes for better UI integration.

---

Enjoy monitoring your pool with Home Assistant! 🏊

