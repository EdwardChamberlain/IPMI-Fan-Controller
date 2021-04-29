import json

import logging
import config
import ipmitools

template = {
    'ENABLE': 'False',
    'MANUAL_MODE': 'False',
    'FAN_SPEED': ''
}

try:
    path = '/data/startup.json' if not config.DEVELOP else 'data/startup.json'
    with open(path, 'r') as f:
        startup_script = json.load(f)
except:
    logging.error("Error opening startup script - Generating new script")
    with open(path, 'w') as f:
        json.dump(template, f)
    exit()

if startup_script['ENABLE'] == 'True':

    if startup_script['MANUAL_MODE'] == 'True':
        logging.info("Setting Manual Mode")
        ipmitools.set_manual_mode()

    if startup_script['FAN_SPEED']:
        logging.info(f"Setting Fan Speed: {startup_script['FAN_SPEED']}")
        ipmitools.set_fan_speed(startup_script['FAN_SPEED'])
