# MyPoolCopilot

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/) [![GitHub Release](https://img.shields.io/github/v/release/gstax/mypoolcopilot)](https://github.com/gstax/mypoolcopilot/releases)

MyPoolCopilot is a custom integration for Home Assistant to monitor your PoolCopilot system easily and efficiently.

## 🚀 Features

- Monitor water and air temperature.
- Display pool pressure, pH, ORP, ionizer status, and system voltage.
- Monitor pump status, pump speed, valve position, and PoolCop operational status.
- Full support for English and French languages.

## 🛠 Installation

1. Go to HACS ➔ Integrations ➔ "+", and add `https://github.com/gstax/mypoolcopilot` as a custom repository.
2. Install **MyPoolCopilot** from HACS.
3. Restart Home Assistant.
4. Add the MyPoolCopilot integration via **Settings ➔ Devices & Services ➔ Add Integration**.
5. Enter your PoolCopilot API Key.

⚠️ **Note:**  
The PoolCopilot API token expires after about 15 minutes.  
You must configure an automation to refresh the token regularly (see below).

## 🧩 Automatic PoolCopilot Token Refresh

Because the PoolCopilot API token expires quickly, you need to implement an automatic refresh system.

Here’s how:

### 1. Enable shell commands

In your `configuration.yaml`, add:

```yaml
shell_command: !include shell_commands.yaml
```

### 2. Create `shell_commands.yaml`

In your `/config/` directory, create a file called `shell_commands.yaml` containing:

```yaml
update_token_mypoolcopilot: /config/scripts/update_token_mypoolcopilot.sh
```

### 3. Create the token update script

Create `/config/scripts/update_token_mypoolcopilot.sh` with the following content:

```bash
#!/bin/bash

APIKEY="YOUR_API_KEY"
HA_TOKEN="YOUR_LONG_LIVED_ACCESS_TOKEN"
HA_URL="http://homeassistant.local:8123"

# Retrieve new PoolCopilot token
NEW_TOKEN=$(curl -s -X POST "https://poolcopilot.com/api/v1/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "APIKEY=$APIKEY" | jq -r '.token')

# Update token in Home Assistant input_text entity
curl -s -X POST "$HA_URL/api/states/input_text.token_poolcopilot" \
  -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"state\": \"$NEW_TOKEN\"}"
```

Make it executable:

```bash
chmod +x /config/scripts/update_token_mypoolcopilot.sh
```

### 4. Create the input_text entity

Add this to your `configuration.yaml`:

```yaml
input_text:
  token_poolcopilot:
    name: PoolCopilot Token
    initial: ""
```

Restart Home Assistant to apply changes.

### 5. Create the automation

Add this automation in Home Assistant:

```yaml
alias: "Update PoolCopilot Token"
description: "Automatically refresh the PoolCopilot token every 5 minutes."
trigger:
  - platform: time_pattern
    minutes: "/5"
condition: []
action:
  - service: shell_command.update_token_mypoolcopilot
mode: single
```

## ✅ Result

- The PoolCopilot token will be refreshed automatically every 5 minutes.
- The MyPoolCopilot integration will always have a valid token.
- No manual intervention required.

## 📈 Future Improvements

- Native automatic token refresh inside the MyPoolCopilot integration.
- Additional sensor device classes for better Home Assistant dashboard integration.
- Improved installation experience.

## 📢 Notes

- Only one instance of MyPoolCopilot can be configured per Home Assistant installation.
- This is a custom integration and is not affiliated with PoolCopilot or Home Assistant.

Enjoy monitoring your pool with Home Assistant! 🏊‍♂️

