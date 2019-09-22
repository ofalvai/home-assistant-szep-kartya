from homeassistant.helpers.entity import Entity
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME

import requests
from bs4 import BeautifulSoup as bs
import re
import json

DOMAIN = 'szep_kartya'

CONF_CARD_NUMBER = 'card_number'
CONF_CARD_CODE = 'card_code'
CONF_MAIN_BALANCE = 'main_balance'
CONF_BALANCE_VENDEGLATAS = 'vendeglatas'
CONF_BALANCE_SZABADIDO = 'szabadido'
CONF_BALANCE_SZALLAS = 'szallas'
CONF_BALANCE_VALUES = [CONF_BALANCE_VENDEGLATAS, CONF_BALANCE_SZABADIDO, CONF_BALANCE_SZALLAS]

DEFAULT_NAME = 'SZÉP Kártya'
DEFAULT_UNIT = 'Ft'
DEFAULT_ICON = 'mdi:credit-card-outline'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_CARD_NUMBER): vol.All(cv.string, vol.Length(min=8, max=8)),
        vol.Required(CONF_CARD_CODE): vol.All(cv.string, vol.Length(min=3, max=3)),
        vol.Optional(CONF_NAME, DEFAULT_NAME): cv.string
    }
)

URL_API = 'https://magan.szepkartya.otpportalok.hu/ajax/egyenleglekerdezes/'
URL_HTML = 'https://magan.szepkartya.otpportalok.hu/fooldal/'


def setup_platform(hass, config, add_entities, discovery_info=None):
    card_number = config.get(CONF_CARD_NUMBER)
    card_code = config.get(CONF_CARD_CODE)
    main_balance = config.get(CONF_MAIN_BALANCE)
    name = config.get(CONF_NAME)

    sensor = SzepKartyaSensor(card_number, card_code, main_balance, name)
    sensor.update()

    add_entities([sensor])


class SzepKartyaSensor(Entity):

    def __init__(self, card_number: int, card_code: int, main_balance: str, name: str):
        self._state = None
        self.balance_vendeglatas = None
        self.balance_szabadido = None
        self.balance_szallas = None

        self.card_number: int = card_number
        self.card_code: int = card_code
        self.main_balance: str = main_balance
        self._name: str = name

        self.token: str = ''
        self.session_id: str = ''

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return sum([self.balance_szallas, self.balance_szabadido, self.balance_vendeglatas])

    @property
    def device_state_attributes(self):
        return {
            'Vendéglátás': f'{self.balance_vendeglatas} {DEFAULT_UNIT}',
            'Szabadidő': f'{self.balance_szabadido} {DEFAULT_UNIT}',
            'Szállás': f'{self.balance_szallas} {DEFAULT_UNIT}'
        }

    @property
    def unit_of_measurement(self):
        return DEFAULT_UNIT

    @property
    def icon(self):
        return DEFAULT_ICON

    def update(self):
        self.scrape_tokens()
        self.fetch_balance()
        self._state = self.balance_vendeglatas

    def scrape_tokens(self):
        response_html = requests.get(URL_HTML)
        soup = bs(response_html.text, 'html.parser')
        script_tag_text = soup.find('script', text=re.compile('ajax_token')).string

        match = re.search(r'ajax_token = \'([a-z0-9]{64})\'', script_tag_text)
        if not match:
            raise ValueError('Can\'t find ajax_token in script tag')

        self.token = match.group(1)
        self.session_id = response_html.cookies['PHPSESSID']

    def fetch_balance(self):
        request_body = f's_azonosito_k={self.card_number}&s_telekod_k={self.card_code}&ajax_token={self.token}'
        cookies = dict(PHPSESSID=self.session_id)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response_api = requests.post(URL_API, headers=headers, data=request_body, cookies=cookies)

        response_json = json.loads(response_api.text)
        self.balance_vendeglatas = parse_balance(response_json[1]['szamla_osszeg7'])
        self.balance_szabadido = parse_balance(response_json[1]['szamla_osszeg8'])
        self.balance_szallas = parse_balance(response_json[1]['szamla_osszeg9'])


def parse_balance(input_string: str) -> int:
    if input_string.strip() == '':
        return 0
    else:
        input_clean: str = input_string.strip().replace('+', '')
        return int(input_clean)
