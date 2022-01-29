import logging

from config.config_loader import ConfigLoader


def get_logger():
    return logging.getLogger('lightbulb.app')

def get_config_manager():
    config = ConfigLoader('./config.json')
    config.load_config()
    return config