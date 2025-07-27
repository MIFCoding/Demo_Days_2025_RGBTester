# 🎚️ Audio Codec Testing System

![alt text](https://ibb.co/3yHhbxVY)

## 📌 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Report Examples](#-report-examples)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🎧 Supported Noise Types

| Noise Type | Parameters | Difficulty Levels |
|------------|------------|------------------|
| **Gaussian** | `amplitude=0.1-0.5` | Easy → Extreme |
| **White** | `intensity=0.05-0.3` | Easy → Hard |
| **Impulse** | `count=5-20`, `duration=0.01-0.1s` | Medium → Extreme |
| **Sinusoidal** | `freq=50-5000Hz` | Easy → Hard |
| **AC Hum** | 50Hz/60Hz | Easy → Medium |
| **Reverb** | `delay=0.1-0.5s`, `decay=0.2-0.8` | Hard → Extreme |

### 📊 Testing Capabilities
```python
# Example test configuration
TEST_CONFIG = {
    "groups": [5, 10, 20],  # Test different string lengths
    "iterations": 100,       # Tests per configuration
    "threshold": 0.9,        # Success threshold
    "modes": ["verbose", "silent", "html"]
}
```
