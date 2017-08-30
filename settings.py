import yaml

with open("config.yml", 'r') as stream:
    config = yaml.load(stream)

DB_CONFIG = config.get('database')

SCHEME = 'http'
DOMAIN = '0.0.0.0:80'
