# SZÉP Kártya Home Assistant component

Custom component for [Home Assistant](https://homeassistant.io) that tracks the balance of a card.

The state of the sensor is the sum of all sub-balances, but each sub-balance is exposed as a property.

![Screenshot](screenshot.png?raw=true)

## Installation

1. Copy the folder `szep_kartya` to `custom_components` inside your Home Assistant config folder.
2. Restart Home Assistant (this installs the component's dependencies)
3. Add your config to `configuration.yaml` (see options below)
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

`card_number`: The last 8 digits of the card (after the `61013242` prefix)

`card_code`: "Telekód" (by default the last 3 digits of card number)

`name` (optional): Friendly name of the sensor

`scan_interval`: The API requires captcha if it's polled too frequently. Updating every few hours (instead of the default 30 seconds) seems to be OK though.
