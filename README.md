# MyPoolCopilot

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/) [![GitHub Release](https://img.shields.io/github/v/release/gstax/mypoolcopilot)](https://github.com/gstax/mypoolcopilot/releases)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Automatic PoolCopilot Token Refresh](#automatic-poolcopilot-token-refresh)
  - [1. Enable shell commands](#1-enable-shell-commands)
  - [2. Create `shell_commands.yaml`](#2-create-shell_commandsyaml)
  - [3. Create the token update script](#3-create-the-token-update-script)
  - [4. Create the input_text entity](#4-create-the-input_text-entity)
  - [5. Create the automation](#5-create-the-automation)
- [Result](#result)
- [Future Improvements](#future-improvements)
- [Notes](#notes)


MyPoolCopilot is a custom integration for Home Assistant to monitor your PoolCopilot system easily and efficiently.

## Features

- Monitor water and air temperature.
- Display pool pressure, pH, ORP, ionizer status, and system voltage.
- Monitor pump status, pump speed, valve position, and PoolCop operational status.
- Full support for English and French languages.

## Installation

1. Go to HACS ➔ Integrations ➔ "+", and add `https://github.com/gstax/mypoolcopilot` as a custom repository.
2. Install **MyPoolCopilot** from HACS.
3. Restart Home Assistant.
4. Add the MyPoolCopilot integration via **Settings ➔ Devices & Services ➔ Add Integration**.
5. Enter your PoolCopilot API Key.

**Note:**  
The PoolCopilot API token expires after 15 minutes.  
To ensure continuous operation, a token refresh automation every 5 minutes (to be safe) is required.
##  Automatic PoolCopilot Token Refresh

Because the PoolCopilot API token expires quickly, you need to implement an automatic refresh system.

Here’s how:

### 1. Enable shell commands

In your `configuration.yaml`, add:

```yaml
shell_command: !include shell_commands.yaml
```

### 2. Create `shell_commands.yaml`

In your `/config/scripts` directory, create a file called `shell_commands.yaml` containing:

```yaml
update_token_mypoolcopilot: /config/scripts/update_token_poolcopilot.sh
```

### 3. Create the token update script

Create `/config/scripts/update_token_poolcopilot.sh` with the following content:

```bash
#!/bin/bash

APIKEY="YOUR_API_KEY"
HA_TOKEN="YOUR_LONG_LIVED_ACCESS_TOKEN"

# **Note:**  
# You must use a Home Assistant **Long-Lived Access Token**.  
# To generate one, go to **Home Assistant Profile page** ➔ [http://homeassistant.local:8123/profile](http://homeassistant.local:8123/profile) ➔ scroll down to "Long-Lived Access Tokens" ➔ click "Create Token".

HA_URL="http://homeassistant.local:8123"
# **Important:**  
# If your Home Assistant is not accessible at `http://homeassistant.local:8123`,  
# you must edit the `HA_URL` variable in the script to match your actual URL or IP address.

ENTITY_ID="input_text.token_poolcopilot"
LOG_FILE="/config/logs/update_token_poolcopilot.log"

log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 🔍 Get current token
RESPONSE=$(curl -s -X GET "$HA_URL/api/states/$ENTITY_ID" -H "Authorization: Bearer $HA_TOKEN")
CURRENT_TOKEN=$(echo "$RESPONSE" | jq -r '.state')
log "🔐 Current token : $CURRENT_TOKEN"

# 🎯 Get a new token
NEW_TOKEN=$(curl -s -X POST "https://poolcopilot.com/api/v1/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "APIKEY=$APIKEY" | jq -r '.token')

if [ -z "$NEW_TOKEN" ] || [ "$NEW_TOKEN" = "null" ]; then
    log "❌ Cannot get a new token"
    exit 1
fi

# 🔁 Compare tokens
if [ "$NEW_TOKEN" = "$CURRENT_TOKEN" ]; then
    log "ℹ Unchanged token - not update needed"
else
    # ✅ Update token in Home Assistant
    curl -s -X POST "$HA_URL/api/states/$ENTITY_ID" \
        -H "Authorization: Bearer $HA_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"state\": \"$NEW_TOKEN\"}" >/dev/null
    log "✅ New token successfully updated"
fi

# 🧾 Get token expiration date
STATUS_JSON=$(curl -s -X GET "https://poolcopilot.com/api/v1/status" \
    -H "PoolCop-Token: $NEW_TOKEN" \
    -H "x-api-key: $APIKEY")

EXPIRE_TS=$(echo "$STATUS_JSON" | jq -r '.api_token.expire')
if [[ "$EXPIRE_TS" =~ ^[0-9]+$ ]]; then
    NOW=$(date +%s)
    REMAINING_SEC=$((EXPIRE_TS - NOW))
    REMAINING_MIN=$((REMAINING_SEC / 60))
    EXP_DATE=$(date -d @"$EXPIRE_TS" '+%Y-%m-%d %H:%M:%S')
    log "⏳ Token expires in $REMAINING_SEC seconds (~$REMAINING_MIN min) at $EXP_DATE"
else
    log "⚠ 'expire' field missing or invalid"
fi

exit 0

```

Make it executable:

```bash
chmod +x /config/scripts/update_token_poolcopilot.sh
```

### 4. Create the input_text entity

Add this to your `configuration.yaml`:

```yaml
input_text:
  token_poolcopilot:
    name: PoolCopilot Token
    max: 255
```

Restart Home Assistant to apply changes.

### 5. Create the automation

Add this automation in Home Assistant:

```yaml

alias: Update PoolCopilot token
description: ""
triggers:
  - trigger: time_pattern
    minutes: /5
conditions: []
actions:
  - action: shell_command.update_token_poolcopilot
    data: {}
  - delay:
      hours: 0
      minutes: 0
      seconds: 20
      milliseconds: 0
  - action: homeassistant.reload_config_entry
    data:
      entry_id: REPLACE WITH mypoolcopilot entry_id
mode: single
```

- you can find 'entry_id' with 'grep mypoolcopilot .storage/core.config_entries'


## Result

- The PoolCopilot token will be refreshed automatically every 5 minutes.
- The MyPoolCopilot integration will always have a valid token.
- No manual intervention required.

## Future Improvements

- Native automatic token refresh inside the MyPoolCopilot integration.
- Additional sensor device classes for better Home Assistant dashboard integration.
- Improved installation experience.

## Notes

- Only one instance of MyPoolCopilot can be configured per Home Assistant installation.
- This is a custom integration and is not affiliated in any way with PoolCopilot or Home Assistant.

Enjoy monitoring your pool with Home Assistant!

