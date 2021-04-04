# OTP SZÉP Kártya Home Assistant component

Custom component for [Home Assistant](https://homeassistant.io) that tracks SZÉP Kártya account balance.

The state of the sensor is the sum of all sub-balances, but each sub-balance is exposed as a property.

![Screenshot](screenshot.png?raw=true)

## Installation

1. Copy the folder `szep_kartya` to `custom_components` inside your Home Assistant config folder.
2. Restart Home Assistant (this installs dependencies of the custom component)
3. Add YAML config to `configuration.yaml` (see below)
4. Restart Home Assistant again

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
