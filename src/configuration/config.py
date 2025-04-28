import configparser


CONFIG_FILE = r'.\src\configuration\config.example.env'

config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding='utf-8')


SECRET_KEY = config.get('PROD', 'SECRET_KEY').strip()
ALGORITHM = config.get('PROD', 'ALGORITHM').strip()

print(f"{ALGORITHM} - {SECRET_KEY}")
