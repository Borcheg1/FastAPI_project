import os

from dotenv import load_dotenv


load_dotenv()

AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
VERIF_TOKEN = os.environ.get('VERIF_TOKEN')
RESET_TOKEN = os.environ.get('RESET_TOKEN')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_PASS = os.environ.get('DB_PASS')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')

TEST_DB_HOST = os.environ.get('TEST_DB_HOST')
TEST_DB_PORT = os.environ.get('TEST_DB_PORT')
TEST_DB_PASS = os.environ.get('TEST_DB_PASS')
TEST_DB_USER = os.environ.get('TEST_DB_USER')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')

SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
