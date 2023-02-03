from os import path
import logging.config
import yaml

"""
	Description:
		- Logger setup with configuration to store .log file inside /logs/ directory
"""

yaml_path = './logs/config.yaml'

with open(yaml_path, 'r') as f:
	config = yaml.safe_load(f)
	logging.config.dictConfig(config)