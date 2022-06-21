import psycopg2
from decouple import config

connection = psycopg2.connect(host=config("DB_HOST"), port=config("DB_PORT"),
                              database=config('DB_NAME'), user=config('DB_USER'), password=config("DB_PASSWORD"))