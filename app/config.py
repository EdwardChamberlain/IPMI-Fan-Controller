import os
import logging
import secrets


class Flask_Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex()


IPMI_HOST = os.getenv('APP_IPMI_HOST') or None
IPMI_USER = os.getenv('APP_IPMI_USER') or None
IPMI_PASS = os.getenv('APP_IPMI_PASS') or None

MANUAL_MODE = False

logging.basicConfig(
    level=os.getenv('APP_LOG_LEVEL') or 'INFO',
    format="%(asctime)s::%(levelname)s::%(filename)s::%(message)s",
)
