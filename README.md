# OTP SZÉP Kártya Home Assistant component

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Custom component for [Home Assistant](https://home-assistant.io) that tracks SZÉP Kártya account balance.

The state of the sensor is the sum of all sub-balances, but each sub-balance is exposed as a property.

![Screenshot](screenshot.png?raw=true)

## Installation

1. Install [HACS](https://hacs.xyz/)
2. Add this as a custom repository to HACS (`https://github.com/ofalvai/home-assistant-szep-kartya`)
3. Install from the integrations list
4. Add YAML config to `configuration.yaml` (see below)
5. Restart Home Assistant

## Configuration

``` yaml
sensor:
  - platform: szep_kartya
    card_number: !secret card_number
    card_code: !secret card_code
    name: SZÉP Kártya
    scan_interval:
      hours: 4
```

`card_number`: The last 8 digits of the card number (after the `61013242` prefix). Make sure to represent the number as string to avoid removing zeroes from the beginning.

`card_code`: "Telekód" (by default the last 3 digits of card number). Make sure to represent the number as string to avoid removing zeroes from the beginning.

`name` (optional): Friendly name of the sensor

`scan_interval`: Define an interval of a few hours (instead of the default 30 seconds). The API gives a captcha challenge if polled too frequently.
