# MyPoolCopilot

[![Install with HACS](https://img.shields.io/badge/HACS-Install-41BDF5?logo=home-assistant&style=for-the-badge)](https://github.com/gstax/mypoolcopilot)

Custom integration for Home Assistant to connect to your PoolCopilot system.

## ✨ Features

- Water Temperature
- Air Temperature
- Pool Pressure
- pH Level
- ORP (Oxidation-Reduction Potential)
- Ioniser Status
- Voltage Level
- Water Level
- Pump Status
- Pump Speed
- Valve Position
- PoolCopilot System Status

## 📦 Installation via HACS

1. Go to **HACS > Integrations > 3 dots menu > Custom Repositories**.
2. Add the repository URL:


- Choose **Integration** as the category.

3. Search for **MyPoolCopilot** in HACS and install it.
4. Restart Home Assistant if requested.
5. Add the integration via **Settings > Devices & Services > Add Integration**.
6. Enter your **API Key** when prompted.

## 🛠 Manual Installation (Alternative)

If you prefer, you can manually install the integration:

1. Copy the folder `custom_components/poolcopilot/` into your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.
3. Add the integration via the UI and provide your API Key.

## ⚙️ Configuration

Only one field is required:

- **API Key**:  
The key provided by your PoolCopilot management interface.

Once set up, the integration will automatically handle token refresh and create all entities.

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## ❗ Disclaimer

This project is a **personal** and **unofficial** integration for PoolCopilot systems.  
It is **not affiliated with or endorsed by PoolCopilot** or any of its parent companies.  
All trademarks and registered trademarks are the property of their respective owners.

---

🔮 See the [ROADMAP](ROADMAP.md) for planned improvements and future features.

